import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Import data
df = pd.read_csv(
    "fcc-forum-pageviews.csv",
    parse_dates=["date"],
    index_col="date"
)

# Clean data
df = df[
    (df["value"] >= df["value"].quantile(0.025)) &
    (df["value"] <= df["value"].quantile(0.975))
]


def draw_line_plot():
    # Copy data
    df_line = df.copy()

    # Draw line plot
    fig, ax = plt.subplots(figsize=(15, 5))

    ax.plot(df_line.index, df_line["value"], color="red", linewidth=1)

    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    fig.savefig("line_plot.png")

    return fig


def draw_bar_plot():
    # Copy data
    df_bar = df.copy()

    # Create year and month columns
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.strftime("%B")

    # Group and average
    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Reorder months
    months = [
        "January", "February", "March", "April",
        "May", "June", "July", "August",
        "September", "October", "November", "December"
    ]

    df_bar = df_bar[months]

    # Plot
    fig = df_bar.plot(kind="bar", figsize=(12, 8)).figure

    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    fig.savefig("bar_plot.png")

    return fig


def draw_box_plot():
    # Prepare data
    df_box = df.copy().reset_index()

    df_box["year"] = df_box["date"].dt.year
    df_box["month"] = df_box["date"].dt.strftime("%b")
    df_box["month_num"] = df_box["date"].dt.month

    df_box = df_box.sort_values("month_num")

    # Draw plots
    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    sns.boxplot(
        x="year",
        y="value",
        data=df_box,
        ax=axes[0]
    )

    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(
        x="month",
        y="value",
        data=df_box,
        order=[
            "Jan", "Feb", "Mar", "Apr",
            "May", "Jun", "Jul", "Aug",
            "Sep", "Oct", "Nov", "Dec"
        ],
        ax=axes[1]
    )

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    fig.savefig("box_plot.png")

    return fig
