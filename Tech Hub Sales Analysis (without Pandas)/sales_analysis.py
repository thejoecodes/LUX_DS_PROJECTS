"""
Day 2 - Sales Analytics Without Pandas
Squad Python Specialization - Data Science, AI & Analytics

Tasks 1-7 use only the standard library. Pandas is allowed in task 8, to check your work.
"""
import csv
import math
from pathlib import Path

DATA_PATH = Path("data") / "electronics_sales.csv"


def read_sales(path: Path = DATA_PATH) -> list[dict[str, str]]:
    """Read the CSV with the csv module and return the raw rows."""
    with path.open(mode="r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        print(f"Rows read: {len(rows)} | Columns: {reader.fieldnames}")
        return rows


def parse_number(value: str) -> float | None:
    """Convert a messy numeric string to a float, or return None if it cannot be trusted."""
    if value is None:
        return None

    cleaned = value.strip()
    if not cleaned:
        return None

    # Safely repair currency prefixes ("KES 18999") and thousands separators ("38,999")
    if cleaned.upper().startswith("KES"):
        cleaned = cleaned[3:].strip()
    cleaned = cleaned.replace(",", "")

    try:
        num = float(cleaned)
    except ValueError:
        return None

    # Reject special float literals like "nan" or "inf"
    if not math.isfinite(num):
        return None

    return num


def convert_rows(rows: list[dict[str, str]]) -> tuple[list[dict], list[dict]]:
    """Return (clean_rows, skipped_rows). Clean rows have numeric quantity, unit price and revenue."""
    clean_rows: list[dict] = []
    skipped_rows: list[dict] = []

    for row in rows:
        sale_id = row.get("sale_id", "UNKNOWN")
        raw_qty = row.get("quantity", "")
        raw_price = row.get("unit_price_kes", "")

        qty = parse_number(raw_qty)
        price = parse_number(raw_price)

        if qty is None:
            skipped_rows.append({"sale_id": sale_id, "reason": f"unparseable quantity ({raw_qty!r})"})
            continue
        if price is None:
            skipped_rows.append({"sale_id": sale_id, "reason": f"unparseable unit_price_kes ({raw_price!r})"})
            continue
        if qty <= 0 or price < 0:
            skipped_rows.append({"sale_id": sale_id, "reason": f"non-positive value (qty={qty}, price={price})"})
            continue

        clean_row = dict(row)
        clean_row["quantity"] = int(qty) if qty.is_integer() else qty
        clean_row["unit_price_kes"] = price
        clean_row["revenue"] = round(qty * price, 2)
        clean_rows.append(clean_row)

    return clean_rows, skipped_rows


def total_revenue(rows: list[dict]) -> float:
    """Sum the revenue across all cleaned rows."""
    return sum(row["revenue"] for row in rows)


def revenue_by(rows: list[dict], field: str) -> dict[str, float]:
    """Total revenue grouped by any column (product, store, payment_method...)."""
    totals: dict[str, float] = {}
    for row in rows:
        key = row[field]
        if key not in totals:
            totals[key] = 0.0
        totals[key] += row["revenue"]
    return totals


def top_n(totals: dict[str, float], n: int = 3) -> list[tuple[str, float]]:
    """Return the n highest (key, value) pairs, highest first."""
    # Break ties deterministically by sorting alphabetically (ascending) on the key
    sorted_items = sorted(totals.items(), key=lambda item: (-item[1], item[0]))
    return sorted_items[:n]


def high_value(rows: list[dict], threshold: float) -> list[dict]:
    """Transactions whose revenue is at or above threshold (use a comprehension)."""
    return [row for row in rows if row["revenue"] >= threshold]


# Reusable statistics - implement these yourself, no statistics module.
def mean(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot compute mean of an empty list.")
    return sum(values) / len(values)


def median(values: list[float]) -> float:
    if not values:
        raise ValueError("Cannot compute median of an empty list.")
    ordered = sorted(values)
    count = len(ordered)
    mid = count // 2
    if count % 2 == 1:
        return float(ordered[mid])
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def minimum_maximum(values: list[float]) -> tuple[float, float]:
    if not values:
        raise ValueError("Cannot compute minimum and maximum of an empty list.")
    low = values[0]
    high = values[0]
    for val in values[1:]:
        if val < low:
            low = val
        if val > high:
            high = val
    return low, high


def verify_with_pandas(path: Path, my_results: dict) -> None:
    """Recompute the headline numbers with pandas and print whether each one matches."""
    import pandas as pd

    df = pd.read_csv(path, dtype=str)

    # Apply the exact same cleaning rules as parse_number() and convert_rows()
    for col in ("quantity", "unit_price_kes"):
        cleaned = (
            df[col]
            .fillna("")
            .str.strip()
            .str.replace(r"(?i)^KES\s*", "", regex=True)
            .str.replace(",", "", regex=False)
        )
        df[col] = pd.to_numeric(cleaned, errors="coerce")

    df = df.dropna(subset=["quantity", "unit_price_kes"]).copy()
    df = df[(df["quantity"] > 0) & (df["unit_price_kes"] >= 0)]
    df["revenue"] = (df["quantity"] * df["unit_price_kes"]).round(2)

    pd_total = float(df["revenue"].sum())
    pd_by_product = df.groupby("product")["revenue"].sum().to_dict()
    pd_top3 = sorted(pd_by_product.items(), key=lambda x: (-x[1], x[0]))[:3]
    pd_mean = float(df["revenue"].mean())
    pd_median = float(df["revenue"].median())

    print("=== pandas verification ===")

    # 1. Total revenue
    if math.isclose(my_results["total_revenue"], pd_total, rel_tol=1e-9):
        print("Total revenue      : MATCH")
    else:
        print(f"Total revenue      : MISMATCH (pure={my_results['total_revenue']:,.2f}, pandas={pd_total:,.2f})")

    # 2. Revenue by product
    prod_match = (
        my_results["revenue_by_product"].keys() == pd_by_product.keys()
        and all(math.isclose(my_results["revenue_by_product"][k], pd_by_product[k], rel_tol=1e-9) for k in pd_by_product)
    )
    if prod_match:
        print("Revenue by product : MATCH")
    else:
        print(f"Revenue by product : MISMATCH (pure={my_results['revenue_by_product']}, pandas={pd_by_product})")

    # 3. Top 3
    top3_match = (
        len(my_results["top_3"]) == len(pd_top3)
        and all(a[0] == b[0] and math.isclose(a[1], b[1], rel_tol=1e-9) for a, b in zip(my_results["top_3"], pd_top3))
    )
    if top3_match:
        print("Top 3              : MATCH")
    else:
        print(f"Top 3              : MISMATCH (pure={my_results['top_3']}, pandas={pd_top3})")

    # 4. Mean / median
    if (
        math.isclose(my_results["mean"], pd_mean, rel_tol=1e-9)
        and math.isclose(my_results["median"], pd_median, rel_tol=1e-9)
    ):
        print("Mean / median      : MATCH")
    else:
        print(
            f"Mean / median      : MISMATCH "
            f"(pure=({my_results['mean']:,.2f}, {my_results['median']:,.2f}), "
            f"pandas=({pd_mean:,.2f}, {pd_median:,.2f}))"
        )


if __name__ == "__main__":
    # Fall back to local file if data/ subdirectory does not exist
    csv_path = DATA_PATH if DATA_PATH.exists() else Path("electronics_sales.csv")

    raw_rows = read_sales(csv_path)
    clean_rows, skipped_rows = convert_rows(raw_rows)

    tot_rev = total_revenue(clean_rows)
    prod_rev = revenue_by(clean_rows, "product")
    store_rev = revenue_by(clean_rows, "store")
    payment_rev = revenue_by(clean_rows, "payment_method")
    top3_products = top_n(prod_rev, 3)

    threshold = 50_000
    hv_sales = high_value(clean_rows, threshold)
    # Dict comprehension counting high-value transactions per store (including 0-count stores)
    hv_counts_by_store = {
        store: sum(1 for row in hv_sales if row["store"] == store)
        for store in store_rev
    }

    revenues = [row["revenue"] for row in clean_rows]
    rev_mean = mean(revenues)
    rev_median = median(revenues)
    rev_min, rev_max = minimum_maximum(revenues)

    # Print formatted report matching expected_report.txt
    skipped_summary = ", ".join(f"{item['sale_id']}: {item['reason']}" for item in skipped_rows)

    print("\n=== Sales report: September 2026 ===")
    print(f"Rows read          : {len(raw_rows)}")
    print(f"Rows used          : {len(clean_rows)}")
    print(f"Rows skipped       : {len(skipped_rows)}   ({skipped_summary})\n")

    print(f"Total revenue (KES): {tot_rev:,.2f}\n")

    print("Revenue by product (KES)")
    for product, amount in sorted(prod_rev.items(), key=lambda x: (-x[1], x[0])):
        print(f"  {product:<22} {amount:>12,.2f}")

    print("\nTop 3 products")
    for rank, (product, amount) in enumerate(top3_products, start=1):
        print(f"  {rank}. {product} - KES {amount:,.2f}")

    print(f"\nHigh-value transactions (>= KES {threshold:,}): {len(hv_sales)}")
    for row in hv_sales:
        print(
            f"  {row['sale_id']}  {row['sale_date']}  {row['store']:<18} "
            f"{row['product']:<22} KES {row['revenue']:,.2f}"
        )

    print("\nHigh-value sales count by store:")
    for store, count in hv_counts_by_store.items():
        print(f"  {store:<22} {count}")

    print("\nTransaction revenue statistics")
    print(f"  mean   : {rev_mean:,.2f}")
    print(f"  median : {rev_median:,.2f}")
    print(f"  min    : {rev_min:,.2f}")
    print(f"  max    : {rev_max:,.2f}\n")

    verify_with_pandas(
        csv_path,
        {
            "total_revenue": tot_rev,
            "revenue_by_product": prod_rev,
            "top_3": top3_products,
            "mean": rev_mean,
            "median": rev_median,
        },
    )
