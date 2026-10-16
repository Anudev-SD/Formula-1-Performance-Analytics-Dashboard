# Formula 1 Data Visualization Project

## Overview

This project explores Formula 1 race data through data analysis and visualization. It uses historical race results, driver information, lap times, and pit-stop records to identify performance patterns and present insights through charts.

## Objectives

- Explore historical Formula 1 race data.
- Analyze driver and constructor performance.
- Examine lap times and fastest-lap performance.
- Explore pit-stop durations and their relationship with race results.
- Generate visualizations and compile them into a PDF report.

## Technologies Used

- Python
- Pandas
- NumPy
- Matplotlib
- Seaborn

## Dataset

The project uses Formula 1 CSV datasets containing:

- `races.csv`
- `drivers.csv`
- `constructors.csv`
- `results.csv`
- `lap_times.csv`
- `pit_stops.csv`

Place these files inside the `data/` directory before running the program.

## Project Structure

```text
formula-1-data-visualization/
├── f1_report.py
├── README.md
├── data/
│   ├── races.csv
│   ├── drivers.csv
│   ├── constructors.csv
│   ├── results.csv
│   ├── lap_times.csv
│   └── pit_stops.csv
└── output/
    ├── F1_Report.pdf
    └── figure_1.png ... figure_8.png
```

## Installation

Install the required Python packages:

```bash
python3 -m pip install pandas numpy matplotlib seaborn
```

## How to Run

1. Download the required dataset files.
2. Place the CSV files inside the `data/` directory.
3. Open a terminal in the project directory.
4. Run:

```bash
python3 f1_report.py
```

## Output

The program generates eight visualizations and combines them into a PDF report named `F1_Report.pdf` inside the `output/` directory.

## Skills Demonstrated

- Data cleaning and preparation
- Exploratory data analysis
- Data visualization
- Working with multiple related datasets
- Python scripting and report generation

##  Get the data
Download "Formula 1 World Championship (1950 - 2020)" from Kaggle and unzip.
Copy these files into a `data/` folder next to `f1_report.py`:

    races.csv  results.csv  drivers.csv  constructors.csv  lap_times.csv  pit_stops.csv

##  Install and run (Mac terminal)
    pip3 install -r requirements.txt
    python3 f1_report.py

Output goes to `output/`: figure_1.png ... figure_8.png and F1_Report.pdf

##  Make it yours
Open `f1_report.py` and edit the CONFIG block at the top:
- SEASON: which year charts 1 and 3 use (default: latest in the data)
- COMPARE / PIT_DRIVERS: which drivers to show
- INSIGHTS: write your own analysis for each chart. It is printed under the chart in the PDF.

Look at each chart, then write what you actually see. The script prints
"key numbers" under each figure, but the interpretation should be yours.

## Author

Anudev Shyna Dinesh
