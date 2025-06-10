import requests 
import click 
import dotenv
import os

dotenv.load_dotenv()

def geocode(city: str, api_key: str) -> dict:
    """Fetches geocode data for a given city using OpenWeather API."""
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&appid={api_key}"

    response = requests.get(url)

    if response.status_code != 200:
        click.echo(f"Error fetching geocode data: {response.status_code}")
        return {}

    return response.json()

def get_weather_data(city:str, api_key:str) -> dict:
    """Fetches weather data for a given city using OpenWeather API.""" 
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url)

    if response.status_code != 200:
        click.echo(f"Error fetching weather data: {response.status_code}")
        return {}
    
    return response.json()

def get_air_quality(city: str, api_key:str) -> dict:
    """Fetches air quality data for a given city using OpenWeather API."""

    # Get geocode data to find the coordinates of the city
    geocode_data = geocode(city, api_key)

    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={geocode_data[0]['lat']}&lon={geocode_data[0]['lon']}&appid={api_key}"

    response = requests.get(url)
    if response.status_code != 200:
        click.echo(f"Error fetching air quality data: {response.status_code}")
        return {}
    return response.json()

def get_daily_forecast(city:str, api_key:str, number_of_days:int = 5) -> dict:
    """Fetches the forecasted weather for the next 16 days""" 

    geocode_data = geocode(city, api_key) 

    url= f"http://api.openweathermap.org/data/2.5/forecast?lat={geocode_data[0]['lat']}&lon={geocode_data[0]['lon']}&appid={api_key}"

    response = requests.get(url) 

    if response.status_code != 200:
        click.echo(f"Error fetching forecast data: {response.status_code}") 
        return {} 

    return response.json()

        
if __name__ == "__main__":

    API = os.getenv("API_KEY")

    response = get_daily_forecast("canberra", API)

    print(response)

 
