# AgriSmart

AgriSmart is an intelligent farm management system designed to help farmers plan, monitor, and analyze all aspects of crop production—from soil preparation and irrigation to market forecasting and yield tracking.

---

## Features

1. **Crop Season Planner** – Select suitable crops based on location and season.  
2. **Crop Rotation Optimizer** – Avoid soil exhaustion with smart crop cycles.  
3. **Irrigation Scheduler** – Efficient water usage based on crop and region.  
4. **Fertilizer Recommender** – Get soil-based, crop-specific fertilizer advice.  
5. **Machinery & Labor Estimator** – Based on crop type and land size.  
6. **Yield & Market Value Tracker** – Estimate income and historical trends.  
7. **Harvest & Storage Advisor** – Know when to harvest and how long you can store.  
8. **Analytics Dashboard** – View performance, weak areas, cost-efficiency, and visual reports.  
9. **MySQL Database** – Secure backend storage for all agricultural records.  
10. **Tkinter GUI** – User-friendly interface for local use.  
11. *(Optional)* **Flask-based web dashboard** for remote access.

---

## Tech Stack

| Component     | Technology                 |
|---------------|----------------------------|
| Backend       | Python + MySQL             |
| GUI           | Tkinter (local)            |
| Data Analysis | Pandas, Seaborn, Matplotlib|
| Web UI (opt.) | Flask + HTML/CSS           |
| Version Ctrl  | Git + GitHub               |

---

## Setup Instructions

```bash
# 1. Clone the repo
git clone https://github.com/KkriZh/AgriSmart.git
cd AgriSmart

# 2. Install dependencies
pip install -r requirements.txt

# 3. Setup database (MySQL)
# Run schema.sql in your MySQL client

# 4. Start the GUI
python gui.py
