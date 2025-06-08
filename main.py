import click
from time import sleep
from datetime import datetime
import requests 
import os 
import dotenv
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.text import Text
import readchar
from google import genai

# Load environment variables from .env file
dotenv.load_dotenv()

console = Console()

openweather_aqi_scale_by_index = {
    1: {
        "qualitative_name": "Good",
        "description": "Air quality is considered satisfactory, and air pollution poses little or no risk.",
        "pollutant_ranges_ug_m3": {
            "SO2": "[0; 20)",
            "NO2": "[0; 40)",
            "PM10": "[0; 20)",
            "PM2.5": "[0; 10)",
            "O3": "[0; 60)",
            "CO": "[0; 4400)"
        },
        "health_advisory": "None."
    },
    2: {
        "qualitative_name": "Fair",
        "description": "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.",
        "pollutant_ranges_ug_m3": {
            "SO2": "[20; 80)",
            "NO2": "[40; 70)",
            "PM10": "[20; 50)",
            "PM2.5": "[10; 25)",
            "O3": "[60; 100)",
            "CO": "[4400; 9400)"
        },
        "health_advisory": "Unusually sensitive people should consider limiting prolonged or heavy exertion outdoors."
    },
    3: {
        "qualitative_name": "Moderate",
        "description": "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
        "pollutant_ranges_ug_m3": {
            "SO2": "[80; 250)",
            "NO2": "[70; 150)",
            "PM10": "[50; 100)",
            "PM2.5": "[25; 50)",
            "O3": "[100; 140)",
            "CO": "[9400-12400)"
        },
        "health_advisory": "People with lung disease (such as asthma), children, older adults, and people who are active outdoors should reduce prolonged or heavy exertion. Everyone else should limit prolonged or heavy exertion."
    },
    4: {
        "qualitative_name": "Poor",
        "description": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.",
        "pollutant_ranges_ug_m3": {
            "SO2": "[250; 350)",
            "NO2": "[150; 200)",
            "PM10": "[100; 200)",
            "PM2.5": "[50; 75)",
            "O3": "[140; 180)",
            "CO": "[12400; 15400)"
        },
        "health_advisory": "People with lung disease (such as asthma), children, older adults, and people who are active outdoors should avoid prolonged or heavy exertion. Everyone else should reduce prolonged or heavy exertion."
    },
    5: {
        "qualitative_name": "Very Poor",
        "description": "Health warnings of emergency conditions. The entire population is more likely to be affected.",
        "pollutant_ranges_ug_m3": {
            "SO2": "⩾350",
            "NO2": "⩾200",
            "PM10": "⩾200",
            "PM2.5": "⩾75",
            "O3": "⩾180",
            "CO": "⩾15400"
        },
        "health_advisory": "Everyone should avoid all outdoor exertion."
    }
}

def get_gemini_response(api_key: str, prompt: str) -> str:
    """Fetches a response from Google Gemini AI."""
    client = genai.Client(api_key=api_key)
    
    response = client.models.generate_content(contents=prompt, model="gemini-2.0-flash")
    
    if response and response.text:
        return response.text
    else:
        return "No response from Gemini AI."

class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")

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

def get_daily_forecast(city:str, api_key:str) -> dict:

    pass



@click.group()
def cli():
    pass

