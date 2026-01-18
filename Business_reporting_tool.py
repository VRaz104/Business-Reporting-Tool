"""
Sales Analysis Script
---------------------
Reads sales data from a CSV, calculates revenue, cost, profit, and profit margin,
plots daily revenue trends, and saves outputs with timestamped filenames.
Includes robust error handling, logging, and configuration-driven settings.
"""

import pandas as pd
import matplotlib.pyplot as plt
import logging
import json
import sys
from pathlib import Path
from datetime import datetime 
try:
    with open("config.json", "r") as f:
        config = json.load(f)
except FileNotFoundError:
    print("Configuration file 'config.json' not found.")
    sys.exit(1)
except json.JSONDecodeError as e:
    print(f"Error parsing config file: {e}")
    sys.exit(1)
DATA_FILE = config.get("data_file", "sales_data.csv")
DATE_COLUMN = config.get("date_column", "date")
LOG_FILE = config.get("log_file", "sales_analysis.log")
PLOT_TITLE = config.get("plot_title", "Daily Revenue Trend")
PLOT_XLABEL = config.get("plot_xlabel", "Date")
PLOT_YLABEL = config.get("plot_ylabel", "Revenue")
OUTPUT_DIR = config.get("output_dir", "outputs") 
Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    filemode='a', 
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logging.info("Script started")
try:
    df = pd.read_csv(DATA_FILE, parse_dates=[DATE_COLUMN])
    logging.info(f"Loaded data from {DATA_FILE} successfully.")
except FileNotFoundError:
    logging.error(f"Data file '{DATA_FILE}' not found.")
    sys.exit(1)
except pd.errors.ParserError as e:
    logging.error(f"Error parsing CSV file: {e}")
    sys.exit(1)
except Exception as e:
    logging.error(f"Unexpected error loading data: {e}")
    sys.exit(1)
required_columns = ["revenue", "cost"]
for col in required_columns:
    if col not in df.columns:
        logging.error(f"Missing required column: {col}")
        sys.exit(1)
try:
    df["profit"] = df["revenue"] - df["cost"]
    total_revenue = df["revenue"].sum()
    total_cost = df["cost"].sum()
    total_profit = df["profit"].sum()
    profit_margin = total_profit / total_revenue if total_revenue != 0 else 0
    summary = pd.DataFrame({
        "Metric": [
            "Total Revenue",
            "Total Cost",
            "Total Profit",
            "Profit Margin (%)"
        ],
        "Value": [
            total_revenue,
            total_cost,
            total_profit,
            round(profit_margin * 100, 2)
        ]
    })
    print("\n=== BUSINESS PERFORMANCE SUMMARY ===\n")
    print(summary.to_string(index=False))
    logging.info("Metrics calculated and summary printed successfully.")
    today = datetime.today().strftime("%Y%m%d")
    summary_file = Path(OUTPUT_DIR) / f"summary_{today}.csv"
    summary.to_csv(summary_file, index=False)
    logging.info(f"Summary saved to {summary_file}")
    print(f"\nSummary saved to: {summary_file}")
except Exception as e:
    logging.error(f"Error calculating metrics: {e}")
    sys.exit(1)
try:
    daily_revenue = df.groupby(DATE_COLUMN)["revenue"].sum()
    plt.figure(figsize=(10, 5))
    daily_revenue.plot(marker='o')
    plt.title(PLOT_TITLE)
    plt.xlabel(PLOT_XLABEL)
    plt.ylabel(PLOT_YLABEL)
    plt.grid(True)
    plt.tight_layout()
    plot_file = Path(OUTPUT_DIR) / f"daily_revenue_{today}.png"
    plt.savefig(plot_file)
    plt.show()
    logging.info(f"Daily revenue plot saved to {plot_file}")
    print(f"Plot saved to: {plot_file}")
except Exception as e:
    logging.error(f"Error plotting daily revenue: {e}")