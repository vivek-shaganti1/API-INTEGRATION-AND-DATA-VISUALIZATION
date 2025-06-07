import os
from flask import Flask, render_template, request
import requests
import seaborn as sns
import matplotlib

matplotlib.use('Agg')  # Add this line to fix the main loop error
import matplotlib.pyplot as plt

from dotenv import load_dotenv
load_dotenv()


app = Flask(__name__)

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
MAPBOX_API_KEY = os.getenv("MAPBOX_API_KEY")

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    image_filename = None

    if request.method == 'POST':
        city = request.form['city']
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data.get('list'):
            temps = [entry['main']['temp'] for entry in data['list'][:8]]
            times = [entry['dt_txt'].split()[1][:5] for entry in data['list'][:8]]

            sns.set(style="darkgrid")
            plt.figure(figsize=(10, 4))
            sns.lineplot(x=times, y=temps, marker="o")
            plt.title(f"Temperature Forecast for {city}")
            plt.ylabel("Temp (°C)")
            plt.xlabel("Time")
            plt.tight_layout()

            image_filename = "plot.png"
            image_path = os.path.join("static", image_filename)
            plt.savefig(image_path)
            plt.close()
            print(f"Plot saved at {image_path}")

            weather_data = {
                'city': city,
                'description': data['list'][0]['weather'][0]['description'],
                'temp': data['list'][0]['main']['temp'],
                'humidity': data['list'][0]['main']['humidity']
            }

    return render_template("index.html", weather=weather_data, image=image_filename, mapbox_api_key=MAPBOX_API_KEY)

if __name__ == '__main__':
    app.run(debug=True)
