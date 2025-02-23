import csv
from datetime import date, timedelta

import matplotlib.pyplot as plt
import mpld3
import pandas as pd
from flask import Flask, redirect, render_template, request

app = Flask(__name__, template_folder="../../templates", static_folder="../../static")

WEIGHTS_FILE = "data/weights.csv"
MIN_VIEW = 74.5
MAX_VIEW = 82


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add", methods=["POST"])
def add():
    weight = request.form["weight"]
    with open("weights.csv", "a") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "weight"])
        writer.writerow(
            {"date": date.today(), "weight": weight.replace("+", ".").strip()}
        )

    return redirect("/display")


def create_plot():
    df = pd.read_csv(WEIGHTS_FILE, parse_dates=["date"])
    df = df.sort_values("date")  # Ensure dates are sorted

    fig, ax = plt.subplots(figsize=(4.5, 2.5))
    ax.plot(
        df["date"],
        df["weight"],
        marker="o",
        linestyle="-",
        color="r",
        label="Weight (kg)",
    )

    # Zoom y axis
    ax.set_ylim(bottom=MIN_VIEW, top=MAX_VIEW)

    # Optional: Extend x-axis slightly for better visualization
    if len(df) > 1:
        ax.set_xlim(
            left=df["date"].min() - timedelta(hours=12),
            right=df["date"].max() + timedelta(hours=12),
        )

    # Ensure first point starts at the leftmost part of the graph
    elif len(df) > 0:
        ax.set_xlim(
            left=df["date"].min() - timedelta(hours=12)
        )  # Start x-axis at the first date

    # Formatting
    # ax.set_title("Weight Over Time")
    # ax.set_xlabel("Date")
    # ax.set_ylabel("Weight (kg)")
    ax.legend()
    plt.xticks(rotation=45)

    return mpld3.fig_to_html(fig)


@app.route("/display")
def display():
    plot = create_plot()

    with open(WEIGHTS_FILE, "r") as f:
        reader = csv.DictReader(f)
        data = [
            {
                "date": date.fromisoformat(row["date"]),
                "weight": f"{float(row["weight"]):.2f}",
            }
            for row in reader
        ]

    return render_template("display.html", plot=plot, data=data)


@app.route("/delete/<date>")
def delete(date: str):
    with open(WEIGHTS_FILE, "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)

    for i, row in enumerate(data):
        if row["date"] == date:
            data.pop(i)
            break

    with open("weights.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "weight"])
        writer.writeheader()
        for row in data:
            writer.writerow(row)

    return redirect("/display")


if __name__ == "__main__":
    app.run(debug=True)
