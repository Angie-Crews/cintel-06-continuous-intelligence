"""Prepare Missouri travel expenditures for continuous intelligence analysis.

Author: Angie Crews
Date: 2026-11-22

Read annual Missouri State Expenditures files for 2022-2026,
filter travel spending, validate payment amounts, and create
a combined dataset for the custom monitoring application.
"""

from pathlib import Path

import polars as pl

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "missouri_travel_2022_2026.csv"

REQUIRED_COLUMNS = [
    "Fiscal Year",
    "Agency Name",
    "Category Description",
    "Detail Description",
    "Vendor Name",
    "Payments Total",
]


def main() -> None:
    """Combine and validate five years of travel expenditures."""
    files = sorted(DATA_DIR.glob("*State_Expenditures*.csv"))

    if len(files) != 5:
        raise ValueError(f"Expected 5 annual files, found {len(files)}")

    frames = []

    for file in files:
        df = pl.read_csv(file, infer_schema_length=0)

        missing = set(REQUIRED_COLUMNS) - set(df.columns)
        if missing:
            raise ValueError(f"{file.name}: missing columns {missing}")

        travel = df.filter(pl.col("Category Description") == "TRAVEL").with_columns(
            pl.col("Fiscal Year").cast(pl.Int32, strict=False),
            pl.col("Payments Total")
            .str.replace_all(",", "")
            .cast(pl.Float64, strict=False)
            .alias("payment_amount"),
        )

        invalid = travel.filter(
            pl.col("payment_amount").is_null()
            | ~pl.col("payment_amount").is_finite()
            | pl.col("Fiscal Year").is_null()
        ).height

        if invalid:
            raise ValueError(f"{file.name}: {invalid} invalid travel records")

        frames.append(
            travel.select(
                "Fiscal Year",
                "Agency Name",
                "Category Description",
                "Detail Description",
                "Vendor Name",
                "payment_amount",
            )
        )

        print(f"{file.name[:4]}: {travel.height:,} travel records")

    combined = pl.concat(frames).sort("Fiscal Year")

    combined.write_csv(OUTPUT_FILE)

    print(f"\nTotal travel records: {combined.height:,}")
    print(f"Saved: {OUTPUT_FILE}")

    print("\nAnnual travel expenditure summary:")
    summary = (
        combined.group_by("Fiscal Year")
        .agg(
            pl.len().alias("records"),
            pl.col("payment_amount").sum().alias("total_spending"),
            pl.col("payment_amount").mean().alias("average_payment"),
        )
        .sort("Fiscal Year")
    )
    print(summary)


if __name__ == "__main__":
    main()
