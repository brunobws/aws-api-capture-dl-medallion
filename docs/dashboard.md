# Dashboard

The Streamlit dashboard is the front-end of the data platform — a web application that connects directly to Athena and surfaces brewery analytics, pipeline execution history, and data quality results in one place.

It runs in a Docker container on the same EC2 instance as Airflow, accessible at port **8501**. Source code lives in [streamlit_app/](../streamlit_app/).

**Live dashboard:** http://56.124.50.116:8501/

![Dashboard Screenshot](images/dashboard-screenshot.png)

---

## Analytics

The Analytics tab queries the Gold layer Iceberg table (`gold.tb_ft_breweries_agg`) and displays pre-aggregated brewery data with cascading filters and interactive charts.

**Filters:** Country → State → Brewery Type, applied in cascade so each selection narrows the next.

**What you can see:**
- KPI cards showing total breweries, countries, states, and types in the current filter selection
- Bar chart of brewery count by type
- Bar chart of top states by brewery count
- Detailed sortable data table
- Export to CSV or JSON

Results are cached for 5 minutes to avoid unnecessary Athena queries on repeated interactions.

[Watch Analytics Demo](videos/01-analytics-dashboard-demo.mp4)

---

## Observability

The Observability tab reads from the `execution_logs` Athena table — the same table the `Logs` module writes to across Lambda and both Glue jobs. It shows the last 90 days of execution history.

**What you can see:**
- Pipeline health KPIs: total executions, success rate, warning count, error count
- Execution trend chart by week
- Status distribution (success / warning / error)
- Job performance metrics per component
- Recent execution details table with step-level timing from the `info` field

[Watch Observability Demo](videos/02-observability-logs-demo.mp4)

---

## Data Quality

The Data Quality tab reads from the `quality_logs` Athena table — written by the `Quality` module after each run of `bronze_to_silver`. It covers the last 90 days of quality check history.

**What you can see:**
- KPI cards: total tests run, pass rate, failure count
- Pie chart of test status distribution
- Most frequently failing columns
- Detailed test results table filterable by table, job, or status
- Export to CSV or JSON

[Watch Data Quality Demo](videos/03-data-quality-demo.mp4)

---

## Technical Notes

- **Backend:** All three tabs query Athena directly via [PyAthena](https://github.com/laughingman7743/PyAthena), using the same `AthenaService` wrapper
- **Caching:** Query results are cached for 300 seconds using a custom `cached_query` decorator to reduce Athena costs
- **Charts:** Built with [Plotly Express](https://plotly.com/python/plotly-express/) for interactive visualizations
- **Containerization:** Runs in Docker on EC2 — see [streamlit_app/Dockerfile](../streamlit_app/Dockerfile)