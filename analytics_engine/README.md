# 🏎️ Fanalytics Data Engine

<div align="center">

### **The analytics engine powering the Fanalytics Formula 1 dashboard**

*A production-style ETL pipeline that transforms two decades of Formula 1 race data into intelligent driver and circuit analytics.*

<br>

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Pandas](https://img.shields.io/badge/Pandas-Data_Engineering-150458?logo=pandas)
![FastF1](https://img.shields.io/badge/FastF1-Jolpica_API-red)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-success?logo=github-actions)
![License](https://img.shields.io/badge/Status-Active-success)

</div>

---

# 📖 Overview

The **Fanalytics Data Engine** is a standalone analytics backend responsible for collecting, processing, engineering, and exporting Formula 1 race intelligence for the **Fanalytics React Dashboard**.

Rather than displaying raw statistics such as championship standings or race results, the engine derives contextual performance metrics from historical race data spanning **2006 to the present**, generating lightweight JSON datasets optimized for frontend consumption.

The entire pipeline is fully automated through **GitHub Actions**, allowing new race weekends to be reflected in the dashboard without manual intervention.

---

# ✨ Key Features

- 🏁 Historical Formula 1 Data Lake (2006–Present)
- ⚡ Automated ETL Pipeline
- 📈 Dynamic Driver & Team Momentum Ratings
- 🧠 Driver Racecraft Analytics
- 🛞 Circuit Fingerprinting
- 🏎️ Tire Degradation Modeling
- 🎯 Driver–Track Mastery Matrix
- 📦 JSON API Generation for React
- ☁️ Weekly Cloud Automation using GitHub Actions
- 🔄 Incremental Race Updates via Jolpica API

---

# 🏗️ System Architecture

```text
                 Historical Formula 1 Database
                 (Kaggle + Ergast/Jolpica)
                           │
                           ▼
                 Data Ingestion Layer
                           │
                           ▼
              master_historical.csv
                           │
          ┌────────────────┼────────────────┐
          ▼                ▼                ▼
 Track Profiles      Power Ratings      Mastery Matrix
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  JSON Export Builder
                           │
                           ▼
                 insights.json
                 tracks.json
                           │
                           ▼
              React / Next.js Dashboard
                           │
                           ▼
                 GitHub Actions Pipeline
                           │
                           ▼
                 Automatic Weekly Updates
```

---

# ⚙️ Data Pipeline

The engine executes every processing stage in chronological order.

```text
Raw Formula 1 Database
        │
        ▼
Bootstrap Historical Dataset
        │
        ▼
Bridge Missing Seasons
        │
        ▼
Generate Track Profiles
        │
        ▼
Generate Dynamic Power Ratings
        │
        ▼
Generate Driver Mastery Matrix
        │
        ▼
Build JSON Exports
        │
        ▼
React Dashboard
```

---

# 📂 Project Structure

```text
analytics_engine/
│
├── .github/
│   └── workflows/
│       └── analytics_pipeline.yml
│
├── data/
│   ├── raw/
│   ├── cache/
│   ├── features/
│   └── export/
│
├── src/
│   │
│   ├── ingestion/
│   │   ├── bootstrap.py
│   │   ├── bridge_seasons.py
│   │   └── update.py
│   │
│   ├── features/
│   │   ├── track_profile.py
│   │   ├── power_ratings.py
│   │   └── mastery.py
│   │
│   └── export/
│       └── json_builder.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

# 🧠 Analytics Engine

## 📈 Dynamic Power Ratings

The engine estimates current driver and constructor performance using an **Exponential Moving Average (EMA)** over the previous ten races.

### Features Generated

- Driver Momentum
- Constructor Momentum
- Driver Racecraft Index
- Positions Gained
- Time-decayed performance weighting

### Preventing Data Leakage

Every rolling calculation applies:

```python
.shift(1)
```

This ensures that every prediction only uses information available **before** the current race.

---

## 🏁 Track Fingerprinting

Every Formula 1 circuit receives its own engineered profile.

### Tire Degradation Index

Historical pit stop frequency is used as a proxy for tyre wear.

Using

```python
pd.qcut()
```

tracks are divided into five degradation categories:

| Index | Interpretation |
|---------|---------------|
| 1 | Very Low Degradation |
| 2 | Low |
| 3 | Medium |
| 4 | High |
| 5 | Very High |

### Circuit Classification

Each circuit is classified as:

- Permanent Circuit
- Street Circuit

This provides contextual information for later driver analysis.

---

## 🧠 Driver–Track Mastery Matrix

Rather than assuming every circuit suits every driver equally, the engine learns driver performance across different track characteristics.

If historical information is unavailable, the engine performs hierarchical fallback:

```text
Track History
      │
      ▼
Street Circuit History
      │
      ▼
Career Average
      │
      ▼
Grid Midpoint (10.5)
```

This prevents missing values while preserving realistic estimates.

---

# 📦 JSON Export Layer

The engineered feature datasets are converted into frontend-friendly JSON objects.

Generated outputs include:

```text
insights.json

tracks.json
```

These files are directly consumed by the React application without requiring a dedicated backend server.

---

# ☁️ Cloud Automation

The entire pipeline is deployed using **GitHub Actions**.

Every Monday the workflow automatically:

- 🚀 Creates a fresh Ubuntu runner
- 🐍 Installs Python
- 📦 Installs dependencies
- 📥 Updates historical race data
- ⚙️ Rebuilds every engineered feature
- 📄 Regenerates JSON exports
- ✅ Commits changes
- ☁️ Pushes updates back to GitHub

No manual intervention is required.

---

# 🔄 Weekly Workflow

```text
Monday (08:00 UTC)

        │

        ▼

GitHub Actions Runner

        │

        ▼

Fetch Latest Race Data

        │

        ▼

Update Historical Database

        │

        ▼

Generate Engineered Features

        │

        ▼

Export JSON Files

        │

        ▼

Commit Changes

        │

        ▼

Push to Repository

        │

        ▼

React Dashboard Updates
```

---

# 🚀 Getting Started

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/<username>/fanalytics.git

cd fanalytics/analytics_engine
```

---

## 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 3️⃣ Build the Historical Dataset (First-Time Setup)

Place the historical Formula 1 CSV files inside:

```text
analytics_engine/data/raw/
```

Then run:

```bash
python src/ingestion/bootstrap.py

python src/ingestion/bridge_seasons.py
```

---

## 4️⃣ Execute the Complete Pipeline

```bash
python main.py
```

The orchestrator automatically:

- Updates race data
- Generates engineered features
- Exports JSON files
- Prepares data for the React frontend

---

# 🛠️ Technology Stack

| Category | Technologies |
|-----------|--------------|
| Programming Language | Python 3.11 |
| Data Processing | Pandas |
| Formula 1 APIs | FastF1, Jolpica (Ergast) |
| Data Storage | CSV Data Lake |
| Feature Engineering | Pandas, NumPy |
| Automation | GitHub Actions |
| Export Format | JSON |
| Frontend Consumer | React + TypeScript |
| Deployment | GitHub + Vercel |

---

# 📈 Engineered Outputs

| Output | Description |
|---------|-------------|
| `master_historical.csv` | Unified historical Formula 1 database |
| `track_profiles.csv` | Circuit fingerprints and tyre degradation metrics |
| `power_ratings.csv` | Driver and constructor momentum metrics |
| `mastery_matrix.csv` | Driver suitability across circuit types |
| `insights.json` | Driver analytics for the frontend |
| `tracks.json` | Track analytics for the frontend |

---

# 🎯 Future Improvements

- 🤖 Machine Learning race outcome prediction
- 🛞 Tyre strategy recommendation engine
- 🌦️ Weather-aware race simulations
- 📊 Driver similarity clustering
- 🏆 Constructor performance forecasting
- 📡 Live telemetry integration
- 🌐 REST API
- 🗄️ PostgreSQL Data Warehouse
- 🐳 Dockerized deployment

---

# 📜 License

This project is intended for educational, research, and portfolio purposes.

Formula 1 data originates from publicly available historical datasets together with the Jolpica (formerly Ergast) API.

---

<div align="center">

### 🏎️ Built for Formula 1 fans who want to understand **why** races are won—not just **who** won them.

⭐ If you found this project interesting, consider giving it a star!

</div>