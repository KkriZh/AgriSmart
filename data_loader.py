from db import get_connection

def insert_data():
    conn = get_connection()
    if not conn:
        print("Failed to connect to database")
        return

    cursor = conn.cursor()

    try:
        crops_data = [
            ('Rice', 'Kharif', 135, 'Clayey', 20.0, 35.0, 'High'),
            ('Wheat', 'Rabi', 120, 'Loamy', 15.0, 25.0, 'Medium'),
            ('Maize', 'Kharif', 100, 'Sandy Loam', 21.0, 30.0, 'Medium'),
            ('Bajra', 'Kharif', 90, 'Sandy', 20.0, 35.0, 'Low'),
            ('Barley', 'Rabi', 110, 'Sandy Loam', 12.0, 25.0, 'Medium'),
            ('Sugarcane', 'Annual', 300, 'Alluvial', 20.0, 38.0, 'Very High'),
            ('Groundnut', 'Kharif', 105, 'Sandy Loam', 25.0, 35.0, 'Low'),
            ('Cotton', 'Kharif', 180, 'Black Soil', 20.0, 35.0, 'Medium'),
            ('Jowar', 'Kharif', 100, 'Sandy Loam', 25.0, 32.0, 'Medium'),
            ('Mustard', 'Rabi', 110, 'Loamy', 10.0, 25.0, 'Low'),
            ('Chickpea', 'Rabi', 100, 'Black Soil', 15.0, 30.0, 'Low'),
            ('Lentil', 'Rabi', 100, 'Alluvial', 10.0, 25.0, 'Low'),
            ('Soybean', 'Kharif', 95, 'Black Soil', 20.0, 30.0, 'Medium'),
            ('Sunflower', 'Zaid', 90, 'Sandy Loam', 20.0, 30.0, 'Medium'),
            ('Tur (Arhar)', 'Kharif', 150, 'Loamy', 20.0, 35.0, 'Low'),
            ('Moong', 'Kharif', 65, 'Sandy Loam', 25.0, 35.0, 'Low'),
            ('Onion', 'Rabi', 120, 'Sandy Loam', 13.0, 28.0, 'Medium'),
            ('Tomato', 'Zaid', 90, 'Loamy', 20.0, 30.0, 'Medium'),
            ('Potato', 'Rabi', 110, 'Sandy Loam', 10.0, 25.0, 'Medium'),
            ('Peas', 'Rabi', 80, 'Loamy', 12.0, 22.0, 'Low')
        ]

        cursor.executemany("""
            INSERT INTO crops (
                crop_name, season, duration, soil,
                ideal_temp_min, ideal_temp_max, water_requirement
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, crops_data)
        
        soil_data = [
            ('Alluvial', 'High'),
            ('Black Soil', 'High'),
            ('Red Soil', 'Medium'),
            ('Laterite', 'Low'),
            ('Sandy', 'Low'),
            ('Loamy', 'High'),
            ('Clayey', 'Medium'),
            ('Sandy Loam', 'Medium'),
            ('Peaty', 'Low'),
            ('Marshy', 'Low')
        ]
        cursor.executemany("""
            INSERT INTO soil_data (type, fertility_level)
            VALUES (%s, %s)
            """, soil_data)

        weather_data = [
            ('Punjab', 'June', 35.2, 120.5),
            ('Punjab', 'July', 33.4, 210.2),
            ('Punjab', 'August', 31.0, 185.0),
            ('Punjab', 'September', 29.5, 160.0),

            ('Bihar', 'June', 34.0, 100.0),
            ('Bihar', 'July', 32.0, 190.0),
            ('Bihar', 'August', 30.0, 170.0),
            ('Bihar', 'September', 29.0, 130.0),

            ('Maharashtra', 'June', 32.0, 150.0),
            ('Maharashtra', 'July', 30.0, 300.0),
            ('Maharashtra', 'August', 28.5, 250.0),
            ('Maharashtra', 'September', 27.0, 200.0),

            ('Tamil Nadu', 'June', 36.5, 70.0),
            ('Tamil Nadu', 'July', 35.0, 90.0),
            ('Tamil Nadu', 'August', 34.0, 85.0),
            ('Tamil Nadu', 'September', 33.0, 100.0),

            ('Uttar Pradesh', 'June', 34.5, 110.0),
            ('Uttar Pradesh', 'July', 32.5, 170.0),
            ('Uttar Pradesh', 'August', 31.5, 150.0),
            ('Uttar Pradesh', 'September', 30.0, 120.0)
        ]
        cursor.executemany("""
            INSERT INTO weather_data (region, month, avg_temp, rainfall_mm)
            VALUES (%s, %s, %s, %s)
            """, weather_data)


        irrigation_data = [
            ('Rice', 'Flood'),
            ('Wheat', 'Sprinkler'),
            ('Maize', 'Drip'),
            ('Bajra', 'Sprinkler'),
            ('Barley', 'Sprinkler'),
            ('Sugarcane', 'Furrow'),
            ('Groundnut', 'Drip'),
            ('Cotton', 'Drip'),
            ('Jowar', 'Sprinkler'),
            ('Mustard', 'Sprinkler'),
            ('Chickpea', 'Sprinkler'),
            ('Lentil', 'Sprinkler'),
            ('Soybean', 'Drip'),
            ('Sunflower', 'Sprinkler'),
            ('Tur (Arhar)', 'Sprinkler'),
            ('Moong', 'Sprinkler'),
            ('Onion', 'Furrow'),
            ('Tomato', 'Drip'),
            ('Potato', 'Sprinkler'),
            ('Peas', 'Sprinkler')
        ]

        cursor.executemany("""
            INSERT INTO irrigation (crop_name, method)
            VALUES (%s, %s)
        """, irrigation_data)

        fertilizer_data = [
            ('Rice', 'Urea', 100),
            ('Wheat', 'DAP', 90),
            ('Maize', 'NPK 20:20:0', 80),
            ('Bajra', 'Urea', 70),
            ('Barley', 'Super Phosphate', 65),
            ('Sugarcane', 'NPK 12:32:16', 250),
            ('Groundnut', 'Gypsum', 40),
            ('Cotton', 'Potash', 120),
            ('Jowar', 'Urea', 75),
            ('Mustard', 'Sulphur', 60),
            ('Chickpea', 'Single Super Phosphate', 55),
            ('Lentil', 'MOP', 45),
            ('Soybean', 'Urea', 85),
            ('Sunflower', 'Zinc Sulphate', 70),
            ('Tur (Arhar)', 'DAP', 60),
            ('Moong', 'Rhizobium', 50),
            ('Onion', 'NPK 10:26:26', 90),
            ('Tomato', 'Compost', 80),
            ('Potato', 'Potash', 100),
            ('Peas', 'Urea', 60)
        ]
        
        cursor.executemany("""
            INSERT INTO fertilizers(crop_name, fertilizer_name, dosage_per_hectare)
            VALUES (%s, %s,%s)
        """, fertilizer_data)

        yield_history = [
            ('Rice', 'Punjab', 2022, 2500.50),
            ('Rice', 'Punjab', 2023, 2550.75),
            ('Wheat', 'Uttar Pradesh', 2022, 3000.00),
            ('Wheat', 'Uttar Pradesh', 2023, 3100.00),
            ('Maize', 'Maharashtra', 2022, 2800.25),
            ('Maize', 'Maharashtra', 2023, 2850.40),
            ('Bajra', 'Rajasthan', 2022, 1800.00),
            ('Bajra', 'Rajasthan', 2023, 1850.00),
            ('Barley', 'Haryana', 2022, 2400.10),
            ('Barley', 'Haryana', 2023, 2500.30),
            ('Sugarcane', 'Uttar Pradesh', 2022, 60000.00),
            ('Sugarcane', 'Uttar Pradesh', 2023, 62000.00),
            ('Groundnut', 'Gujarat', 2022, 2000.00),
            ('Groundnut', 'Gujarat', 2023, 2100.00),
            ('Cotton', 'Maharashtra', 2022, 1800.00),
            ('Cotton', 'Maharashtra', 2023, 1850.00),
            ('Jowar', 'Karnataka', 2022, 1700.00),
            ('Jowar', 'Karnataka', 2023, 1750.00),
            ('Mustard', 'Rajasthan', 2022, 1200.00),
            ('Mustard', 'Rajasthan', 2023, 1250.00),
            ('Chickpea', 'Madhya Pradesh', 2022, 1500.00),
            ('Chickpea', 'Madhya Pradesh', 2023, 1550.00),
            ('Lentil', 'Bihar', 2022, 1400.00),
            ('Lentil', 'Bihar', 2023, 1450.00),
            ('Soybean', 'Madhya Pradesh', 2022, 2200.00),
            ('Soybean', 'Madhya Pradesh', 2023, 2250.00),
            ('Sunflower', 'Andhra Pradesh', 2022, 1600.00),
            ('Sunflower', 'Andhra Pradesh', 2023, 1650.00),
            ('Tur (Arhar)', 'Maharashtra', 2022, 1300.00),
            ('Tur (Arhar)', 'Maharashtra', 2023, 1350.00),
            ('Moong', 'Telangana', 2022, 1000.00),
            ('Moong', 'Telangana', 2023, 1050.00),
            ('Onion', 'Maharashtra', 2022, 20000.00),
            ('Onion', 'Maharashtra', 2023, 21000.00),
            ('Tomato', 'Karnataka', 2022, 25000.00),
            ('Tomato', 'Karnataka', 2023, 25500.00),
            ('Potato', 'Punjab', 2022, 30000.00),
            ('Potato', 'Punjab', 2023, 31000.00),
            ('Peas', 'Himachal Pradesh', 2022, 1200.00),
            ('Peas', 'Himachal Pradesh', 2023, 1250.00)
        ]
        cursor.executemany("""
            INSERT INTO yield_history (crop_name, region, year, yield_per_hectare)
            VALUES (%s, %s, %s, %s)
        """, yield_history)

        market_prices = [
            ('Rice', 25),
            ('Wheat', 22),
            ('Maize', 18),
            ('Bajra', 20),
            ('Barley', 21),
            ('Sugarcane', 3),
            ('Groundnut', 45),
            ('Cotton', 60),
            ('Jowar', 20),
            ('Mustard', 55),
            ('Chickpea', 50),
            ('Lentil', 55),
            ('Soybean', 40),
            ('Sunflower', 48),
            ('Tur (Arhar)', 75),
            ('Moong', 65),
            ('Onion', 15),
            ('Tomato', 20),
            ('Potato', 12),
            ('Peas', 50)
        ]
        cursor.executemany("""
            INSERT INTO  market_prices(crop_name, price_per_KG)
            VALUES (%s, %s)
        """, market_prices)

        storage_advice = [
            ('Rice', 25, 365, 'Cool, dry place in jute bags'),
            ('Wheat', 25, 365, 'Well-ventilated dry space'),
            ('Maize', 24, 180, 'Low moisture bins'),
            ('Bajra', 26, 180, 'Airtight containers'),
            ('Barley', 24, 270, 'Dry storage in silos'),
            ('Sugarcane', 10, 3, 'Freshly used, no long-term storage'),
            ('Groundnut', 18, 120, 'Cool, low humidity rooms'),
            ('Cotton', 22, 365, 'Dry covered godown'),
            ('Jowar', 25, 180, 'Sealed gunny bags'),
            ('Mustard', 20, 150, 'Low moisture, pest-free place'),
            ('Chickpea', 25, 180, 'Ventilated bins'),
            ('Lentil', 25, 180, 'Dry and airtight containers'),
            ('Soybean', 22, 150, 'Cool dry warehouse'),
            ('Sunflower', 20, 120, 'No exposure to direct sun'),
            ('Tur (Arhar)', 25, 180, 'Closed dry bins'),
            ('Moong', 25, 120, 'Avoid humid environments'),
            ('Onion', 10, 60, 'Dry, netted bags, no water contact'),
            ('Tomato', 7, 14, 'Cool storage, not freezing'),
            ('Potato', 4, 120, 'Cold storage, avoid sprouting'),
            ('Peas', 4, 10, 'Frozen or refrigerated packs')
        ]
        cursor.executemany("""
            INSERT INTO  storage_advice(crop_name,storage_temp_celsius, storage_life_days,storage_condition )
            VALUES (%s, %s,%s,%s)
        """, storage_advice)

        conn.commit()

    except Exception as e:
        conn.rollback()
        print("Error inserting data:", e)

    finally:
        cursor.close()
        conn.close()
