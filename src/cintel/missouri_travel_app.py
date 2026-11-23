"""Missouri Travel Expenditure Dashboard.

Author: Angie Crews
Date: 2026-11-22

Analyze Missouri state travel expenditures for fiscal years 2022-2026.
Explore spending trends, agencies, expense types, and unusual payments.
"""

import marimo

__generated_with = "0.18.0"
app = marimo.App(width="full")


@app.cell
def _():
    from pathlib import Path

    import altair as alt
    import marimo as mo
    import polars as pl

    return Path, alt, mo, pl


@app.cell
def _(mo):
    mo.md(
        """
        # Missouri State Travel Expenditure Dashboard

        **Fiscal Years 2022–2026**

        This interactive application examines Missouri state travel
        expenditures to identify spending trends, compare state agencies,
        evaluate travel expense categories, and flag unusually large payments.

        **Data source:** Missouri State Expenditures

        **Project:** Continuous Intelligence — Module 6, Part D3
        """
    )


@app.cell
def _(Path, pl):
    data_file = Path("data/missouri_travel_2022_2026.csv")
    travel_df = pl.read_csv(data_file)
    return (travel_df,)


@app.cell
def _(mo, travel_df):
    mo.md(
        f"""
        ## Dataset Overview

        - **Total travel records:** {travel_df.height:,}
        - **Fiscal years:** 2022–2026
        - **Data:** Missouri state travel expenditures

        The dashboard examines annual spending, state agencies, travel expense
        categories, and unusually large individual payments.

        Use the fiscal-year selector to view all years or a single year.
        """
    )


@app.cell
def _(mo):
    year_selector = mo.ui.dropdown(
        options={
            "All Years (2022–2026)": "All",
            "2022": 2022,
            "2023": 2023,
            "2024": 2024,
            "2025": 2025,
            "2026": 2026,
        },
        value="All Years (2022–2026)",
        label="Select Fiscal Year",
    )
    mo.output.replace(year_selector)
    return (year_selector,)


@app.cell
def _(pl, travel_df, year_selector):
    selected_year = year_selector.value
    if selected_year == "All":
        filtered_travel_df = travel_df
        year_label = "2022–2026"
    else:
        filtered_travel_df = travel_df.filter(
            pl.col("Fiscal Year").cast(pl.Int32) == selected_year
        )
        year_label = str(selected_year)
    return filtered_travel_df, year_label


@app.cell
def _(pl, travel_df):
    annual_spending = (
        travel_df.group_by("Fiscal Year")
        .agg(
            pl.len().alias("records"),
            pl.col("payment_amount").sum().alias("total_spending"),
            pl.col("payment_amount").mean().alias("average_payment"),
        )
        .sort("Fiscal Year")
    )
    return (annual_spending,)


@app.cell
def _(alt, annual_spending, mo):
    chart_data = annual_spending.to_pandas()
    annual_chart = (
        alt.Chart(chart_data)
        .mark_bar(color="#3578B8")
        .encode(
            x=alt.X(
                "Fiscal Year:O",
                title="Fiscal Year",
                axis=alt.Axis(labelAngle=0),
            ),
            y=alt.Y(
                "total_spending:Q",
                title="Total Spending ($)",
                axis=alt.Axis(format="~s"),
            ),
            tooltip=[
                alt.Tooltip("Fiscal Year:O", title="Year"),
                alt.Tooltip("total_spending:Q", title="Total Spending", format="$,.2f"),
                alt.Tooltip("records:Q", title="Travel Records", format=","),
                alt.Tooltip(
                    "average_payment:Q", title="Average Payment", format="$,.2f"
                ),
            ],
        )
        .properties(
            title="Missouri Annual Travel Expenditures (2022–2026)",
            width=550,
            height=350,
        )
    )
    mo.vstack(
        [
            mo.md("## Annual Travel Spending"),
            annual_chart,
            mo.md(
                "Travel spending increased between 2022 and 2026. "
                "This chart always shows all five fiscal years "
                "to provide an overall spending comparison."
            ),
        ]
    )


@app.cell
def _(filtered_travel_df, pl):
    agency_spending = (
        filtered_travel_df.group_by("Agency Name")
        .agg(
            pl.len().alias("records"),
            pl.col("payment_amount").sum().alias("total_spending"),
        )
        .sort("total_spending", descending=True)
    )
    expense_spending = (
        filtered_travel_df.group_by("Detail Description")
        .agg(
            pl.len().alias("records"),
            pl.col("payment_amount").sum().alias("total_spending"),
        )
        .sort("total_spending", descending=True)
    )
    return agency_spending, expense_spending


