# 🏎️ Fanalytics

**Fanalytics** is a modern Formula 1 analytics platform that combines historical statistics, interactive dashboards, and machine learning concepts to provide a data-driven view of the sport.

The project is designed to serve as both an analytics application and a learning platform for data engineering, visualization, and predictive modeling.

---

## Features

### Dashboard

* Live-style overview of the Formula 1 season
* Driver and constructor standings
* Race calendar and event information
* Summary statistics and key metrics

### Driver Explorer

* Detailed driver profiles
* Career statistics
* Race starts, wins, podiums, and championship information
* Search, filtering, and sorting capabilities

### Team Explorer

* Constructor profiles
* Team performance statistics
* Historical achievements
* Driver associations

### Circuit Explorer

* Circuit information and specifications
* Track length and corner count
* Historical race statistics
* Interactive track cards

### Data Visualizations

* Championship progression
* Comparative statistics
* Historical trends
* Performance summaries

### Race Simulator *(Work in Progress)*

* Predict finishing positions based on configurable race conditions
* Inputs such as driver, constructor, track, weather, tyre strategy, and grid position
* Planned machine learning integration

---

## Project Architecture

```text
                 Data Sources
                      │
                      ▼
          Python Data Processing Pipeline
                      │
          JSON Generation & Validation
                      │
                      ▼
              Static JSON Data Files
                      │
                      ▼
             React + TypeScript Frontend
                      │
                      ▼
              Responsive Web Dashboard
```

The frontend consumes locally generated JSON files rather than querying external APIs directly, providing:

* Faster page loads
* Consistent data representation
* Easier deployment
* Simplified caching
* Separation between data ingestion and presentation

---

## Technology Stack

### Frontend

* React
* TypeScript
* Vite
* Tailwind CSS

### Data Processing

* Python
* Pandas
* Jupyter Notebooks

### Future Machine Learning

* Scikit-learn
* Random Forests
* Neural Networks
* Feature Engineering for race prediction

### Deployment

* GitHub
* Vercel

---

## Repository Structure

```text
src/
  components/
  pages/
  services/
  types/

public/
  data/
  images/
    drivers/
    teams/
    tracks/

python_scripts/
  data_generation/
  image_download/
  update_scripts/
```

---

## Development Roadmap

* [x] React frontend foundation
* [x] Responsive page structure
* [x] JSON-based data architecture
* [x] Driver, team, and circuit pages
* [ ] Automated data ingestion pipeline
* [ ] Historical statistics generation
* [ ] Interactive visualizations
* [ ] Race simulation engine
* [ ] Machine learning prediction models
* [ ] Scheduled update automation

---

## Vision

Fanalytics aims to demonstrate how software engineering, data pipelines, visualization, and machine learning can be applied to Formula 1 analytics while maintaining a modular and maintainable architecture.

The project emphasizes reproducible data processing, clean frontend design, and extensibility for future analytical features.

---

## License

This project is intended for educational and portfolio purposes. Users should verify the licensing and terms of use for any external datasets, APIs, or media assets incorporated into the project.
