from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = "95c287908cb0a660ae025b93df88fe7e"

@app.route("/", methods=["GET", "POST"])
def index():
    weather = None
    error = None

    if request.method == "POST":
        city = request.form["city"].strip()

        try:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)

            data = response.json()

            print(data)

            if str(data.get("cod")) == "200":
                temp = data["main"]["temp"]
                humidity = data["main"]["humidity"]
                condition = data["weather"][0]["main"]
                forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
                forecast_data = requests.get(forecast_url).json()

                forecast_list = []

                for item in forecast_data["list"][:5]:
                    forecast_list.append({
                         "temp": item["main"]["temp"],
                         "condition": item["weather"][0]["main"]
                })

                
                if temp > 35:
                   recommendation = "🔥 Very Hot! Stay hydrated and avoid sun."
                   clothes = "👕 Wear light cotton clothes, sunglasses, and cap."
                   food = "🥤 Drink juices, coconut water, eat fruits like watermelon."

                elif temp < 20:
                    recommendation = "🧥 Cold weather! Keep yourself warm."
                    clothes = "🧥 Wear sweaters, jackets, and warm clothes."
                    food = "☕ Drink hot tea/coffee, eat soups and warm foods."

                elif "Rain" in condition:
                     recommendation = "🌧 Rainy weather! Be careful outside."
                     clothes = "🧥 Wear raincoat, carry umbrella."
                     food = "🍜 Eat hot snacks like soup, noodles, tea."

                elif "Cloud" in condition:
                     recommendation = "☁ Cloudy weather, comfortable outside."
                     clothes = "👕 Light casual wear is fine."
                     food = "🍲 Normal food, stay hydrated."

                else:
                    recommendation = "😊 Pleasant weather. Enjoy your day!"
                    clothes = "👕 Comfortable clothes."
                    food = "🍽 Eat healthy and balanced meals."
                if "Clear" in condition:
                    icon = "☀"
                elif "Cloud" in condition:
                    icon = "☁"
                elif "Rain" in condition:
                    icon = "🌧"
                else:
                    icon = "🌤"

            

                weather = {
                  "city": city,
                  "temp": temp,
                  "humidity": humidity,
                  "condition": condition,
                  "icon": icon,
                  "recommendation": recommendation,
                  "clothes": clothes,
                  "food": food,
                  "forecast": forecast_list
                }

            else:
                error = "❌ City not found!"

        except Exception as e:
            error = "⚠ Something went wrong!"
            print(e)

    return render_template("index.html", weather=weather, error=error)
@app.route("/location", methods=["GET", "POST"])
def location():
    lat = request.args.get("lat")
    lon = request.args.get("lon")

    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if str(data.get("cod")) == "200":
            city = data["name"]
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            condition = data["weather"][0]["main"]
            forecast_url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric"
            forecast_data = requests.get(forecast_url).json()

            forecast_list = []

            for item in forecast_data["list"][:5]:
                forecast_list.append({
                    "temp": item["main"]["temp"],
                    "condition": item["weather"][0]["main"]
            })

            # ✅ SAME RECOMMENDATION LOGIC
            if temp > 35:
                recommendation = "🔥 Very Hot! Stay hydrated and avoid sun."
                clothes = "👕 Wear light cotton clothes, sunglasses, and cap."
                food = "🥤 Drink juices, coconut water, eat fruits like watermelon."

            elif temp < 20:
                recommendation = "🧥 Cold weather! Keep yourself warm."
                clothes = "🧥 Wear sweaters, jackets, and warm clothes."
                food = "☕ Drink hot tea/coffee, eat soups and warm foods."

            elif "Rain" in condition:
                recommendation = "🌧 Rainy weather! Be careful outside."
                clothes = "🧥 Wear raincoat, carry umbrella."
                food = "🍜 Eat hot snacks like soup, noodles, tea."

            elif "Cloud" in condition:
                recommendation = "☁ Cloudy weather, comfortable outside."
                clothes = "👕 Light casual wear is fine."
                food = "🍲 Normal food, stay hydrated."

            else:
                recommendation = "😊 Pleasant weather. Enjoy your day!"
                clothes = "👕 Comfortable clothes."
                food = "🍽 Eat healthy and balanced meals."

            # ✅ ICON
            if "Clear" in condition:
                icon = "☀"
            elif "Cloud" in condition:
                icon = "☁"
            elif "Rain" in condition:
                icon = "🌧"
            else:
                icon = "🌤"

            # ✅ UPDATED WEATHER DICTIONARY
            weather = {
                "city": city,
                "temp": temp,
                "humidity": humidity,
                "condition": condition,
                "icon": icon,
                "recommendation": recommendation,
                "clothes": clothes,
                "food": food,
                "forecast": forecast_list
            }

            return render_template("index.html", weather=weather)

        else:
            return render_template("index.html", error="❌ Location not found!")

    except Exception as e:
        print(e)
        return render_template("index.html", error="⚠ Error fetching location data")

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