@app.cell
def _(agency_spending, alt, expense_spending, mo, year_label):
    agency_chart = (
        alt.Chart(agency_spending.to_pandas())
        .mark_bar(color="#16877B")
        .encode(
            y=alt.Y(
                "Agency Name:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelLimit=260),
            ),
            x=alt.X(
                "total_spending:Q",
                title="Total Spending ($)",
                axis=alt.Axis(format="~s"),
            ),
            tooltip=[
                alt.Tooltip("Agency Name:N", title="Agency"),
                alt.Tooltip("total_spending:Q", title="Total Spending", format="$,.2f"),
                alt.Tooltip("records:Q", title="Travel Records", format=","),
            ],
        )
        .properties(
            title=f"Travel Spending by State Agency ({year_label})",
            width=850,
            height=650,
        )
    )
    expense_chart = (
        alt.Chart(expense_spending.to_pandas())
        .mark_bar(color="#D58A35")
        .encode(
            y=alt.Y(
                "Detail Description:N",
                sort="-x",
                title=None,
                axis=alt.Axis(labelLimit=280),
            ),
            x=alt.X(
                "total_spending:Q",
                title="Total Spending ($)",
                axis=alt.Axis(format="~s"),
            ),
            tooltip=[
                alt.Tooltip("Detail Description:N", title="Expense Type"),
                alt.Tooltip("total_spending:Q", title="Total Spending", format="$,.2f"),
                alt.Tooltip("records:Q", title="Travel Records", format=","),
            ],
        )
        .properties(
            title=f"Travel Spending by Expense Category ({year_label})",
            width=850,
            height=550,
        )
    )
    mo.vstack(
        [
            mo.md("## Travel Spending by State Agency"),
            agency_chart,
            mo.md(
                f"Compare total travel spending across Missouri "
                f"state agencies for {year_label}."
            ),
            mo.md("## Travel Spending by Expense Category"),
            expense_chart,
            mo.md(
                f"Compare lodging, mileage, meals, transportation, "
                f"and other travel expenses for {year_label}."
            ),
        ]
    )


@app.cell
def _(mo):
    payment_threshold = mo.ui.slider(
        start=1000,
        stop=100000,
        step=1000,
        value=10000,
        label="Flag payments greater than ($)",
        show_value=True,
    )
    mo.output.replace(payment_threshold)
    return (payment_threshold,)


@app.cell
def _(filtered_travel_df, payment_threshold, pl):
    unusual_payments = filtered_travel_df.filter(
        pl.col("payment_amount") > payment_threshold.value
    ).sort("payment_amount", descending=True)
    flagged_count = unusual_payments.height
    flagged_total = unusual_payments["payment_amount"].sum() or 0.0
    largest_payments = unusual_payments.select(
        "Fiscal Year",
        "Agency Name",
        "Detail Description",
        "Vendor Name",
        "payment_amount",
    ).head(20)
    return flagged_count, flagged_total, largest_payments


@app.cell
def _(
    flagged_count,
    flagged_total,
    largest_payments,
    mo,
    year_label,
):
    payment_table = largest_payments.to_pandas().rename(
        columns={
            "Fiscal Year": "Fiscal Year",
            "Agency Name": "Agency",
            "Detail Description": "Expense Type",
            "Vendor Name": "Vendor",
            "payment_amount": "Payment ($)",
        }
    )
    mo.vstack(
        [
            mo.md("## Unusual Travel Payments"),
            mo.md(
                "Flag individual payments above a chosen dollar amount. "
                "This is a screening rule, not proof of an error or improper spending."
            ),
            mo.md(
                f"**Selected period:** {year_label}  "
                f"\n\n**Flagged payments:** {flagged_count:,}  "
                f"\n\n**Combined value of flagged payments:** ${flagged_total:,.2f}"
            ),
            mo.md("### 20 Largest Flagged Payments"),
            mo.ui.table(payment_table, pagination=True, page_size=10),
            mo.md(
                "**Interpretation:** Review large payments in context. "
                "Different agencies and travel categories may have very different "
                "normal payment sizes. The threshold can be adjusted above."
            ),
        ]
    )


if __name__ == "__main__":
    app.run()
