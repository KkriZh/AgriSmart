CREATE DATABaSE IF NOT EXISTS agrismart;
use agrismart;
CREATE TABLE crops(
    crop_name VARCHAR(20) PRIMARY KEY,
    season VARCHAR(10),
    duration INT,
    soil VARCHAR(10),
    ideal_temp_min DECIMAL(5,2),
    ideal_temp_max DECIMAL(5,2),
    water_requirement VARCHAR(50)
);

CREATE TABLE soil_data(
    Soil_id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(20),
    fertility_level VARCHAR(20)
);

CREATE TABLE weather_data(
    wether_id INT PRIMARY KEY AUTO_INCREMENT,
    region VARCHAR(20),
    month VARCHAR(20),
    avg_temp DECIMAL(5,2),
    rainfall_mm DECIMAL(5,2)
);

CREATE TABLE irrigation(
    crop_name VARCHAR(20) PRIMARY KEY,
    method VARCHAR(20),
    FOREIGN KEY (crop_name) REFERENCES crops(crop_name)
);

CREATE TABLE fertilizers(
    crop_name VARCHAR(20),
    fertilizer_name VARCHAR(50),
    dosage_per_hectare INT,
    PRIMARY KEY (crop_name),
    FOREIGN KEY (crop_name) REFERENCES crops(crop_name)
);
CREATE TABLE yield_history(
    id INT PRIMARY KEY AUTO_INCREMENT,
    crop_name VARCHAR(50),
    region VARCHAR(50),
    year INT,
    yield_per_hectare DECIMAL(6,2),
    FOREIGN KEY (crop_name) REFERENCES crops(crop_name)
);

CREATE TABLE market_prices(
    crop_name VARCHAR(20) PRIMARY KEY,
    price_per_KG DECIMAL(6,2),
    FOREIGN KEY(crop_name) REFERENCES crops(crop_name)
);

CREATE TABLE storage_advice(
    crop_name VARCHAR(20) PRIMARY KEY,
    storage_temp_celsius Int,
    storage_life_days Int,
    storage_condition TEXT,
    FOREIGN KEY(crop_name) REFERENCES crops(crop_name)
);
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50),
    password VARCHAR(100),
    region VARCHAR(50)
);
