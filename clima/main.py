import eel
import requests
import json

# Inicializar eel con la carpeta web
eel.init('web')

# API key para OpenWeatherMap (reemplaza esto con tu API key)
WEATHER_API_KEY = "5f3feab84ae445fc3e6f9b1528bcf1fe"

@eel.expose
def get_weather(city):
    try:
        # Obtener coordenadas de la ciudad
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}"
        geo_response = requests.get(geocoding_url)
        geo_data = geo_response.json()

        if not geo_data:
            return {"error": "Ciudad no encontrada"}

        # Obtener lat y lon de la primera coincidencia
        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Obtener el clima usando las coordenadas
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=es"
        weather_response = requests.get(weather_url)
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            return {
                "temperature": round(weather_data["main"]["temp"]),
                "description": weather_data["weather"][0]["description"].capitalize(),
                "forecast": {
                    "humidity": weather_data["main"]["humidity"],
                    "wind_speed": round(weather_data["wind"]["speed"] * 3.6, 1),  # Convertir a km/h
                    "feels_like": round(weather_data["main"]["feels_like"])
                },
                "coordinates": {
                    "lat": lat,
                    "lon": lon
                }
            }
        else:
            return {"error": "Error al obtener datos del clima"}

    except Exception as e:
        print(f"Error: {str(e)}")  # Para debugging
        return {"error": f"Error en la aplicación: {str(e)}"}

# Iniciar la aplicación
if __name__ == "__main__":
    try:
        eel.start('index.html', size=(800, 600))
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
