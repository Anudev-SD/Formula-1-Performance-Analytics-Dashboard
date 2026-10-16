# Formula 1 Data Visualization Project

## 1. Get the data
Download "Formula 1 World Championship (1950 - 2020)" from Kaggle and unzip.
Copy these files into a `data/` folder next to `f1_report.py`:

    races.csv  results.csv  drivers.csv  constructors.csv  lap_times.csv  pit_stops.csv

## 2. Install and run (Mac terminal)
    pip3 install -r requirements.txt
    python3 f1_report.py

Output goes to `output/`: figure_1.png ... figure_8.png and F1_Report.pdf

## 3. Make it yours
Open `f1_report.py` and edit the CONFIG block at the top:
- UNIVERSITY, COURSE, STUDENT_ID: your own details for the cover page
- SEASON: which year charts 1 and 3 use (default: latest in the data)
- COMPARE / PIT_DRIVERS: which drivers to show
- INSIGHTS: write your own analysis for each chart. It is printed under the chart in the PDF.

Look at each chart, then write what you actually see. The script prints
"key numbers" under each figure, but the interpretation should be yours.
