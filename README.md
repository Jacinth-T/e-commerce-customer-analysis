# Project 05 — E-Commerce Customer Behavior Analysis

A web-based data analytics dashboard that analyzes e-commerce customer behavior using **RFM segmentation**, **product analytics**, and **regional revenue mapping**. Built with Python, Pandas, SQLite, and Streamlit.

---

## 🚀 Setup

### 1. Download the Dataset

Download the **UCI Online Retail Dataset** from:
- [UCI ML Repository — Online Retail](https://archive.ics.uci.edu/ml/datasets/online+retail)
- Direct download: [Online Retail.xlsx](https://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx)

Save the file as `data/online_retail.csv` (convert from .xlsx to .csv if needed, or the setup script handles .xlsx too).

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run Setup (One-Time)

```bash
python setup.py
```

This script:
- Cleans the raw dataset (removes nulls, cancelled orders, invalid rows)
- Computes RFM scores and customer segments
- Generates product and regional summaries
- Stores everything in a SQLite database at `db/ecommerce.db`

### 4. Launch the Dashboard

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501` to view the dashboard.

---

## 📁 Project Structure

```
project05_ecommerce/
│
├── data/
│   └── online_retail.csv          # Raw dataset (downloaded by user)
│
├── db/
│   └── ecommerce.db               # SQLite database (auto-generated)
│
├── modules/
│   ├── __init__.py
│   ├── alpha_ingest.py            # Module Alpha — data cleaning & loading
│   ├── beta_rfm.py                # Module Beta  — RFM segmentation
│   ├── gamma_products.py          # Module Gamma — product analytics
│   └── delta_regional.py          # Module Delta — regional revenue
│
├── pages/
│   ├── __init__.py
│   ├── 2_Customer_Segments.py     # RFM scatter + segment breakdown
│   ├── 3_Product_Analytics.py     # Top products charts
│   ├── 4_Purchase_Timeline.py     # Monthly revenue trends
│   └── 5_Regional_Revenue.py      # Country-level revenue view
│
├── database.py                    # DB connection + table creation + SQL queries
├── app.py                         # Streamlit entry point (Home/Overview)
├── setup.py                       # One-time data pipeline script
├── requirements.txt
└── README.md
```

---

## 📦 Modules

| Module | File | Purpose |
|--------|------|---------|
| **Alpha** | `alpha_ingest.py` | Loads raw CSV, cleans data, stores in SQLite |
| **Beta** | `beta_rfm.py` | Computes RFM scores and segments customers |
| **Gamma** | `gamma_products.py` | Aggregates product sales data |
| **Delta** | `delta_regional.py` | Aggregates revenue by country |

---

## 📊 Dashboard Pages

1. **Overview** — KPI cards showing total customers, revenue, orders, and countries
2. **Customer Segments** — RFM scatter plot, segment bar chart, summary table
3. **Product Analytics** — Top products by revenue and quantity, searchable catalog
4. **Purchase Timeline** — Monthly revenue trends and order volume over time
5. **Regional Revenue** — Country-level bar chart, world choropleth map, data table

---

## 📈 Dataset

- **Source:** UCI Machine Learning Repository — [Online Retail Dataset](https://archive.ics.uci.edu/ml/datasets/online+retail)
- **Size:** ~540,000 transactions, 8 columns
- **Time Range:** December 2010 – December 2011
- **Origin:** UK-based online gift retailer
- **Columns:** InvoiceNo, StockCode, Description, Quantity, InvoiceDate, UnitPrice, CustomerID, Country

---
