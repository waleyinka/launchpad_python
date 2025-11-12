# 🏙 Airbnb Data Deep Dive – Python + Pandas Challenge

## 📖 Overview
This project explores Airbnb listing data for **London** and **New York City** using Python and Pandas.  
It’s designed as a practical data-cleaning and analysis exercise — transforming messy real-world data into actionable insights.

The workflow follows a **data engineering mindset**: load raw data, clean it systematically, enrich it with useful features, and perform analytical queries directly in Pandas.

---

## 🧩 Objectives
- Practice **data wrangling** and cleaning using Pandas.
- Build a reproducible data-cleaning pipeline.
- Derive insights about **pricing, availability, and host behavior**.
- Learn to manage raw and cleaned datasets within a structured project directory.

---

## 🗂 Project Structure
```bash
airbnb/
│
├── london.csv
├── new_york.csv
│
├── data/
│ ├── london_cleaned.csv
│ └── nyc_cleaned.csv
│
├── london.ipynb
├── new_york.ipynb
└── README.md
```

---

## ⚙️ Setup Instructions

### 1. Create and activate a virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate     # macOS/Linux
venv\Scripts\activate        # Windows
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

### 3. Launch Jupyter Notebook
```bash
jupyter notebook
```

---

## 📥 Data Loading

Download datasets directly from [Inside Airbnb](http://insideairbnb.com/get-the-data.html).

Example using `wget` (inside your Jupyter cell or terminal):

```bash
!wget https://data.insideairbnb.com/united-kingdom/england/london/2024-06-01/data/listings.csv -O london.csv
```

Then load into pandas:

```python
import pandas as pd
df_raw = pd.read_csv("london.csv")
```

---

## 🧹 Data Cleaning
Work on a copy of the raw dataset to keep it immutable:

```python
df_clean = df_raw.copy()
```

**Cleaning steps:**

 - Convert price fields from strings ("$2,100.00") to float.

 - Parse last_review as datetime.

 - Handle missing values in reviews_per_month, host_name, and neighbourhood_group.

 - Remove rows with zero or invalid price or availability_365.

 - Save the cleaned dataset:

```python
import os
os.makedirs("data", exist_ok=True)
df_clean.to_csv("data/london_cleaned.csv", index=False)
```

---

## ✨ Data Enrichment

Enhance your dataset with additional derived features:

| **Column**                | **Description**                                                     |
| :-------------------- | :-------------------------------------------------------------- |
| `price_per_booking`   | `price / minimum_nights`, rounded to 2 decimals                 |
| `availability_bucket` | Categorical: Full-time (>300), Part-time (100–300), Rare (<100) |

```python
df_clean['price_per_booking'] = (df_clean['price'] / df_clean['minimum_nights']).replace([float('inf'), -float('inf')], None).round(2)

def categorize(x):
    if x > 300: return 'Full-time'
    elif 100 <= x <= 300: return 'Part-time'
    else: return 'Rare'

df_clean['availability_bucket'] = df_clean['availability_365'].apply(categorize)
```

---

## 📊 Analysis Questions

 1. Top 10 most expensive neighborhoods by average price

 2. Average availability and price by room type

 3. Host with the most listings

 4. Average price variation across boroughs/districts

 5. Listings that have never been reviewed

**Example Queries**

```python
# 1. Most expensive neighborhoods
df_clean.groupby('neighbourhood', as_index=False) \
  .agg(avg_price=('price', 'mean')) \
  .sort_values(by='avg_price', ascending=False) \
  .head(10)

# 2. Average availability & price by room type
df_clean.groupby('room_type', as_index=False) \
  .agg(avg_price=('price', 'mean'), avg_availability=('availability_365', 'mean'))

# 3. Host with most listings
df_clean['host_name'].value_counts().head(1)
```

---

## 🧠 Key Insights (Example Results)

**London**
| **Metric**                         | **Insight**                          |
| ------------------------------ | -------------------------------- |
| Most Expensive Neighbourhood   | **Tower Hamlets** – avg. £434.84 |
| Highest-Priced Room Type       | **Hotel room** – avg. £694.91    |
| Never Reviewed                 | 13,714 listings (~22%)           |
| Price–Availability Correlation | 0.01 (very weak)                 |

**New York**
| **Metric**                         | **Insight**                                      |
| ------------------------------ | -------------------------------------------- |
| Most Expensive Neighbourhood   | **SoHo** – avg. $3,418.54                    |
| Highest-Priced Room Type       | **Hotel room** – avg. $36,431.21             |
| Borough Range                  | Manhattan ~1,182.95 vs Staten Island ~125.56 |
| Never Reviewed                 | 6,343 listings (~30%)                        |
| Price–Availability Correlation | 0.04 (weak positive)                         |

---

## 🪜 Reproducibility Checklist

 - Always work on a copy: df_clean = df_raw.copy()
 - Save cleaned data to data/ before clearing the kernel
 - Use relative paths (data/london_cleaned.csv)
 - Check your working directory using os.getcwd()
 - Keep your cleaning and analysis code in separate notebook sections

---

## 🧩 License

This project is for educational and analytical purposes using publicly available Airbnb data from [Inside Airbnb](http://insideairbnb.com/get-the-data.html).
All dataset rights remain with their respective owners.