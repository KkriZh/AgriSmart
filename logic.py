import mysql.connector
from db import get_connection
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

user_info = {}

def initialize_system():
    conn = get_connection()
    if conn:
        print("System Initialized: Database connected.")
        conn.close()
    else:
        raise ConnectionError("Failed to connect to the database")

def save_user_data(name, location, preferences):
    global user_info
    user_info = {"name": name, "location": location, "preferences": preferences}
    print(f"User data saved: {user_info}")
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (username, region) VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE region = VALUES(region)
    """, (name, location))
    conn.commit()
    cursor.close()
    conn.close()

def recommend_crops(duration=None, soil=None, temp=None, season=None, water_requirement=None):
    conn = get_connection()
    cursor = conn.cursor()
    conditions = []
    params = []
    if water_requirement:
        conditions.append("water_requirement = %s")
        params.append(water_requirement)
    if season:
        conditions.append("season = %s")
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
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM crops WHERE crop_name=%s"
    cursor.execute(query, (crop,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result

def estimate_resources(crop, land_area):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fertilizer_name, dosage_per_hectare FROM fertilizers WHERE crop_name = %s", (crop,))
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
    return pd.DataFrame(rows, columns=["crop_name", "region", "year", "yield_per_hectare"])

def plot_yield_by_crop(embed_frame=None):
    df = get_yield_stats()
    if df.empty:
        print("No data to plot.")
        return
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="year", y="yield_per_hectare", hue="crop_name", ax=ax)
    ax.set_title("Yield Trend by Crop")
    ax.set_xlabel("Year")
    ax.set_ylabel("Yield (kg/hectare)")
    ax.grid(True)
    if embed_frame:
        canvas = FigureCanvasTkAgg(fig, master=embed_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        plt.tight_layout()
        plt.show()

def plot_yield_by_region(embed_frame=None):
    df = get_yield_stats()
    if df.empty:
        print("No data to plot.")
        return
    fig, ax = plt.subplots()
    sns.barplot(data=df, x="year", y="yield_per_hectare", hue="region", ax=ax)
    ax.set_title("Yield Trend by Region")
    ax.set_xlabel("Year")
    ax.set_ylabel("Yield (kg/hectare)")
    ax.grid(True)
    if embed_frame:
        canvas = FigureCanvasTkAgg(fig, master=embed_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    else:
        plt.tight_layout()
        plt.show()

def plot_crop_region_matrix():
    df = get_yield_stats()
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
    return pd.DataFrame(rows, columns=["crop_name", "price_per_KG"])

def plot_market_prices():
    df = analyze_market()
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
    cursor.execute("SELECT type, fertility_level FROM soil_data")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=["Soil Type", "Fertility Level"])

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

def get_weather(region=None, month=None):
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT region, month, avg_temp, rainfall_mm FROM weather_data WHERE 1=1"
    params = []
    if region:
        query += " AND region = %s"
        params.append(region)
    if month:
        query += " AND month = %s"
        params.append(month)
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=["region", "month", "avg_temp", "rainfall_mm"])

def plot_weather_trends(region):
    df = get_weather(region=region)
    if df.empty:
        print("No weather data found for this region.")
        return
    sns.lineplot(data=df, x="month", y="avg_temp", label="Avg Temp")
    sns.lineplot(data=df, x="month", y="rainfall_mm", label="Rainfall (mm)")
    plt.title(f"Weather Trends for {region}")
    plt.xlabel("Month")
    plt.ylabel("Value")
    plt.legend()
    plt.tight_layout()
    plt.show()

def get_irrigation_method(crop):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT method FROM irrigation WHERE crop_name = %s", (crop,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else None

def get_storage_advice(crop):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT storage_temp_celsius, storage_life_days, storage_condition
        FROM storage_advice WHERE crop_name = %s
    """, (crop,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if result:
        return {
            "temperature": result[0],
            "life days": result[1],
            "condition": result[2]
        }
    return None
