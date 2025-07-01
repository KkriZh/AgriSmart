import mysql.connector
from db import  get_connection
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def initialize_system():
    conn=get_connection()
    if conn:
        print("System Initialized: Database connected.")
        conn.close()
    else:
        raise ConnectionError("Failed to connect to the database")

def recommend_crops(duration=None,soil=None, temp=None, season=None, water_requirement=None):
    conn = get_connection()
    cursor = conn.cursor()
    conditions = []
    params = []
    if water_requirement:
        conditions.append("water_requirement = %s")
        params.append(water_requirement)
    if season:
        conditions.append("soil = %s")
        params.append(season)
    if duration:
        conditions.append("duration = %s")
        params.append(duration)
    if soil:
        conditions.append("soil = %s")
        params.append(soil)
    if temp is not None:
        conditions.append("ideal_temp_min <= %s AND ideal_temp_max >= %s")
        params.extend([temp, temp])

    query = "SELECT crop_name FROM crops"
    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    cursor.execute(query, tuple(params))
    results = cursor.fetchall()
    crops = [row[0] for row in results]
    cursor.close()
    conn.close()
    return crops

def crop_details(crop):
    conn=get_connection()
    cursor=conn.cursor()
    query="SELECT * FROM crops WHERE crop_name=%s"
    cursor.execute(query,(crop,))
    result=cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def estimate_resources(crop, land_area):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT fertilizer_name, dosage_per_hectare FROM fertilizers WHERE crop_name = %s"
    cursor.execute(query, (crop,))
    fert = cursor.fetchone()
    cursor.execute("SELECT method FROM irrigation WHERE crop_name = %s", (crop,))
    irrig = cursor.fetchone()
    cursor.close()
    conn.close()
    if fert:
        fert_name, dosage = fert
        total_fert = dosage * land_area
    else:
        fert_name, total_fert = None, 0
    return {
        "fertilizer": fert_name,
        "total_fertilizer": total_fert,
        "irrigation_method": irrig[0] if irrig else None
    }

def get_yield_stats(region=None, crop=None):
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT crop_name, region, year, yield_per_hectare FROM yield_history WHERE 1=1"
    params = []
    
    if region:
        query += " AND region = %s"
        params.append(region)
    if crop:
        query += " AND crop_name = %s"
        params.append(crop)

    query += " ORDER BY year"

    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=["crop_name", "region", "year", "yield_per_hectare"])
    return df


def plot_yield_by_crop():
    df=get_yield_stats()
    if df.empty:
        print("No data to plot.")
        return
    sns.lineplot(data=df, x="year", y="yield_per_hectare", hue="crop_name", marker="o")
    plt.title("Yield Trend by Crop")
    plt.xlabel("Year")
    plt.ylabel("Yield (kg/hectare)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_yield_by_region():
    df=get_yield_stats()
    if df.empty:
        print("No data to plot.")
        return
    sns.lineplot(data=df, x="year", y="yield_per_hectare", hue="region", marker="o")
    plt.title("Yield Trend by Region")
    plt.xlabel("Year")
    plt.ylabel("Yield (kg/hectare)")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_crop_region_matrix():
    df=get_yield_stats()
    if df.empty:
        print("No data to plot.")
        return
    pivot = df.pivot_table(index="crop_name", columns="region", values="yield_per_hectare", aggfunc="mean")
    sns.heatmap(pivot, annot=True, fmt=".1f", cmap="YlGnBu")
    plt.title("Average Yield per Crop by Region")
    plt.xlabel("Region")
    plt.ylabel("Crop")
    plt.tight_layout()
    plt.show()

def analyze_market(crops=None):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT crop_name, price_per_KG FROM market_prices"
    params = ()

    if crops:
        placeholders = ','.join(['%s'] * len(crops))
        query += f" WHERE crop_name IN ({placeholders})"
        params = tuple(crops)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=["crop_name", "price_per_KG"])
    return df

def plot_market_prices(crops=None):
    df = analyze_market(crops)
    if df.empty:
        print("No market price data found.")
        return
    plt.figure(figsize=(10, 6))
    sns.barplot(data=df, x="crop_name", y="price_per_KG", palette="viridis")
    plt.title("Market Price per KG by Crop")
    plt.ylabel("Price (₹)")
    plt.xlabel("Crop Name")
    plt.xticks(rotation=45)
    plt.grid(axis="y")
    plt.tight_layout()
    plt.show()

def get_soil_fertility():
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT type, fertility_level FROM soil_data"
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    df = pd.DataFrame(rows, columns=["Soil Type", "Fertility Level"])
    return df

def plot_soil_fertility_distribution():
    df = get_soil_fertility()
    if df.empty:
        print("No soil data found.")
        return
    
    plt.figure(figsize=(8, 5))
    sns.countplot(data=df, x="Fertility Level", order=["Low", "Medium", "High"], palette="Set2")
    plt.title("Distribution of Soil Fertility Levels")
    plt.xlabel("Fertility Level")
    plt.ylabel("Count of Soil Types")
    plt.tight_layout()
    plt.show()
