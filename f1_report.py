"""
Formula 1 Data Visualization Project
Builds 8 charts from the Kaggle "Formula 1 World Championship" CSVs
and assembles them into a PDF report.

Run:  python f1_report.py
Needs the CSVs in ./data  (see README.md)
"""
import textwrap
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages

# ----------------------------------------------------------------- CONFIG
AUTHOR = "Anudev Shyna Dinesh"
UNIVERSITY = ""        # fill in your own
COURSE = ""            # fill in your own
STUDENT_ID = ""        # fill in your own
TITLE = "Formula 1 Data Visualization Report"
SUBTITLE = "Exploring Performance, Strategy, and Insights from Formula 1 Data"

SEASON = None                       # None = latest season in the data
COMPARE = ("hamilton", "max_verstappen")   # driverRef values for chart 2
PIT_DRIVERS = ["VER", "HAM", "LEC", "NOR", "ALO"]  # driver codes for chart 8
MAX_PIT_SECONDS = 60                # drop pit stops longer than this (red flags etc.)

# Write YOUR OWN analysis here. Each text is printed under its chart in the PDF.
INSIGHTS = {
    1: "",
    2: "",
    3: "",
    4: "",
    5: "",
    6: "",
    7: "",
    8: "",
}

DATA = Path("data")
OUT = Path("output")
OUT.mkdir(exist_ok=True)
sns.set_theme(style="whitegrid", palette="muted")


# ------------------------------------------------------------------ LOAD
def read(name):
    # Kaggle's Ergast CSVs use \N for missing values
    return pd.read_csv(DATA / name, na_values=["\\N"])


def load():
    races = read("races.csv")[["raceId", "year", "round", "name"]].rename(columns={"name": "race"})
    drivers = read("drivers.csv")
    drivers["driver"] = drivers["forename"] + " " + drivers["surname"]
    drivers = drivers[["driverId", "driverRef", "code", "driver"]]
    teams = read("constructors.csv")[["constructorId", "name"]].rename(columns={"name": "team"})

    res = read("results.csv")
    res["fastestLapSpeed"] = pd.to_numeric(res["fastestLapSpeed"], errors="coerce")
    res = (res.merge(races, on="raceId").merge(drivers, on="driverId").merge(teams, on="constructorId"))

    laps = read("lap_times.csv").merge(races[["raceId", "year"]], on="raceId").merge(drivers, on="driverId")
    pits = read("pit_stops.csv").merge(races[["raceId", "year"]], on="raceId").merge(drivers, on="driverId")
    pits["seconds"] = pits["milliseconds"] / 1000
    pits = pits[pits["seconds"] <= MAX_PIT_SECONDS]
    return res, laps, pits


# ---------------------------------------------------------------- CHARTS
def chart1(res, **_):
    season = SEASON or int(res["year"].max())
    r = res[res["year"] == season]
    top = r.groupby("team")["points"].sum().nlargest(4).index
    cum = (r[r["team"].isin(top)].groupby(["round", "team"])["points"].sum()
           .unstack("team").sort_index().fillna(0).cumsum())
    fig, ax = plt.subplots(figsize=(10, 6))
    for team in cum.columns:
        ax.plot(cum.index, cum[team], marker="o", label=team)
    ax.set(title=f"Constructor Championship Timeline ({season})", xlabel="Race round", ylabel="Cumulative points")
    ax.legend(title="Constructor")
    final = cum.iloc[-1].sort_values(ascending=False)
    facts = f"{season} final totals: " + ", ".join(f"{t} {p:.0f}" for t, p in final.items()) + "."
    cap = f"Cumulative points of the top four constructors in {season}."
    return fig, cap, facts


