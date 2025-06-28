CREATE DATABSE IF NOT EXISTS agrismart;
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

CREATE TABLE wether_data(
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
    crop_name VARCHAR(20) PRIMARY KEY,
    il_type VARCHAR(50),
    fertilizer_name VARCHAR(50),
    dosage_per_acre VARCHAR(50),
    PRIMARY KEY (crop_name, soil_type),
    FOREIGN KEY (crop_name) REFERENCES crops(crop_name)
);

