# Flight Analytics App

A web application built with Reflex to analyze and visualize historical performance metrics for domestic flight routes within the USA. This tool provides insights into flight delays, cancellations, and on-time arrivals, complemented by real-time weather data for origin and destination airports.

## Key Features

*   **Route Performance Analysis**: Get statistics on flight performance between any two US domestic airports.
*   **Historical Data Querying**: Analyze data over various time horizons, from the last month up to the maximum available dataset range (since early 2018).
*   **Interactive Visualizations**:
    *   A pie chart breaks down flights into on-time, delayed, cancelled, and diverted categories.
    *   A network graph displays the total number of scheduled flights for the selected route.
*   **Real-time Weather Integration**: Fetches and displays current METAR (Meteorological Aerodrome Report) status for the origin and destination airports using the `aviationweather.gov` API.
*   **Intuitive UI**: A clean, responsive interface with an animated particle background, tooltips for weather category explanations, and a datalist for easy airport code selection.

## Technology Stack

*   **Full-Stack Framework**: [Reflex](https://reflex.dev/)
*   **Data Analysis Engine**: [DuckDB](https://duckdb.org/) for fast queries on Parquet files.
*   **Data Visualization**:
    *   [Recharts](https://recharts.org/) (via Reflex) for the pie chart.
    *   [Matplotlib](https://matplotlib.org/) & [NetworkX](https://networkx.org/) for generating the route graph.
*   **Styling**: Reflex's built-in components with a custom Tailwind V4 plugin.
*   **Background Animation**: [particles.js](https://vincentgarreau.com/particles.js/)

## Data Sources

*   **Historical Flight Data**: The application queries a local Parquet file (`combinedv2.parquet`) containing US domestic flight data from 2018 to mid-2025. **Note: This dataset is not included in the repository.**
*   **Airport Codes**: A local Parquet file (`iata-icao.parquet`) is used to convert IATA codes to ICAO codes for weather API requests.
*   **Weather Data**: Real-time METAR data is fetched from the [Aviation Weather Center API](https://aviationweather.gov/api).

## Local Setup and Installation

To run this application on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/sai-foss/Flight_Analytics_App.git
    cd Flight_Analytics_App
    ```

2.  **Install Dependencies**
    It is recommended to use a virtual environment.
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    pip install -r requirements.txt
    ```

3.  **Set Up Data File**
    This application requires a Parquet file with historical flight data.
    *   Obtain your flight data Parquet file.
    *   Open `Flight_Analytics_App/state.py`.
    *   Locate the `analyze` method and update the path to your dataset. For example, change `local_path` to the correct location on your system:
        ```python
        # In Flight_Analytics_App/state.py
        
        # ... inside the analyze method
        cloud_path = Path("/var/data/dataset_file.parquet")
        local_path = Path("/path/to/your/dataset_file.parquet") # <-- UPDATE THIS PATH
        path = ""
        # ...
        ```

4.  **Initialize and Run the Application**
    ```bash
    reflex init
    reflex run
    ```
    The application will be available at `http://localhost:3000`.

## Project Structure
```
.
├── Flight_Analytics_App/
│   ├── Flight_Analytics_App.py   # Main app entry point and page routing
│   ├── state.py                  # Core application logic, state management, and event handlers
│   ├── background/
│   │   ├── background.py         # Defines the page shell with the animated background
│   │   └── particles.py          # Configuration for particles.js
│   ├── components/
│   │   ├── cards.py              # UI card components for input, charts, and weather
│   │   └── gradients.py          # Helper functions for creating gradient borders
│   └── data/
│       ├── airport_list.py       # Manages the list of airport codes for the input datalist
│       ├── database.py           # Contains DuckDB queries for flight data analysis
│       ├── iata-icao.parquet     # Parquet file for IATA to ICAO code conversion
│       └── network_graph.py      # Generates the route network graph using Matplotlib
├── LICENSE
├── requirements.txt              # Python dependencies
└── rxconfig.py                   # Reflex application configuration
```

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
