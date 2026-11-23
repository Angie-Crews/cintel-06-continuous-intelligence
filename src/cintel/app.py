"""app.py - Reactive marimo app for this project.

Author: Angie Crews
Date: 2026-11

Purpose:
- Monitor system performance using continuous intelligence.
- Calculate error rate and average latency signals.
- Detect observations exceeding defined thresholds.
- Classify system health as STABLE, WARNING, or CRITICAL.
- Compare overall system health with individual observations.
- Display an interactive observation health chart.

RUN LOCALLY:

    uv run marimo edit src/cintel/app.py
    uv run marimo run src/cintel/app.py

Press CTRL+c in the terminal to stop the app.

WASM DEPENDENCIES:

Browser-based WebAssembly environments require separate
dependency installation. Local execution uses the project
dependencies managed by uv.

NO LOGGING:

The reactive app does not create persistent log files.

PLAN CELLS:

1. Imports and dependencies.
2. Title and introduction.
3. Load system metrics and design signals.
4. Interactive threshold controls.
5. Detect anomalies and classify system health.
6. Display observation health summary.
7. Display observation health chart.
8. Display overall system assessment.
9. Display anomalous observations.
10. Closing information.
"""

# === INITIALIZE MARIMO ===

import marimo

__generated_with = "0.25.0"

app = marimo.App(width="medium")


# === CELL 1: IMPORTS AND DEPENDENCIES ===


@app.cell
async def _():
    import sys

    if sys.platform == "emscripten":
        import micropip

        await micropip.install(["polars", "pandas", "pyarrow", "altair"])

    import marimo as mo
    import polars as pl

    from cintel.utils_system import (
        design_signals,
        load_system_metrics,
    )

    return design_signals, load_system_metrics, mo, pl, sys


# === CELL 2: TITLE AND INTRODUCTION ===


@app.cell
def _(mo):
    mo.md(
        r"""
        # Continuous Intelligence

        This application combines signal design (Module 3)
        and anomaly detection (Module 2) to evaluate
        system health.

        Three assessment levels are used:

        - 🟢 **STABLE** - No thresholds exceeded.
        - 🟡 **WARNING** - One threshold exceeded.
        - 🔴 **CRITICAL** - Two thresholds exceeded.

        The application evaluates both overall system health
        and individual observations.

        Move the sliders below to explore how changing
        thresholds affects system classifications.
        """
    )


# === CELL 3: LOAD DATA AND DESIGN SIGNALS ===


@app.cell
def _(design_signals, load_system_metrics, mo, sys):
    """Load system metrics and calculate monitoring signals."""
    notebook_location = mo.notebook_location()

    if notebook_location is None:
        raise RuntimeError("Unable to determine notebook location.")

    filename = "system_metrics.csv"

    if sys.platform == "emscripten":
        from pyodide.http import open_url  # ty: ignore[import-not-found]

        data_url = notebook_location / "public" / filename
        df = load_system_metrics(open_url(str(data_url)))
    else:
        data_path = notebook_location.parents[1] / "data" / filename
        df = load_system_metrics(data_path)

    df = design_signals(df)

    return (df,)


# === CELL 4: INTERACTIVE THRESHOLD CONTROLS ===


@app.cell
def _(mo):
    max_error_rate = mo.ui.slider(
        start=0.0,
        stop=0.5,
        value=0.05,
        step=0.01,
        label="Max error rate",
    )

    max_avg_latency = mo.ui.slider(
        start=0,
        stop=200,
        value=40,
        step=1,
        label="Max avg latency (ms)",
    )

    mo.hstack(
        [max_error_rate, max_avg_latency],
        justify="space-between",
    )

    return max_avg_latency, max_error_rate


# === CELL 5: DETECT ANOMALIES AND CLASSIFY HEALTH ===


