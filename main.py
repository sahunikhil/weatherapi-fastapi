from fastapi import FastAPI

import httpx
import datetime
import traceback
import aiofiles
import os
import json
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI()

STORAGE = "./data/"
DB_CONNECTION = "mongodb://admin:password@localhost:27017"

# Connect to MongoDB
client = AsyncIOMotorClient(DB_CONNECTION)
db = client.weatherapidb
log_collection = db.logs

async def save_file_locally(city: str, content: dict):
    try:
        full_path = os.path.join(STORAGE, f"{city}_{datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")}.json")
        os.makedirs(STORAGE, exist_ok=True)
        json_string = json.dumps(content, indent=4)
        async with aiofiles.open(full_path, 'w') as file:
            await file.write(json_string)
        return full_path
    except Exception as e:
        print(log_exception("save_file_locally", e))


def log_exception(func_name: str, exception: Exception):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_type = type(exception).__name__
    error_message = str(exception)
    tb = traceback.extract_tb(exception.__traceback__)
    last_trace = tb[-1]
    log_line = (
        f"[{current_time}] ERROR in function '{func_name}' at "
        f"{last_trace.filename}, line {last_trace.lineno}: "
        f"{error_type} - {error_message}"
    )
    return log_line


# Function to get latitude and longitude using Nominatim
async def get_lat_lon(city: str):
    try:
        url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"

        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
        if data:
            print(data)
            print(data[0]["lat"], data[0]["lon"])
            return data[0]["lat"], data[0]["lon"]
        return None, None
    except Exception as e:
        print(log_exception("get_lat_lon", e))
       

@app.get("/weather")
async def get_weather(city: str):
    try:
        # Check if latest file stored is not more than 5 min late
        files = [os.path.join(STORAGE, f) for f in os.listdir(STORAGE)if os.path.isfile(os.path.join(STORAGE, f))]
        if files:
            latest_file = max(files, key=os.path.getmtime)
            if (latest_file.split("_")[0] == city) and ((datetime.datetime.now() - datetime.datetime.strptime(latest_file.split("_")[1], "%Y-%m-%dT%H:%M:%S")) <= datetime.timedelta(minutes=5)):
                async with aiofiles.open(latest_file, 'r') as f:
                    json_string = await f.read()
                    return json.loads(json_string)
            
        # Get latitude and longitude using Nominatim
        lat, lon = await get_lat_lon(city)
        if lat is None or lon is None:
            return {"error": "Failed to get latitude and longitude."}

        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,rain,showers,snowfall&timezone=auto&forecast_days=1"
            )
            weather_data = response.json()
        if weather_data:
            print(weather_data)
            # Save weather data locally
            file_path = await save_file_locally(city=city, content=weather_data)
            #  log the event in MongoDB table 
            await log_collection.insert_one({'city': city, 'timestamp': datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), 'file_path': file_path})
            return weather_data
        return {"error": "Failed to get weather data."}
    except Exception as e:
        print(log_exception("get_weather", e))
