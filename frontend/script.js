const cityInput = document.getElementById("city");

const aqiValue = document.getElementById("aqiValue");
const aqiStatus = document.getElementById("aqiStatus");

const thermoFill = document.getElementById("thermoFill");
const faceIcon = document.getElementById("faceIcon");

const pm25 = document.getElementById("pm25");
const pm10 = document.getElementById("pm10");
const no2 = document.getElementById("no2");
const so2 = document.getElementById("so2");
const co = document.getElementById("co");
const o3 = document.getElementById("o3");

const mlCluster = document.getElementById("mlCluster");

function searchCity() {
    const city = cityInput.value.trim();
    if (city === "") {
        alert("Please enter a city name");
        return;
    }
    fetchAQIData(city);
}

async function fetchAQIData(city) {
    try {
        const response = await fetch(
            `http://127.0.0.1:5000/calculate-aqi?city=${encodeURIComponent(city)}`
        );

        if (!response.ok) throw new Error("Backend error");

        const data = await response.json();

        // AQI
        aqiValue.innerText = data.AQI;
        aqiStatus.innerText = data.category;

        // ML Cluster
        mlCluster.innerText = "ML Pollution Pattern: " + data.ml_cluster;

        // Thermometer height
        let percent = Math.min((data.AQI / 500) * 100, 100);
        thermoFill.style.height = percent + "%";

        // Color + Face logic
        if (data.AQI <= 50) {
            thermoFill.style.background = "#00ff99";
            faceIcon.innerText = "😊";
        } else if (data.AQI <= 100) {
            thermoFill.style.background = "#ffee58";
            faceIcon.innerText = "🙂";
        } else if (data.AQI <= 200) {
            thermoFill.style.background = "#ff9800";
            faceIcon.innerText = "😐";
        } else if (data.AQI <= 300) {
            thermoFill.style.background = "#ff5252";
            faceIcon.innerText = "😷";
        } else {
            thermoFill.style.background = "#8e24aa";
            faceIcon.innerText = "☠️";
        }

        // Pollutants
        pm25.innerText = data.pollutants["PM2.5"];
        pm10.innerText = data.pollutants["PM10"];
        no2.innerText = data.pollutants["NO2"];
        so2.innerText = data.pollutants["SO2"];
        co.innerText = data.pollutants["CO"];
        o3.innerText = data.pollutants["O3"];

    } catch (error) {
        alert("Backend not running or API issue");
        console.error(error);
    }
}

// Default load
document.addEventListener("DOMContentLoaded", () => {
    fetchAQIData("Delhi");
});
