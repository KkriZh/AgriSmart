from __future__ import annotations

from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from logic import analyze_market, get_soil_fertility, get_weather, get_yield_stats

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "assets" / "charts"


def safe_df(fn, *args, **kwargs) -> pd.DataFrame:
    try:
        df = fn(*args, **kwargs)
    except Exception as exc:
        print(f"[warn] {fn.__name__} failed: {exc}")
        return pd.DataFrame()
    if df is None:
        return pd.DataFrame()
    return df


def save_figure(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(path, dpi=160)
    plt.close()


def chart_yield_by_crop() -> bool:
    df = safe_df(get_yield_stats)
    if df.empty:
        return False
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="year", y="yield_per_hectare", hue="crop_name")
    plt.title("Yield by Crop")
    plt.xlabel("Year")
    plt.ylabel("Yield (kg/hectare)")
    plt.grid(axis="y", alpha=0.3)
    save_figure(OUTPUT_DIR / "yield_by_crop.png")
    return True


def chart_yield_by_region() -> bool:
    df = safe_df(get_yield_stats)
    if df.empty:
        return False
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="year", y="yield_per_hectare", hue="region")
    plt.title("Yield by Region")
    plt.xlabel("Year")
    plt.ylabel("Yield (kg/hectare)")
    plt.grid(axis="y", alpha=0.3)
    save_figure(OUTPUT_DIR / "yield_by_region.png")
    return True


def chart_market_prices() -> bool:
    df = safe_df(analyze_market)
    if df.empty:
        return False
    plt.figure(figsize=(8, 5))
    sns.barplot(data=df, x="crop_name", y="price_per_KG", palette="viridis")
    plt.title("Market Price per KG")
    plt.xlabel("Crop")
    plt.ylabel("Price per KG")
    plt.xticks(rotation=25, ha="right")
    plt.grid(axis="y", alpha=0.3)
    save_figure(OUTPUT_DIR / "market_prices.png")
    return True


def chart_soil_fertility() -> bool:
    df = safe_df(get_soil_fertility)
    if df.empty:
        return False
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Fertility Level", order=["Low", "Medium", "High"], palette="Set2")
    plt.title("Soil Fertility Levels")
    plt.xlabel("Fertility Level")
    plt.ylabel("Count")
    plt.grid(axis="y", alpha=0.3)
    save_figure(OUTPUT_DIR / "soil_fertility.png")
    return True


def chart_weather_trend() -> bool:
    df = safe_df(get_weather)
    if df.empty:
        return False
    region = df["region"].iloc[0]
    df_region = df[df["region"] == region].copy()
    if df_region.empty:
        return False
    plt.figure(figsize=(8, 5))
    sns.lineplot(data=df_region, x="month", y="avg_temp", label="Avg Temp")
    sns.lineplot(data=df_region, x="month", y="rainfall_mm", label="Rainfall (mm)")
    plt.title(f"Weather Trends - {region}")
    plt.xlabel("Month")
    plt.ylabel("Value")
    plt.grid(alpha=0.3)
    save_figure(OUTPUT_DIR / "weather_trend.png")
    return True


def main() -> None:
    sns.set_theme(style="whitegrid")
    results = {
        "yield_by_crop": chart_yield_by_crop(),
        "yield_by_region": chart_yield_by_region(),
        "market_prices": chart_market_prices(),
        "soil_fertility": chart_soil_fertility(),
        "weather_trend": chart_weather_trend(),
    }
    for name, ok in results.items():
        status = "ok" if ok else "skipped"
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