def chart2(laps, **_):
    lt = laps.copy()
    med = lt.groupby("raceId")["milliseconds"].transform("median")
    lt = lt[lt["milliseconds"] <= med * 1.07]          # drop pit-in/out and safety-car laps
    lt["gap"] = (lt["milliseconds"] - med) / 1000      # seconds vs race median, removes track-length effect
    lt = lt[lt["driverRef"].isin(COMPARE)]
    yearly = lt.groupby(["year", "driver"])["gap"].mean().unstack("driver")
    fig, ax = plt.subplots(figsize=(10, 6))
    for d in yearly.columns:
        ax.plot(yearly.index, yearly[d], marker="o", label=d)
    ax.axhline(0, color="grey", lw=0.8, ls="--")
    ax.set(title="Lap Pace vs Race Median: Hamilton vs Verstappen",
           xlabel="Year", ylabel="Mean lap time minus race median (s)")
    ax.legend()
    facts = ("Negative = faster than the typical car in the race. "
             "Lap times are compared to each race's median so different track lengths do not distort the chart.")
    cap = "Average lap-time gap to the race median by year (lower is faster)."
    return fig, cap, facts


def chart3(res, **_):
    season = SEASON or int(res["year"].max())
    r = res[(res["year"] == season)].dropna(subset=["fastestLapSpeed"]).copy()
    r["rel_speed"] = r["fastestLapSpeed"] - r.groupby("raceId")["fastestLapSpeed"].transform("mean")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.regplot(data=r, x="positionOrder", y="rel_speed", scatter_kws={"alpha": 0.5}, ax=ax)
    ax.set(title=f"Fastest-Lap Speed vs Finishing Position ({season})",
           xlabel="Finishing position", ylabel="Fastest-lap speed minus race average (km/h)")
    rho = r["positionOrder"].corr(r["rel_speed"], method="spearman")
    facts = f"Spearman correlation between finishing position and relative fastest-lap speed: {rho:.2f}."
    cap = "Each dot is one driver in one race; the line is a linear fit."
    return fig, cap, facts


def chart4(pits, **_):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(pits["seconds"], bins=40, kde=True, color="purple", ax=ax)
    ax.set(title="Pit Stop Duration Distribution", xlabel="Pit stop time in pit lane (s)", ylabel="Count")
    s = pits["seconds"]
    facts = (f"{len(s):,} stops, median {s.median():.1f}s, 5th-95th percentile {s.quantile(.05):.1f}-"
             f"{s.quantile(.95):.1f}s. These are full pit-lane times, not just the ~2.5s tyre change.")
    cap = f"Histogram of pit-lane time for stops up to {MAX_PIT_SECONDS}s."
    return fig, cap, facts


def chart5(res, **_):
    pod = res[res["positionOrder"] <= 3].groupby("driver").size().nlargest(10).sort_values()
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(pod.index, pod.values, color=sns.color_palette("flare", len(pod)))
    ax.set(title="Podium Finishes by Driver (Top 10, all seasons in data)", xlabel="Podiums", ylabel="")
    top = pod.index[-1]
    facts = f"{top} leads with {pod.iloc[-1]} podiums in this dataset."
    cap = "Number of top-three finishes per driver."
    return fig, cap, facts


def chart6(res, **_):
    y = res.dropna(subset=["fastestLapSpeed"]).groupby("year")["fastestLapSpeed"].agg(["max", "mean"])
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(y.index, y["max"], marker="o", label="Fastest of the season")
    ax.plot(y.index, y["mean"], marker="o", label="Average of race fastest laps")
    ax.set(title="Trends in Fastest-Lap Speeds Over the Years", xlabel="Year", ylabel="Speed (km/h)")
    ax.legend()
    facts = (f"Data covers {int(y.index.min())}-{int(y.index.max())}. "
             f"Season-best speed ranged from {y['max'].min():.0f} to {y['max'].max():.0f} km/h.")
    cap = "Fastest-lap speed per season. Track mix changes each year, so read trends with care."
    return fig, cap, facts


def chart7(res, pits, **_):
    pit_mean = pits.groupby(["raceId", "driverId"])["seconds"].mean().rename("pit_time").reset_index()
    d = res.merge(pit_mean, on=["raceId", "driverId"])
    d = d[d["grid"] > 0].rename(columns={"grid": "Grid", "positionOrder": "Finish",
                                          "points": "Points", "fastestLapSpeed": "FastLapSpeed",
                                          "pit_time": "PitTime", "year": "Year"})
    cols = ["Year", "Grid", "Finish", "Points", "FastLapSpeed", "PitTime"]
    corr = d[cols].corr()
    fig, ax = plt.subplots(figsize=(9, 7))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax)
    ax.set_title("Correlation Between Performance Metrics")
    facts = (f"Grid vs Finish: {corr.loc['Grid', 'Finish']:.2f}; Grid vs Points: {corr.loc['Grid', 'Points']:.2f}; "
             f"PitTime vs Finish: {corr.loc['PitTime', 'Finish']:.2f}. Based on {len(d):,} driver-races with pit data.")
    cap = "Pearson correlations. Correlation does not prove cause."
    return fig, cap, facts