@app.cell
def _(df, max_avg_latency, max_error_rate, pl):
    """Evaluate individual observations and overall health."""
    # Detect anomalies exceeding either threshold.
    anomalies_df = df.filter(
        (pl.col("error_rate") > max_error_rate.value)
        | (pl.col("avg_latency_ms") > max_avg_latency.value)
    )

    # Add observation numbers.
    observations_df = df.with_row_index(
        "observation",
        offset=1,
    )

    # Count threshold violations for each observation.
    observations_df = observations_df.with_columns(
        (
            (pl.col("error_rate") > max_error_rate.value).cast(pl.Int64)
            + (pl.col("avg_latency_ms") > max_avg_latency.value).cast(pl.Int64)
        ).alias("thresholds_exceeded")
    )

    # Assign individual health classifications.
    observations_df = observations_df.with_columns(
        pl.when(pl.col("thresholds_exceeded") >= 2)
        .then(pl.lit("CRITICAL"))
        .when(pl.col("thresholds_exceeded") == 1)
        .then(pl.lit("WARNING"))
        .otherwise(pl.lit("STABLE"))
        .alias("system_state")
    )

    # Calculate overall system averages.
    summary_df = df.select(
        [
            pl.col("requests").mean().alias("avg_requests"),
            pl.col("errors").mean().alias("avg_errors"),
            pl.col("error_rate").mean().alias("avg_error_rate"),
            pl.col("avg_latency_ms").mean().alias("avg_latency_ms"),
        ]
    )

    # Count overall threshold violations.
    summary_df = summary_df.with_columns(
        (
            (pl.col("avg_error_rate") > max_error_rate.value).cast(pl.Int64)
            + (pl.col("avg_latency_ms") > max_avg_latency.value).cast(pl.Int64)
        ).alias("thresholds_exceeded")
    )

    # Assign overall system classification.
    summary_df = summary_df.with_columns(
        pl.when(pl.col("thresholds_exceeded") >= 2)
        .then(pl.lit("CRITICAL"))
        .when(pl.col("thresholds_exceeded") == 1)
        .then(pl.lit("WARNING"))
        .otherwise(pl.lit("STABLE"))
        .alias("system_state")
    )

    return anomalies_df, observations_df, summary_df


# === CELL 6: OBSERVATION HEALTH SUMMARY ===


@app.cell
def _(mo, observations_df, pl):
    """Display counts for each health classification."""
    counts = observations_df.group_by("system_state").len()

    def count_state(state):
        result = counts.filter(pl.col("system_state") == state)
        return result["len"][0] if result.height > 0 else 0

    stable = count_state("STABLE")
    warning = count_state("WARNING")
    critical = count_state("CRITICAL")

    total = observations_df.height

    mo.md(
        f"""
        ## Observation Health Summary

        | Status | Observations |
        |:---|---:|
        | 🟢 **STABLE** | {stable} |
        | 🟡 **WARNING** | {warning} |
        | 🔴 **CRITICAL** | {critical} |

        **Total observations:** {total}
        """
    )


# === CELL 7: OBSERVATION HEALTH CHART ===


@app.cell
def _(mo, observations_df):
    """Display a color-coded chart of system observations."""
    from typing import cast

    import altair as alt

    # Prepare chart data.
    chart_df = observations_df.select(
        [
            "observation",
            "system_state",
        ]
    ).to_pandas()

    # Build chart using Altair.
    chart = alt.Chart(chart_df)

    # Apply rectangle marks.
    # The ignore comment is limited to Altair's
    # dynamic method typing.
    chart = cast(alt.Chart, chart.mark_rect())

    # Configure observation position and health colors.
    chart = chart.encode(  # type: ignore[attr-defined]
        x=alt.X(
            "observation:O",
            title="Observation Number",
            axis=alt.Axis(labels=False),
        ),
        color=alt.Color(
            "system_state:N",
            title="System Health",
            scale=alt.Scale(
                domain=[
                    "STABLE",
                    "WARNING",
                    "CRITICAL",
                ],
                range=[
                    "#2E8B57",
                    "#F4B400",
                    "#D9534F",
                ],
            ),
        ),
        tooltip=[
            "observation:O",
            "system_state:N",
        ],
    )

    # Set chart dimensions and title.
    chart = chart.properties(
        title="System Health Across 60 Observations",
        height=100,
        width=600,
    )

    # Display the interactive chart.
    mo.ui.altair_chart(chart)


# === CELL 8: OVERALL SYSTEM ASSESSMENT ===


@app.cell
def _(mo, summary_df):
    state = summary_df.to_dicts()[0]["system_state"]

    status_icons = {
        "STABLE": "🟢",
        "WARNING": "🟡",
        "CRITICAL": "🔴",
    }

    status_icon = status_icons.get(state, "")

    mo.md(f"## Overall System State: {status_icon} **{state}**")


@app.cell
def _(mo, summary_df):
    mo.ui.table(summary_df)


# === CELL 9: ANOMALOUS OBSERVATIONS ===


@app.cell
def _(anomalies_df, mo):
    mo.md(
        f"""
        ## Anomaly Detection Results

        **{anomalies_df.height} anomalous observations**
        detected at the selected thresholds.
        """
    )


@app.cell
def _(anomalies_df, mo):
    mo.ui.table(anomalies_df)


# === CELL 10: CLOSING INFORMATION ===


@app.cell
def _(mo):
    mo.md(
        r"""
        ---

        ### Project Interpretation

        Overall system averages may appear stable even
        when individual observations show warning or
        critical conditions.

        Evaluating both overall performance and individual
        observations provides a more complete assessment
        of system health.

        ---

        [Learn more about Marimo](https://marimo.io/)

        **Running locally?**

        Press **CTRL+c** in the VS Code terminal
        to stop the application.
        """
    )


# === CONDITIONAL EXECUTION GUARD ===

if __name__ == "__main__":
    app.run()
