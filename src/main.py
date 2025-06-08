import click
from time import sleep
from datetime import datetime
import os 
import dotenv
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.align import Align
from rich.live import Live
from rich.text import Text
import readchar
from charts import Charts
from weather import *
from config import Mapping
from llm import get_gemini_response

# Load environment variables from .env file
dotenv.load_dotenv()

console = Console()


class Clock:
    """Renders the time in the center of the screen."""

    def __rich__(self) -> Text:
        return Text(datetime.now().ctime(), style="bold magenta", justify="center")


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
        f"[bold] Air Quality Index:[/bold] {air_quality_data['list'][0]['main']['aqi']} ({Mapping.openweather_aqi_scale_by_index[air_quality_data['list'][0]['main']['aqi']]['qualitative_name']})\n\n"

        f"[bold] Description: [/bold] {Mapping.openweather_aqi_scale_by_index[air_quality_data['list'][0]['main']['aqi']]['description']}\n\n"
        f"[bold] Health Advisory: [/bold] {Mapping.openweather_aqi_scale_by_index[air_quality_data['list'][0]['main']['aqi']]['health_advisory']}\n\n"
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

    # Charts
    temp_bar = Charts({"mon": 1, "tue":2, "wed":3,"thu":4,"fri":4,"sat":2,"sun":1})

    # Create a panel for the weather information
    header_panel = Panel(Clock(),style="blue")
    weather_panel = Panel(weather_info, title=f"Weather in {city.title()}", style="blue")
    weather_report_panel = Panel(Text(weather_report, style="green"), title="Weather Report", style="blue")
    air_quality_panel = Panel(air_quality_info, title="Current Air Quality", style="blue")
    forecast_panel = Panel(temp_bar.bar("+"), title="Weekly Forecast", style="magenta")

    layout["header"].update(header_panel)
    layout["weather"].update(weather_panel)
    layout["weather_report"].update(weather_report_panel)
    layout["air_quality"].update(air_quality_panel)
    layout["forecast"].update(forecast_panel)
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
