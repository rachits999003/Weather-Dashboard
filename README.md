
# 🌦️ Modern Weather Dashboard

A sleek and responsive weather dashboard built using Python, Tkinter, and the OpenWeatherMap API. Provides real-time weather information and a 5-day forecast visualized with Matplotlib.

## 🚀 Features

- 🌍 Location-based weather using geocoding
- 🌡️ Current weather with emoji icons
- 📊 Interactive 5-day temperature forecast
- 📈 Dynamic Matplotlib charts
- 🎨 Custom themed UI (modern and clean)
- ⚡ Multi-threaded API calls to keep UI smooth

## 🧠 Technologies Used

- `tkinter` – UI framework
- `matplotlib` – Graph plotting
- `geopy` – Geolocation service
- `requests` – API requests
- `dotenv` – Secure API key storage
- `OpenWeatherMap API` – Weather data source

## 🔧 Setup Instructions

1. **Clone the repo**

```bash
git clone https://github.com/rachits999003/weather-dashboard.git
cd weather-dashboard
```

2. **Install dependencies**

You can install the required libraries using pip:

```bash
pip install -r requirements.txt
```

3. **Set up your environment**

Create a `.env` file in the root directory:

```env
WEATHER_API_KEY=your_openweathermap_api_key
```

4. **Run the app**

```bash
python main.py
```

## 📂 Project Structure

```
weather-dashboard/
├── main.py              # Main GUI logic and API calls
├── .env                 # Your secret API key
├── requirements.txt     # Dependencies list
└── README.md            # You're reading it!
```

## 🙌 Credits

- Weather data from OpenWeatherMap
- Geolocation from Nominatim / OpenStreetMap

## 📄 License

This project is open-source under the MIT License.
