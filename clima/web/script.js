// Definición de capas de mapas
var openStreetMapStandard = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
});

var openStreetMapTopo = L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: &copy; OpenStreetMap contributors, OpenTopoMap'
});

var openStreetMapHot = L.tileLayer('https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors, Humanitarian OpenStreetMap Team'
});

// Inicializa el mapa con una capa estándar
var map = L.map('map', {
    center: [0, 0],
    zoom: 2,
    layers: [openStreetMapStandard]
});

// Control de capas
var baseMaps = {
    "Estándar": openStreetMapStandard,
    "Topográfico": openStreetMapTopo,
    "Humanitario": openStreetMapHot
};
L.control.layers(baseMaps).addTo(map);

// Función para buscar la ciudad y actualizar el mapa
function buscarCiudad() {
    const ciudad = document.getElementById('city-input').value;

    if (ciudad) {
        // Llama a la función de eel para obtener el clima
        eel.get_weather(ciudad)(function (datos) {
            if (datos.error) {
                alert(datos.error);
                return;
            }

            // Actualiza la información del clima en la interfaz
            document.getElementById('temperature').textContent = `${datos.temperature}°C`;
            document.getElementById('description').textContent = datos.description;
            document.getElementById('humidity').textContent = `${datos.forecast.humidity}%`;
            document.getElementById('wind').textContent = `${datos.forecast.wind_speed} km/h`;
            document.getElementById('feels').textContent = `${datos.forecast.feels_like}°C`;

            // Mueve el mapa a la ubicación de la ciudad y agrega un marcador
            const { lat, lon } = datos.coordinates;
            map.setView([lat, lon], 13);
            L.marker([lat, lon]).addTo(map)
                .bindPopup(`<b>${ciudad}</b><br>${datos.description}`)
                .openPopup();
        });
    } else {
        alert("Por favor, ingresa una ciudad.");
    }
}