def chart8(pits, **_):
    p = pits[pits["code"].isin(PIT_DRIVERS)]
    s = p.groupby("code")["seconds"].agg(Min="min", Avg="mean", Max="max").reindex(
        [c for c in PIT_DRIVERS if c in p["code"].unique()])
    fig, ax = plt.subplots(figsize=(10, 6))
    s.plot(kind="bar", ax=ax, rot=0, color=["#e0a020", "#d9703a", "#d94a66"])
    ax.set(title="Pit Stop Times by Driver", xlabel="Driver", ylabel="Time (s)")
    best = s["Avg"].idxmin()
    facts = f"Lowest average pit-lane time among the selected drivers: {best} ({s['Avg'].min():.1f}s)."
    cap = f"Minimum, average and maximum pit-lane time (stops up to {MAX_PIT_SECONDS}s)."
    return fig, cap, facts


CHARTS = [
    (1, "Constructor Championship Timeline", chart1),
    (2, "Lap Times Over the Years (Hamilton vs Verstappen)", chart2),
    (3, "Speed vs Finishing Position", chart3),
    (4, "Pit Stop Duration Distribution", chart4),
    (5, "Podium Finishes by Drivers", chart5),
    (6, "Trends in Fastest Lap Speeds Over the Years", chart6),
    (7, "Correlation Between Performance Metrics", chart7),
    (8, "Pit Stop Times", chart8),
]


# ------------------------------------------------------------------- PDF
A4 = (8.27, 11.69)


def cover(pdf):
    fig = plt.figure(figsize=A4)
    fig.text(0.5, 0.80, UNIVERSITY, ha="center", fontsize=16)
    fig.text(0.5, 0.65, TITLE, ha="center", fontsize=24, weight="bold", wrap=True)
    fig.text(0.5, 0.60, "\n".join(textwrap.wrap(SUBTITLE, 55)), ha="center", fontsize=13)
    fig.text(0.5, 0.40, AUTHOR, ha="center", fontsize=18, weight="bold")
    if STUDENT_ID:
        fig.text(0.5, 0.36, f"Student ID: {STUDENT_ID}", ha="center", fontsize=12)
    if COURSE:
        fig.text(0.5, 0.32, COURSE, ha="center", fontsize=12)
    pdf.savefig(fig)
    plt.close(fig)


def chart_page(pdf, num, title, png, cap, facts, insight):
    fig = plt.figure(figsize=A4)
    fig.text(0.08, 0.95, f"{num}. {title}", fontsize=16, weight="bold")
    ax = fig.add_axes([0.06, 0.50, 0.88, 0.42])
    ax.imshow(plt.imread(png))
    ax.axis("off")
    body = f"Figure {num}: {cap}\n\nKey numbers: {facts}"
    if insight.strip():
        body += f"\n\nAnalysis: {insight.strip()}"
    fig.text(0.08, 0.46, "\n".join(textwrap.fill(p, 95) for p in body.split("\n")),
             va="top", fontsize=10.5)
    pdf.savefig(fig)
    plt.close(fig)


def main():
    res, laps, pits = load()
    pdf_path = OUT / "F1_Report.pdf"
    with PdfPages(pdf_path) as pdf:
        cover(pdf)
        for num, title, fn in CHARTS:
            fig, cap, facts = fn(res=res, laps=laps, pits=pits)
            png = OUT / f"figure_{num}.png"
            fig.tight_layout()
            fig.savefig(png, dpi=200)
            plt.close(fig)
            chart_page(pdf, num, title, png, cap, facts, INSIGHTS.get(num, ""))
            print(f"done: figure {num} - {title}")
    print(f"\nReport saved to {pdf_path}")


if __name__ == "__main__":
    main()
