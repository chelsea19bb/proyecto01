import eel
import requests

# Inicializar Eel con la carpeta web
eel.init('web')

# API key para OpenWeatherMap (reemplázala con tu API key válida)
WEATHER_API_KEY = "5f3feab84ae445fc3e6f9b1528bcf1fe"

# Función expuesta a JavaScript para obtener datos climáticos y coordenadas
@eel.expose
def get_weather(city):
    try:
        if not city.strip():
            return {"error": "Por favor, ingresa el nombre de una ciudad."}

        # Obtener coordenadas de la ciudad
        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={WEATHER_API_KEY}"
        geo_response = requests.get(geocoding_url, timeout=10)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            return {"error": "Ciudad no encontrada"}

        lat = geo_data[0]['lat']
        lon = geo_data[0]['lon']

        # Obtener datos meteorológicos
        weather_url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={WEATHER_API_KEY}&units=metric&lang=es"
        weather_response = requests.get(weather_url, timeout=10)
        weather_response.raise_for_status()
        weather_data = weather_response.json()

        if weather_response.status_code == 200:
            return {
                "temperature": round(weather_data["main"]["temp"]),
                "description": weather_data["weather"][0]["description"].capitalize(),
                "forecast": {
                    "humidity": weather_data["main"]["humidity"],
                    "wind_speed": round(weather_data["wind"]["speed"] * 3.6, 1),  # Convertir a km/h
                    "feels_like": round(weather_data["main"]["feels_like"]),
                },
                "coordinates": {"lat": lat, "lon": lon},
            }
        else:
            return {"error": "Error al obtener datos del clima"}

    except requests.exceptions.RequestException:
        return {"error": "No se pudo conectar al servicio. Verifica tu conexión a Internet."}
    except Exception as e:
        return {"error": f"Error inesperado: {str(e)}"}

# Inicia la aplicación
if __name__ == "__main__":
    try:
        eel.start('index.html', size=(800, 600))
    except Exception as e:
        print(f"Error al iniciar la aplicación: {str(e)}")
