# Agricultural Market Price Dashboard

A Streamlit-based interactive dashboard for exploring agricultural commodity prices across Indian states using AGMARKNET market data.
## Live Demo

[Open Website](https://appdashboard-jtabfikst7jkp7kunt2kef.streamlit.app/)
## Features

* State-wise and commodity-wise filtering
* Summary KPI cards:

  * Total Records
  * Unique States
  * Unique Commodities
  * Average Modal Price
* Top commodities by average price
* State-wise average price comparison
* Commodity price spread analysis
* Download filtered data as CSV
* State-to-state commodity price comparison (Bonus)
* Custom Streamlit theme using `.streamlit/config.toml`

## Dataset

Source:

AGMARKNET, Ministry of Agriculture & Farmers Welfare, Government of India

The dataset contains:

* State
* District
* Market
* Commodity
* Variety
* Grade
* Arrival Date
* Minimum Price
* Maximum Price
* Modal Price

## Installation

Install the required packages:

```bash
pip install streamlit pandas plotly
```

## Running the App

```bash
streamlit run dashboard.py
```

The application will open automatically in your browser:

```text
http://localhost:8501
```

## Dashboard Structure

### Sidebar Filters

* State filter
* Commodity filter
* Price type selector
* State comparison mode

### KPI Cards

* Total records
* States covered
* Commodities available
* Average modal price

### Visualizations

#### Top Commodities by Average Price

Displays the highest priced commodities based on average modal price.

#### Average Price by State

Compares commodity prices across states.

#### Price Spread Analysis

Shows commodities with the highest difference between minimum and maximum market prices.

#### State Comparison (Bonus)

Compare two states for a selected commodity and determine which state has lower prices.

Example:

> Is Onion cheaper in Maharashtra or Uttar Pradesh today?

### Data Table

Filtered data can be viewed and downloaded as CSV.

## References

Streamlit Cheat Sheet

https://docs.streamlit.io/develop/quick-reference/cheat-sheet

Streamlit Tutorial

https://docs.streamlit.io/get-started/tutorials/create-an-app

Streamlit Theming

https://docs.streamlit.io/develop/concepts/configuration/theming

Streamlit Community Cloud

https://docs.streamlit.io/deploy/streamlit-community-cloud

## Project Structure

```text
.
├── .streamlit
│   └── config.toml
├── agri_market_prices.csv
├── dashboard.py
├── README.md
└── .gitignore
```

## Bonus Features Implemented

* State comparison mode
* Custom dashboard theme
* Enhanced chart styling
* Downloadable filtered dataset
## About This Project

This project was developed as part of a Streamlit dashboard exercise using agricultural market price data from AGMARKNET.

The dashboard implementation in `dashboard.py` was independently built by referring to the Streamlit documentation, tutorial material, and exercise requirements. The application structure, filtering logic, visualizations, dashboard layout, theming, and additional features were implemented and customized during development.

The repository also contains `app.py`, which is and should be created without AI and can be used as a separate learning and experimentation file while exploring Streamlit concepts and components.

## Learning References

The following resources were used during development:

* Streamlit Cheat Sheet
  https://docs.streamlit.io/develop/quick-reference/cheat-sheet

* Streamlit Create an App Tutorial
  https://docs.streamlit.io/get-started/tutorials/create-an-app

* Streamlit Theming Documentation
  https://docs.streamlit.io/develop/concepts/configuration/theming

These resources were used as references while designing and implementing the dashboard rather than as direct copies of a complete solution.

## Author Notes

The dashboard was developed using an iterative "vibe coding" approach—building features, testing ideas, refining visualizations, and improving usability step by step. Several enhancements beyond the core exercise requirements were added, including:

* State-to-state commodity comparison
* Custom dashboard styling and theming
* Improved chart presentation
* Enhanced filtering workflow
* CSV export functionality

The final application represents a practical exploration of Streamlit, data visualization, and dashboard development using Python.

## Author

Muthuraman
