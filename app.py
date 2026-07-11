from flask import Flask, render_template, request
import requests
import google.generativeai as genai
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def get_ai_advice(city, temp, humidity, condition):
    prompt = f"""
    You are a weather assistant.

    City: {city}
    Temperature: {temp}°C
    Humidity: {humidity}%
    Weather Condition: {condition}

    Return the answer in HTML format like this:

    <h3>🌤 Weather Summary</h3>
    <p>...</p>

    <h3>👕 Clothing Suggestion</h3>
    <p>...</p>

    <h3>🍲 Food Suggestion</h3>
    <p>...</p>

    <h3>🚗 Travel Advice</h3>
    <p>...</p>

    <h3>💪 Health Tip</h3>
    <p>...</p>

    Do not use markdown (* or **).
    Return only HTML.
    """

    try:
        response = model.generate_content(prompt)

        print("Gemini Response:")
        print(response.text)

        return response.text

    except Exception as e:
        print("Gemini Error:", e)
        return """
        <h3>⚠ Gemini AI</h3>
        <p>AI Recommendation is temporarily unavailable.</p>
        <p>Please try again later.</p>
        """

API_KEY = os.getenv("OPENWEATHER_API_KEY")

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

                for item in forecast_data["list"][::8][:5]:

                    day = datetime.strptime(
                        item["dt_txt"],
                        "%Y-%m-%d %H:%M:%S"
                    ).strftime("%A")

                    forecast_list.append({
                        "day": day,
                        "temp": round(item["main"]["temp"]),
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

                ai_advice = get_ai_advice(city, temp, humidity, condition)
                print("Weather dictionary is being created")
                print("AI Advice:", ai_advice)

                
             
                weather = {
                  "city": city,
                  "temp": temp,
                  "humidity": humidity,
                  "condition": condition,
                  "icon": icon,
                  "recommendation": recommendation,
                  "clothes": clothes,
                  "food": food,
                  "ai_advice": ai_advice,
                  "forecast": forecast_list
                }

            else:
                error = "❌ City not found!"

        except Exception as e:
            error = str(e)
            print("ERROR:", e)
    if weather:
        return render_template("result.html", weather=weather)

    return render_template("index.html", error=error)

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

            for item in forecast_data["list"][::8][:5]:

                day = datetime.strptime(
                    item["dt_txt"],
                    "%Y-%m-%d %H:%M:%S"
                ).strftime("%A")

                forecast_list.append({
                   "day": day,
                   "temp": round(item["main"]["temp"]),
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
            
            
            ai_advice = get_ai_advice(city, temp, humidity, condition)
            print("Weather dictionary is being created")
            print("AI Advice:", ai_advice)

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
                "ai_advice": ai_advice,
                "forecast": forecast_list
            }
            return render_template("result.html", weather=weather)
            
        else:
            return render_template("index.html", error="❌ Location not found!")

    except Exception as e:
        print(e)
        return render_template("index.html", error="⚠ Error fetching location data")

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
