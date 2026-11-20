# Uber Data Analysis — New York City, 2014

This repository contains my analysis of Uber pickups in New York City from April through September 2014. I combined the six monthly files and examined when pickups happened, how activity changed month to month, and how pickups were distributed across the five dispatch bases.

The analysis is in **Uber data analysis.ipynb**. The notebook expects the six monthly CSV files to be stored together in `data/raw/`. The original source is FiveThirtyEight's public Uber TLC FOIL dataset.

## Dataset

Source: [FiveThirtyEight — Uber TLC FOIL Response](https://github.com/fivethirtyeight/uber-tlc-foil-response). The pickup data was supplied to FiveThirtyEight by the New York City Taxi and Limousine Commission.

The project uses the six monthly CSVs for April–September 2014. Each file contains:

| Column | Meaning |
|---|---|
| Date/Time | Pickup date and time |
| Lat | Pickup latitude |
| Lon | Pickup longitude |
| Base | TLC base code affiliated with the pickup |

The six files contain **4,534,327 pickup records**. These are pickup-level records; they do not include fares, destinations, passenger counts, or trip duration.

## Run the project

Use Python 3.9 or later.

1. Clone the repository:
   ```bash
   git clone https://github.com/Akshay270406/Uber-Data-Analysis.git
   cd Uber-Data-Analysis
   ```
2. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
3. The six monthly CSV files are already included in `data/raw/`; no separate data download is required.
4. Start Jupyter:
   ```bash
   jupyter notebook
   ```
   Open **Uber data analysis.ipynb** and run the cells from top to bottom.

The notebook reads files from data/raw/. It no longer depends on a local shapefile path; the geographic view is plotted directly from pickup coordinates.

## Analysis performed

- Loaded and concatenated the six monthly CSVs.
- Converted pickup timestamps to datetime and derived date, month, weekday, and hour fields.
- Checked the combined dataset's dimensions, data types, missing values, duplicate rows, and dispatch-base counts.
- Compared pickup totals by month, weekday, and hour.
- Examined monthly patterns by hour and weekday using heatmaps.
- Compared dispatch-base volumes overall and by month.
- Plotted a sample of pickup coordinates to inspect their geographic spread.

Row counts use len(data) or data.shape[0]. DataFrame.size counts all cells (rows multiplied by columns), so it should not be used when the intended metric is number of pickup records.

## Findings from the six-month data

- **4,534,327 pickups** across April–September 2014.
- Monthly volume increased from **564,516 in April** to **1,028,136 in September**, an **82.13%** increase between those months.
- **Thursday** had the highest weekday total (**755,145**), followed by **Friday (741,139)**. Sunday had the lowest (**490,180**).
- The busiest pickup hour was **17:00 (5 PM)** with **336,190** pickups. The lowest was **02:00 (2 AM)** with **45,865**.
- The three largest dispatch bases were **B02617 (1,458,853)**, **B02598 (1,393,113)**, and **B02682 (1,212,789)**. Together they account for approximately **89.64%** of records.

These are raw totals over the period, not per-day averages. Months have different numbers of days, so monthly totals should not be interpreted as daily rates without normalizing by the number of days.

## Repository files

```text
Uber-Data-Analysis/
├── Uber data analysis.ipynb
├── README.md
├── requirements.txt
└── data/
    └── raw/
        ├── uber-raw-data-apr14.csv
        ├── uber-raw-data-may14.csv
        ├── uber-raw-data-jun14.csv
        ├── uber-raw-data-jul14.csv
        ├── uber-raw-data-aug14.csv
        └── uber-raw-data-sep14.csv
```

The six monthly CSVs are the input files required by the notebook.

## Interpretation notes

The analysis is descriptive. It identifies pickup-volume patterns but does not establish why demand changes, measure driver supply, or estimate causal effects. The coordinate plot shows pickup points, not official borough boundaries. The notebook does not establish a general Saturday-night surge in Lower Manhattan.

## Source

[FiveThirtyEight Uber TLC FOIL Response — pinned source revision](https://github.com/fivethirtyeight/uber-tlc-foil-response/tree/63bb878b76f47f69b4527d50af57aac26dead983/uber-trip-data).