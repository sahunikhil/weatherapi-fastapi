# Weather API Service

## Overview

This FastAPI project provides a weather API service that asynchronously fetches weather data for a given city from external public APIs. It stores the fetched weather data as JSON files locally and logs the events in a MongoDB database. The service uses caching to reduce redundant API calls by storing weather data for each city for up to 5 minutes.

## Features

- **Asynchronous Data Fetching**: Fetches weather data asynchronously from external APIs using FastAPI and `httpx`.
- **Local JSON Storage**: Stores each weather response as a JSON file locally with the format `{city}_{timestamp}.json`.
- **MongoDB Integration**: Logs each API call event into MongoDB, including the city name, timestamp, and local file path.
- **Caching**: Implements a 5-minute cache for each city's weather data, avoiding repeated API calls within that time frame.
- **Error Handling**: Includes logging for exceptions to facilitate debugging.

**Note: This project doesn't need api keys, all the apis used doesn't need api keys. Enjoy <3!**

## Prerequisites

Before running the project, ensure you have the following installed:

- **Python 3.10+**
- **MongoDB** (locally or through Docker)
- **Docker** (if using Docker to run MongoDB)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/sahunikhil/weatherapi-fastapi.git
cd weatherapi-fastapi
```

### 2. Install Dependencies

Install all required Python dependencies from the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Running MongoDB

If you have Docker installed, you can run MongoDB using the provided `docker-compose.yml` file:

```bash
docker-compose up -d
```

This will start a MongoDB container with the credentials specified in the compose file (`admin/password`).

### 4. Running the Application

You can run the FastAPI application using `uvicorn`:

```bash
fastapi dev main.py
```

The service will be available at `http://127.0.0.1:8000`, and you can access the API documentation at `http://127.0.0.1:8000/docs`.

Here's the updated section for **Testing the `/weather` Endpoint** in the README, with the proper `curl` command:

---

### 5. Testing the `/weather` Endpoint

Once the FastAPI server is running (typically at `http://127.0.0.1:8000` by default), you can test the `/weather` endpoint by making a `GET` request with a city name as the query parameter.

#### Example cURL Request

To test the endpoint for the city "London", you can use the following `curl` command:

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/weather?city=London' \
  -H 'accept: application/json'
```

#### Sample Response
```json
{
  "latitude": 51.5073219,
  "longitude": -0.1276474,
  "generationtime_ms": 0.055789947509765625,
  "utc_offset_seconds": 0,
  "timezone": "GMT",
  "timezone_abbreviation": "GMT",
  "elevation": 11,
  "current_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature_2m": "°C",
    "rain": "mm",
    "showers": "mm",
    "snowfall": "cm"
  },
  "current": {
    "time": "2024-10-23T16:15",
    "interval": 900,
    "temperature_2m": 12.3,
    "rain": 0,
    "showers": 0,
    "snowfall": 0
  }
}
```

Replace the city name (`London`) with any other city of your choice to fetch its weather data.
## Project Structure

```bash
weatherapi-fastapi/
│
├── app/
│   ├── main.py          # Main FastAPI application logic
│   ├── utils.py         # Helper functions (e.g., for saving files)
├── data/                # Directory for locally stored JSON files
├── requirements.txt     # Python dependencies
├── Dockerfile           # Dockerfile for the FastAPI app
├── docker-compose.yml   # Docker Compose for MongoDB setup
└── README.md            # Project documentation
```

## Key Features and Code Details

- **Asynchronous Data Fetching**: The FastAPI app fetches data asynchronously from OpenMeteo API.
- **Local Storage**: Weather data is saved in the `./data` directory as `{city}_{timestamp}.json`.
- **MongoDB Logging**: Each weather data request is logged in a MongoDB collection, storing the city name, timestamp, and file path.
- **5-Minute Caching**: Before making an external API call, the app checks if the weather data for the requested city is already available and is less than 5 minutes old. If so, the cached data is returned.

## Example Response

```json
{
  "latitude": 26.625,
  "longitude": 82,
  "generationtime_ms": 0.03504753112792969,
  "utc_offset_seconds": 19800,
  "timezone": "Asia/Kolkata",
  "timezone_abbreviation": "IST",
  "elevation": 98,
  "current_units": {
    "time": "iso8601",
    "interval": "seconds",
    "temperature_2m": "°C",
    "rain": "mm",
    "showers": "mm",
    "snowfall": "cm"
  },
  "current": {
    "time": "2024-10-23T16:15",
    "interval": 900,
    "temperature_2m": 31.4,
    "rain": 0,
    "showers": 0,
    "snowfall": 0
  }
}
```

## Logging

The application logs any exceptions with details such as the function name, error type, error message, and where the error occurred. The logging function outputs detailed information for easier debugging.

## Deployment

The application can be deployed using Docker and Docker Compose, making it easy to set up MongoDB and the FastAPI app in containers. The provided configuration in the `docker-compose.yml` file includes everything needed to run both the MongoDB instance and the FastAPI service.

