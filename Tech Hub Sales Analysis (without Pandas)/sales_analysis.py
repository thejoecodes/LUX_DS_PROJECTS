"""
Sales Analytics Without Pandas

"""
import csv
from pathlib import Path

DATA_PATH = Path("data") / "electronics_sales.csv"


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with open(path, mode="r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        print(f"Read {reader.line_num} rows from {path}")
        return list(reader)


def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted."""
    try:
        # Remove currency symbols and commas
        cleaned_value = value.replace("Ksh", "").replace(",", "")
        return float(cleaned_value)
    except ValueError:
        return None


def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    clean_rows = []
    skipped_rows = []
    for row in rows:
        quantity = parse_number(row["quantity"])
        unit_price = parse_number(row["unit_price"])
        revenue = parse_number(row["revenue"])
        if quantity is not None and unit_price is not None and revenue is not None:
            clean_rows.append({**row, "quantity": quantity, "unit_price": unit_price, "revenue": revenue})
        else:
            skipped_rows.append(row)
    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    return sum(row["revenue"] for row in rows)


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals: dict[str, float] = {}
    for row in rows:
        key = row[field]
        totals[key] = totals.get(key, 0) + row["revenue"]
    return totals


def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    raise NotImplementedError


# Reusable statistics - implement these yourself, no statistics module.
def mean(values: list[float]) -> float:
    raise NotImplementedError


def median(values: list[float]) -> float:
    raise NotImplementedError


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    raise NotImplementedError


def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    raise NotImplementedError


def main(path: Path = DATA_PATH) -> None:
    """Read the CSV, clean it, and print some statistics."""
    rows = read_sales(path)
    clean_rows, skipped_rows = convert_rows(rows)

    print(f"Total rows: {len(rows)}")
    print(f"Clean rows: {len(clean_rows)}")
    print(f"Skipped rows: {len(skipped_rows)}")

    # Print some statistics
    print(f"Total revenue: {total_revenue(clean_rows)}")

if __name__ == "__main__":
    main(DATA_PATH)
