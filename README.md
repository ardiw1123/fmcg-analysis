# FMCG Sales Performance Analysis

A comprehensive data analysis project examining **3 years of Fast-Moving Consumer Goods (FMCG) sales data** across multiple product categories, distribution channels, and regions. The project covers the full analytics pipeline — from data cleaning and feature engineering to exploratory data analysis (EDA) and interactive dashboard development.

---

## Project Overview

| Detail | Description |
|---|---|
| **Objective** | Analyze FMCG sales performance (Jan 2022 – Dec 2024) to identify revenue drivers, promotional effectiveness, seasonal patterns, and operational efficiency |
| **Dataset** | 190,757 transactions across 5 product categories, 3 distribution channels, and 3 regions |
| **Tools** | Python · pandas · NumPy · Matplotlib · Seaborn · Streamlit · Plotly |
| **Output** | 2 Jupyter notebooks (cleaning + EDA) and 1 interactive Streamlit dashboard |

---

## Project Structure

```
FMCG/
├── 01_FMCG_Sales.ipynb          # Data Cleaning & Feature Engineering
├── 02_FMCG_Sales.ipynb          # Exploratory Data Analysis (EDA)
├── dashboard.py                  # Interactive Streamlit Dashboard
├── Data/
│   ├── FMCG_2022_2024.csv       # Raw dataset (190K+ rows × 14 columns)
│   └── cleaned_FMCG_data.csv    # Cleaned dataset (190K+ rows × 26 columns)
└── README.md
```

---

## Notebooks

### Notebook 01 Data Cleaning & Feature Engineering

End-to-end data preparation pipeline:

- **Data Type Validation** Converted date columns, validated boolean flags, ensured numeric integrity
- **Negative Value Handling** Investigated and treated negative values in `stock_available`, `delivered_qty`, and `units_sold` (product returns / data entry errors)
- **Outlier Detection** Applied IQR × 3.0 winsorization to preserve valid business extremes while capping statistical outliers
- **Feature Engineering** Created 12 derived columns including:
  - `revenue` (price × units sold)
  - `sell_through_rate` (% of delivered quantity that was sold)
  - `stock_adequate` (binary flag for stock sufficiency)
  - Time-based features: `year`, `quarter`, `yearmonth`, `is_weekend`
  - `delivery_tier` (Same Day / Fast / Standard / Slow)

### Notebook 02 Exploratory Data Analysis (EDA)

Structured analysis driven by business questions:

| Section | Business Question |
|---|---|
| Distribution Overview | What is the distribution of key numerical variables? |
| Category Analysis | Which product categories are most profitable? |
| Channel Analysis | Which distribution channel is the most effective? |
| Regional Analysis | Which region is underperforming? |
| Promotion Effect | How significant is the impact of promotions on sales? |
| Time Trend Analysis | What are the YoY revenue trends and seasonal patterns? |
| Brand Analysis | Which brands dominate in each category? |
| Sell-Through & Operations | How efficient is the product distribution? |
| Correlation Analysis | Which variables have the most influence on revenue? |

---

## Interactive Dashboard

Built with **Streamlit** and **Plotly**, the dashboard provides real-time filtering and professional visualizations across three pages:

### Pages
- **Executive Overview**: KPI cards, monthly revenue trend, quarterly heatmap, category revenue breakdown, channel revenue share (donut chart)
- **Product & Channel**: Top 10 brands, category × channel stacked bars, monthly channel trends, average pricing analysis, pack type comparison
- **Operations & Promotion**: Sell-through rate by category, stock adequacy rates, promotion uplift analysis, delivery speed impact

### Features
- **Global Filters**: Year, Category, Channel, and Region multi-select filters
- **Responsive Layout**: Optimized for desktop with clean card-based design
- **Consistent Color Palette**: Category, channel, and region color coding across all charts
- **YoY Comparison**: Revenue growth tracking with delta indicators

### Running the Dashboard

```bash
# Install dependencies
pip install streamlit plotly pandas numpy

# Launch the dashboard
streamlit run dashboard.py
```

---

## Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.10+** | Core programming language |
| **pandas** | Data manipulation and analysis |
| **NumPy** | Numerical computations |
| **Matplotlib + Seaborn** | Static visualizations in notebooks |
| **Plotly** | Interactive charts in dashboard |
| **Streamlit** | Web-based dashboard framework |
| **Google Colab** | Notebook execution environment |

---

## Getting Started

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Setup

```bash
# Clone or download the project
cd FMCG

# Install required packages
pip install pandas numpy matplotlib seaborn streamlit plotly

# Run the dashboard
streamlit run dashboard.py
```

### Notebooks
Open `01_FMCG_Sales.ipynb` and `02_FMCG_Sales.ipynb` in **Google Colab** or **Jupyter Notebook** and execute cells sequentially.

---

## Author

**Ardi Gunawan Pratama**

---

*This project was developed as a portfolio piece demonstrating end-to-end data analysis skills for a Business Analyst role.*
