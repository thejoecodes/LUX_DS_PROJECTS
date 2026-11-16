# Sales Analytics Without Pandas

## Overview & Approach

This project implements an end-to-end sales analytics pipeline using only Python's standard library (`csv`, `math`, and `pathlib`), with `pandas` reserved strictly for cross-checking the final headline figures.

The pipeline follows a four-stage architecture:
1. **Ingestion (`read_sales`)**: Streams raw string rows from `electronics_sales.csv` using `csv.DictReader` so column names are mapped dynamically without assuming fixed column indices.
2. **Validation & Cleaning (`parse_number`, `convert_rows`)**: Separates rows into trusted records (`clean_rows`) and quarantined records (`skipped_rows`) with explicit audit reasons rather than silently coercing corrupt data.
3. **Aggregation & Statistical Analysis (`total_revenue`, `revenue_by`, `top_n`, `high_value`, `mean`, `median`, `minimum_maximum`)**: Computes business metrics using plain Python dictionaries, list/dict comprehensions, and custom $O(n)$ / $O(n \log n)$ statistical functions without external libraries or built-in `min()`/`max()` helpers.
4. **Independent Verification (`verify_with_pandas`)**: Re-runs the exact same cleaning rules using vectorized `pandas` operations and compares every headline metric against the pure-Python output using relative floating-point tolerance (`math.isclose(..., rel_tol=1e-9)`).

---

## How to Run the Script

### Prerequisites
- **Python 3.10+** (required for `float | None` union type syntax).
- **`pandas`** (used solely in Task 8 for `verify_with_pandas`).

Install `pandas` if it is not already present in your environment:
```bash
pip install pandas
```

### Directory Layout
Place the CSV file either inside a `data/` subfolder (`data/electronics_sales.csv`, matching `DATA_PATH`) or in the same directory as `sales_analytics.py` (`./electronics_sales.csv`). The script automatically checks `data/electronics_sales.csv` first and falls back to `./electronics_sales.csv`.

```text
.
├── sales_analytics.py
├── README.md
└── data/
    └── electronics_sales.csv
```

### Execution
Run the script from your terminal:
```bash
python sales_analytics.py
```

---

## Data Cleaning Rules & Justifications

Every numeric field (`quantity` and `unit_price_kes`) passes through `parse_number()` and business-logic validation in `convert_rows()`. Below are the exact rules applied and why each decision was made:

| Input Pattern | Example in Dataset | Action | Justification |
| :--- | :--- | :--- | :--- |
| **Leading / trailing whitespace** | `" 2 "` | **Repair** (`strip()`) | Whitespace around numbers is a harmless formatting artifact from manual CSV exports. |
| **Currency prefix (`KES`)** | `"KES 18999"` (`S-3029`) | **Repair** (strip case-insensitive `KES` prefix) | The column (`unit_price_kes`) is already denominated in Kenyan Shillings; stripping an explicit `KES` label preserves an unambiguous numeric value. |
| **Thousands separators (`,`)** | `"38,999"` (`S-3017`) | **Repair** (`replace(",", "")`) | Standard comma grouping in formatted prices does not alter numeric magnitude once removed. |
| **Empty / `None` strings** | `""` (`S-3035`, `S-3039`) | **Skip** | Missing quantities or prices cannot be imputed without inventing revenue; skipping prevents artificial distortion. |
| **Placeholder text** | `"N/A"` (`S-3030`) | **Skip** | Explicitly marks unavailable data; treating it as `0` would falsely deflate average order value and distort product metrics. |
| **Spelled-out number words** | `"two"` (`S-3006`) | **Skip** | Parsing natural-language words introduces ambiguity (e.g., typos, regional spellings, or phrases like `"two or three"`). Rejecting non-digit words guarantees strict data integrity. |
| **Non-finite floats** | `"nan"`, `"inf"`, `"-inf"` | **Skip** (`math.isfinite()`) | Python's `float("nan")` and `float("inf")` succeed without raising `ValueError`, which would corrupt sums and means if not explicitly blocked. |
| **Zero or negative quantities** | `quantity <= 0` | **Skip** | A completed sales record must represent at least one unit sold; zero or negative quantities indicate unflagged returns or entry errors. |
| **Negative unit prices** | `unit_price_kes < 0` | **Skip** | Negative pricing represents a refund or data corruption rather than valid gross sales revenue. |

### Audit Summary on `electronics_sales.csv`
- **Rows read**: `50`
- **Rows used**: `46`
- **Rows skipped**: `4`
  - `S-3006`: unparseable quantity (`'two'`)
  - `S-3030`: unparseable `unit_price_kes` (`'N/A'`)
  - `S-3035`: unparseable quantity (`''`)
  - `S-3039`: unparseable `unit_price_kes` (`''`)

---

## Assumptions & Design Decisions

1. **Row-Level Revenue Rounding**: Each row's revenue is calculated as `round(qty * price, 2)` to avoid IEEE-754 binary floating-point drift during summation and `pandas` comparison.
2. **Tie-Breaking in `top_n()`**: Products are ranked by descending revenue (`-revenue`). When two or more products have identical total revenue, ties are broken **alphabetically in ascending order (A–Z)** by product name (`key=lambda item: (-item[1], item[0])`). This ensures deterministic, reproducible rankings across runs and matches the `pandas` verification sort order.
3. **High-Value Threshold Inclusivity**: `high_value(rows, threshold=50_000)` uses `>=` (`revenue >= 50000`), matching the report specification (`>= KES 50,000`). Store counts include all active stores from `revenue_by(clean_rows, "store")`, explicitly reporting `0` for stores with no qualifying transactions (such as `Mombasa City Mall`).
4. **Statistical Definitions**:
   - `mean()` computes the arithmetic mean ($\frac{1}{n}\sum x_i$).
   - `median()` sorts a copy of the values and returns the middle value for odd $n$, or the arithmetic mean of the two middle values for even $n$ (standard continuous median).
   - `minimum_maximum()` performs a single linear scan without built-in `min()`/`max()`.
   - All three statistical helpers raise a descriptive `ValueError` when given an empty list.
5. **Pandas Verification Alignment**: In `verify_with_pandas()`, the CSV is initially loaded with `dtype=str` so `pandas` does not apply implicit type inference before our custom cleaning rules run. Because both pipelines apply identical string sanitization and filtering, all four headline checks (`Total revenue`, `Revenue by product`, `Top 3`, and `Mean / median`) report `MATCH`.