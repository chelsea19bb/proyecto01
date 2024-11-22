const resultDiv = document.getElementById('result');
const mapDiv = document.getElementById('map');
let map;

async function getWeather() {
    const city = document.getElementById('cityInput').value.trim();
    if (!city) {
        alert("Por favor, ingresa el nombre de una ciudad.");
        return;
    }

    const response = await eel.get_weather(city)();
    if (response.error) {
        showError(response.error);
    } else {
        showWeather(city, response);
        showMap(response.coordinates.lat, response.coordinates.lon);
    }
}

function showWeather(city, data) {
    resultDiv.className = "animate__animated animate__fadeIn text-dark";
    resultDiv.innerHTML = `
        <div class="card">
            <div class="card-body">
                <h5 class="card-title">Clima en ${city}</h5>
                <p>🌡️ Temperatura: ${data.temperature}°C</p>
                <p>🌬️ Viento: ${data.forecast.wind_speed} km/h</p>
                <p>💧 Humedad: ${data.forecast.humidity}%</p>
                <p>🌤️ Sensación térmica: ${data.forecast.feels_like}°C</p>
                <p>${data.description}</p>
            </div>
        </div>`;
}

function showError(message) {
    resultDiv.className = "animate__animated animate__shakeX text-danger";
    resultDiv.innerHTML = `<p>${message}</p>`;
    mapDiv.style.display = "none";
}

function showMap(lat, lon) {
    mapDiv.style.display = "block";
    if (map) {
        map.remove();
    }
    map = L.map('map').setView([lat, lon], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '© OpenStreetMap'
    }).addTo(map);
    L.marker([lat, lon]).addTo(map)
        .bindPopup(`Ubicación: (${lat.toFixed(2)}, ${lon.toFixed(2)})`)
        .openPopup();
}
