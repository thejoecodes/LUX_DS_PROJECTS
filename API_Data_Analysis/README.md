# API Data Analysis Using Python Data Structures

This project retrieves sample user data from the [JSONPlaceholder Users API](https://jsonplaceholder.typicode.com/users) and explores it with Python data structures and data-analysis libraries. The analysis is implemented in [`Analysis.ipynb`](Analysis.ipynb).

## What the notebook does

- Fetches user records from the API with `requests`.
- Inspects the structure and data types of nested API records.
- Flattens selected user, address, and company fields into customer records, including email domains and numeric latitude/longitude.
- Uses Python sets and dictionaries to find unique cities and count customers by city and email top-level domain.
- Converts the cleaned records to a pandas DataFrame and inspects its shape and column types.
- Exports customer and city-count data as CSV files and saves a bar chart of the city distribution.

## Requirements

- Python 3.9 or newer
- JupyterLab or Jupyter Notebook
- `requests`, `pandas`, and `matplotlib`

## Setup and run

From this project directory, create and activate a virtual environment, install the dependencies, and launch JupyterLab:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install requests pandas matplotlib jupyterlab
jupyter lab
```

Open `Analysis.ipynb` in JupyterLab and run its cells from top to bottom. An internet connection is required to retrieve data from the API.

## Generated files

Running the notebook creates or updates:

- `output/customers.csv` — flattened customer data, including ID, contact details, city, coordinates, company, and website.
- `output/city_counts.csv` — customer count for each city.
- `city_distribution.png` — bar chart of the customer distribution by city.

The `output` directory must exist before running the notebook's CSV export cells; it is included in this project.
