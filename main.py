import os
import sys
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime
import threading
import time

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from matplotlib.figure import Figure
import numpy as np

from geopy.geocoders import Nominatim
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
if WEATHER_API_KEY is None:
    print("Please set the WEATHER_API_KEY environment variable.")
    sys.exit(1)

# Constants
BG_COLOR = "#f0f0f0"
PRIMARY_COLOR = "#2c3e50"
ACCENT_COLOR = "#3498db"
SECONDARY_COLOR = "#ecf0f1"
TEXT_COLOR = "#34495e"
ERROR_COLOR = "#e74c3c"
SUCCESS_COLOR = "#2ecc71"

# Weather Icons
WEATHER_ICONS = {
    "clear sky": "☀️",
    "few clouds": "🌤️",
    "scattered clouds": "⛅",
    "broken clouds": "☁️",
    "shower rain": "🌦️",
    "rain": "🌧️",
    "thunderstorm": "⛈️",
    "snow": "❄️",
    "mist": "🌫️",
    "overcast clouds": "☁️",
    "light rain": "🌦️",
    "moderate rain": "🌧️",
    "heavy rain": "🌧️",
}

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Modern Weather App")
        self.root.geometry("900x650")
        self.root.configure(bg=BG_COLOR)
        self.root.minsize(900, 650)
        
        # Initialize geocoder
        self.geolocator = Nominatim(user_agent="weather_app")
        
        # Current weather data
        self.current_weather = None
        self.forecast_data = None
        self.location_info = None
        
        # Create custom fonts
        self.title_font = font.Font(family="Helvetica", size=16, weight="bold")
        self.subtitle_font = font.Font(family="Helvetica", size=12, weight="bold")
        self.regular_font = font.Font(family="Helvetica", size=10)
        
        # Create UI
        self.create_ui()
        
    def create_ui(self):
        # Main frame
        main_frame = tk.Frame(self.root, bg=BG_COLOR)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="Weather Dashboard", 
            font=self.title_font, 
            bg=BG_COLOR, 
            fg=PRIMARY_COLOR
        )
        title_label.pack(pady=(0, 20))
        
        # Search frame
        search_frame = tk.Frame(main_frame, bg=BG_COLOR)
        search_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Location entry
        self.location_var = tk.StringVar()
        self.location_entry = ttk.Entry(
            search_frame, 
            textvariable=self.location_var, 
            font=self.regular_font,
            width=50
        )
        self.location_entry.pack(side=tk.LEFT, padx=(0, 10), ipady=5)
        self.location_entry.bind("<Return>", lambda e: self.get_weather())
        
        # Search button
        search_button = ttk.Button(
            search_frame,
            text="Search",
            command=self.get_weather
        )
        search_button.pack(side=tk.LEFT, padx=5, ipady=5)
        
        # Status label
        self.status_var = tk.StringVar()
        self.status_label = tk.Label(
            main_frame,
            textvariable=self.status_var,
            font=self.regular_font,
            bg=BG_COLOR,
            fg=TEXT_COLOR
        )
        self.status_label.pack(pady=(0, 10))
        
        # Content frame
        self.content_frame = tk.Frame(main_frame, bg=BG_COLOR)
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Current weather frame
        self.current_weather_frame = tk.Frame(self.content_frame, bg=SECONDARY_COLOR, bd=1, relief=tk.GROOVE)
        self.current_weather_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Current weather title
        current_title = tk.Label(
            self.current_weather_frame,
            text="Current Weather",
            font=self.subtitle_font,
            bg=SECONDARY_COLOR,
            fg=PRIMARY_COLOR
        )
        current_title.pack(pady=10)
        
        # Current weather content
        self.weather_info_frame = tk.Frame(self.current_weather_frame, bg=SECONDARY_COLOR)
        self.weather_info_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Location label
        self.location_label = tk.Label(
            self.weather_info_frame,
            text="Enter a location to start",
            font=self.subtitle_font,
            bg=SECONDARY_COLOR,
            fg=PRIMARY_COLOR,
            wraplength=350
        )
        self.location_label.pack(pady=10)
        
        # Weather icon label
        self.weather_icon = tk.Label(
            self.weather_info_frame,
            text="",
            font=font.Font(size=48),
            bg=SECONDARY_COLOR
        )
        self.weather_icon.pack(pady=5)
        
        # Temperature label
        self.temp_label = tk.Label(
            self.weather_info_frame,
            text="",
            font=font.Font(family="Helvetica", size=36),
            bg=SECONDARY_COLOR,
            fg=PRIMARY_COLOR
        )
        self.temp_label.pack(pady=5)
        
        # Description label
        self.desc_label = tk.Label(
            self.weather_info_frame,
            text="",
            font=self.regular_font,
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR
        )
        self.desc_label.pack(pady=5)
        
        # Additional info frame
        self.additional_info = tk.Frame(self.weather_info_frame, bg=SECONDARY_COLOR)
        self.additional_info.pack(fill=tk.X, pady=15)
        
        # Feels like, humidity, wind speed
        self.feels_like = tk.Label(
            self.additional_info,
            text="",
            font=self.regular_font,
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR
        )
        self.feels_like.pack(pady=2)
        
        self.humidity = tk.Label(
            self.additional_info,
            text="",
            font=self.regular_font,
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR
        )
        self.humidity.pack(pady=2)
        
        self.wind_speed = tk.Label(
            self.additional_info,
            text="",
            font=self.regular_font,
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR
        )
        self.wind_speed.pack(pady=2)
        
        self.last_updated = tk.Label(
            self.additional_info,
            text="",
            font=self.regular_font,
            bg=SECONDARY_COLOR,
            fg=TEXT_COLOR
        )
        self.last_updated.pack(pady=10)
        
        # Forecast frame
        self.forecast_frame = tk.Frame(self.content_frame, bg=SECONDARY_COLOR, bd=1, relief=tk.GROOVE)
        self.forecast_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Forecast title
        forecast_title = tk.Label(
            self.forecast_frame,
            text="Weather Forecast",
            font=self.subtitle_font,
            bg=SECONDARY_COLOR,
            fg=PRIMARY_COLOR
        )
        forecast_title.pack(pady=10)
        
        # Create matplotlib figure for forecast
        self.forecast_plot_frame = tk.Frame(self.forecast_frame, bg=SECONDARY_COLOR)
        self.forecast_plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create figure with default empty plot
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.forecast_plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Initial plot setup
        self.ax.set_title("Temperature Forecast")
        self.ax.set_xlabel("Date")
        self.ax.set_ylabel("Temperature (°C)")
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Set initial focus on location entry
        self.location_entry.focus_set()
    
    def get_weather(self):
        """Get weather data for the input location"""
        location_name = self.location_var.get().strip()
        if not location_name:
            messagebox.showerror("Error", "Please enter a location")
            return
        
        # Show loading status
        self.status_var.set("Fetching location data...")
        self.root.update()
        
        # Run geocoding and API calls in a separate thread to keep UI responsive
        threading.Thread(target=self._fetch_weather_data, args=(location_name,), daemon=True).start()
    
    def _fetch_weather_data(self, location_name):
        """Fetch weather data in background thread"""
        try:
            # Get location coordinates
            location = self.geolocator.geocode(location_name, timeout=10)
            if not location:
                self.status_var.set("Location not found. Please try again.")
                return
            
            self.location_info = location
            lat, lon = location.latitude, location.longitude
            
            # Get current weather
            self.status_var.set("Fetching current weather...")
            self.root.update_idletasks()
            
            current_response = requests.get(
                "https://api.openweathermap.org/data/2.5/weather",
                params={
                    "lat": lat, 
                    "lon": lon, 
                    "appid": WEATHER_API_KEY, 
                    "units": "metric"
                }
            )
            current_response.raise_for_status()
            self.current_weather = current_response.json()
            
            # Get 5-day forecast
            self.status_var.set("Fetching forecast data...")
            self.root.update_idletasks()
            
            forecast_response = requests.get(
                "https://api.openweathermap.org/data/2.5/forecast",
                params={
                    "lat": lat, 
                    "lon": lon, 
                    "appid": WEATHER_API_KEY, 
                    "units": "metric"
                }
            )
            forecast_response.raise_for_status()
            self.forecast_data = forecast_response.json()
            
            # Update UI with weather data
            self.root.after(0, self._update_ui)
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
    
    def _update_ui(self):
        """Update UI with weather data"""
        if not self.current_weather:
            return
        
        # Update current weather information
        city = self.current_weather["name"]
        country = self.current_weather.get("sys", {}).get("country", "")
        
        # Get location address from geocoder result
        if self.location_info and self.location_info.address:
            location_text = self.location_info.address
        else:
            location_text = f"{city}, {country}" if country else city
        
        self.location_label.config(text=location_text)
        
        # Weather description and icon
        description = self.current_weather["weather"][0]["description"]
        icon_text = WEATHER_ICONS.get(description.lower(), "🌡️")
        self.weather_icon.config(text=icon_text)
        
        # Temperature
        temp = self.current_weather["main"]["temp"]
        self.temp_label.config(text=f"{temp:.1f}°C")
        
        # Description
        self.desc_label.config(text=description.title())
        
        # Additional info
        feels_like = self.current_weather["main"]["feels_like"]
        humidity = self.current_weather["main"]["humidity"]
        wind_speed = self.current_weather["wind"]["speed"]
        
        self.feels_like.config(text=f"Feels like: {feels_like:.1f}°C")
        self.humidity.config(text=f"Humidity: {humidity}%")
        self.wind_speed.config(text=f"Wind Speed: {wind_speed} m/s")
        
        # Last updated
        now = datetime.now().strftime("%H:%M:%S, %d %b %Y")
        self.last_updated.config(text=f"Last updated: {now}")
        
        # Update forecast plot if we have forecast data
        if self.forecast_data:
            self._update_forecast_plot()
        
        self.status_var.set("Weather data loaded successfully!")
    
    def _update_forecast_plot(self):
        """Update the forecast plot with data"""
        # Clear the current plot
        self.ax.clear()
        
        # Extract forecast data
        forecast_list = self.forecast_data.get("list", [])
        if not forecast_list:
            return
        
        # Extract timestamps and temperatures
        timestamps = []
        temperatures = []
        feels_like_temps = []
        
        for item in forecast_list:
            # Convert timestamp to datetime
            dt = datetime.fromtimestamp(item["dt"])
            timestamps.append(dt)
            
            # Get temperature and feels like
            temp = item["main"]["temp"]
            feels_like = item["main"]["feels_like"]
            
            temperatures.append(temp)
            feels_like_temps.append(feels_like)
        
        # Plot data
        self.ax.plot(timestamps, temperatures, 'o-', color=ACCENT_COLOR, label='Temperature')
        self.ax.plot(timestamps, feels_like_temps, 'o--', color=SUCCESS_COLOR, label='Feels like')
        
        # Format x-axis to display dates nicely
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%b\n%H:%M'))
        plt.setp(self.ax.get_xticklabels(), rotation=45, ha='right')
        
        # Add grid and legend
        self.ax.grid(True, linestyle='--', alpha=0.7)
        self.ax.legend()
        
        # Set labels and title
        self.ax.set_xlabel('Date & Time')
        self.ax.set_ylabel('Temperature (°C)')
        self.ax.set_title('5-Day Temperature Forecast')
        
        # Adjust layout and draw
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()