@cli.command()
@click.argument('city')
@click.option('--api-key', default=os.getenv('API_KEY'), help='Your OpenWeather API key')
def weather(city:str, api_key:str) -> dict:
    """Fetches and displays weather and air quality data for a given city."""


    with console.status(f"Fetching weather data for {city.title()}...", spinner = "dots"):
        # get data
        weather_data = get_weather_data(city, api_key)
        air_quality_data = get_air_quality(city, api_key)


    # layoout
    layout = Layout()

    layout.split(
        Layout(name="header", size=3),
        Layout(ratio=1, name="main"),
        Layout(name="footer",size=3),
        Layout(name="exit", size=1)
    )

    layout["main"].split_row(Layout(name="left"), Layout(name="right", ratio=2))
    layout["left"].split(Layout(name="weather"), Layout(name="air_quality"))
    layout["right"].split(Layout(name="weather_report"), Layout(name="forecast"))
    
    # layout content

    weather_info = (
        f"[bold] Current Weather:[/bold] {weather_data['weather'][0]['main']} ({weather_data['weather'][0]['description']})\n"
        f"[bold] Temperature:[/bold] {weather_data['main']['temp']}°C (feels like {weather_data['main']['feels_like']}°C)\n"
        f"[bold] Min Temperature:[/bold] {weather_data['main']['temp_min']}°C\n"
        f"[bold] Max Temperature:[/bold] {weather_data['main']['temp_max']}°C\n"
        "\n"
        f"[bold] Humidity:[/bold] {weather_data['main']['humidity']}%\n"
        f"[bold] Pressure:[/bold] {weather_data['main']['pressure']} hPa\n"
        f"[bold] Wind Speed:[/bold] {weather_data['wind']['speed']} m/s\n"
        f"[bold] Wind Direction:[/bold] {weather_data['wind']['deg']}°\n"
        "\n"
    )

    air_quality_info = (
        f"[bold] Air Quality Index:[/bold] {air_quality_data['list'][0]['main']['aqi']} ({openweather_aqi_scale_by_index[air_quality_data['list'][0]['main']['aqi']]['qualitative_name']})\n\n"

        f"[bold] Description: [/bold] {openweather_aqi_scale_by_index[air_quality_data['list'][0]['main']['aqi']]['description']}\n\n"
        f"[bold] Health Advisory: [/bold] {openweather_aqi_scale_by_index[air_quality_data['list'][0]['main']['aqi']]['health_advisory']}\n\n"
        "[bold] Air Quality Breakdown:[/bold]\n"
        f"  - CO: {air_quality_data['list'][0]['components']['co']} µg/m³\n"
        f"  - NO2: {air_quality_data['list'][0]['components']['no2']} µg/m³\n"
        f"  - O3: {air_quality_data['list'][0]['components']['o3']} µg/m³\n"
        f"  - SO2: {air_quality_data['list'][0]['components']['so2']} µg/m³\n"
        f"  - PM2.5: {air_quality_data['list'][0]['components']['pm2_5']} µg/m³\n"
        f"  - PM10: {air_quality_data['list'][0]['components']['pm10']} µg/m³\n"
    )


    prompt = f"The time is {datetime.now()}. You are a weather reporter in the city of {city.title()}. You are tasked with giving a weather update based on the following data:\n\n {weather_info} \n {air_quality_info}\n\n Please provide a concise update and include any relevant details about the weather, air quality, and any other important information that a resident of {city.title()} should know. Most important please indicate what a resident can wear today based on the weather and include accessories i.e. umbrella, sunglasses, etc."
    
    with console.status(f"Fetching weather report from Gemini AI for {city.title()}...", spinner="dots"):
        weather_report = get_gemini_response(api_key=os.getenv('GEMINI_API_KEY'), prompt=prompt)

    # Create a panel for the weather information
    header_panel = Panel(Clock(),style="blue")
    weather_panel = Panel(weather_info, title=f"Weather in {city.title()}", style="blue")
    weather_report_panel = Panel(Text(weather_report, style="green"), title="Weather Report", style="blue")
    air_quality_panel = Panel(air_quality_info, title="Current Air Quality", style="blue")
    
    layout["header"].update(header_panel)
    layout["weather"].update(weather_panel)
    layout["weather_report"].update(weather_report_panel)
    layout["air_quality"].update(air_quality_panel)
    layout["exit"].update(Align.left(Text("Press 'q' to exit", style="orange")))
   

    # rendering
    with Live(layout, screen=True, redirect_stderr=False) as live:
        try:
            while True:
                if readchar.readkey() == "q":
                    print("Bye! Have a great day...")
                    break
                sleep(1)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    cli()
