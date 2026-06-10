# backend/aqi_calculator.py

def calculate_sub_index(cp, breakpoints):
    for bp in breakpoints:
        if bp["low"] <= cp <= bp["high"]:
            return (
                (bp["I_high"] - bp["I_low"]) /
                (bp["high"] - bp["low"])
            ) * (cp - bp["low"]) + bp["I_low"]
    return None


def calculate_aqi(pollutants):
    """
    Calculates AQI using CPCB (India) standard.
    AQI = max(sub-indices of all pollutants)
    """

    breakpoints = {
        "PM2.5": [
            {"low": 0, "high": 30, "I_low": 0, "I_high": 50},
            {"low": 31, "high": 60, "I_low": 51, "I_high": 100},
            {"low": 61, "high": 90, "I_low": 101, "I_high": 200},
            {"low": 91, "high": 120, "I_low": 201, "I_high": 300},
            {"low": 121, "high": 250, "I_low": 301, "I_high": 400},
            {"low": 251, "high": 500, "I_low": 401, "I_high": 500}
        ],
        "PM10": [
            {"low": 0, "high": 50, "I_low": 0, "I_high": 50},
            {"low": 51, "high": 100, "I_low": 51, "I_high": 100},
            {"low": 101, "high": 250, "I_low": 101, "I_high": 200},
            {"low": 251, "high": 350, "I_low": 201, "I_high": 300},
            {"low": 351, "high": 430, "I_low": 301, "I_high": 400},
            {"low": 431, "high": 600, "I_low": 401, "I_high": 500}
        ],
        "NO2": [
            {"low": 0, "high": 40, "I_low": 0, "I_high": 50},
            {"low": 41, "high": 80, "I_low": 51, "I_high": 100},
            {"low": 81, "high": 180, "I_low": 101, "I_high": 200},
            {"low": 181, "high": 280, "I_low": 201, "I_high": 300},
            {"low": 281, "high": 400, "I_low": 301, "I_high": 400},
            {"low": 401, "high": 1000, "I_low": 401, "I_high": 500}
        ],
        "SO2": [
            {"low": 0, "high": 40, "I_low": 0, "I_high": 50},
            {"low": 41, "high": 80, "I_low": 51, "I_high": 100},
            {"low": 81, "high": 380, "I_low": 101, "I_high": 200},
            {"low": 381, "high": 800, "I_low": 201, "I_high": 300},
            {"low": 801, "high": 1600, "I_low": 301, "I_high": 400},
            {"low": 1601, "high": 2000, "I_low": 401, "I_high": 500}
        ],
        "CO": [
            {"low": 0, "high": 1, "I_low": 0, "I_high": 50},
            {"low": 1.1, "high": 2, "I_low": 51, "I_high": 100},
            {"low": 2.1, "high": 10, "I_low": 101, "I_high": 200},
            {"low": 10.1, "high": 17, "I_low": 201, "I_high": 300},
            {"low": 17.1, "high": 34, "I_low": 301, "I_high": 400},
            {"low": 34.1, "high": 50, "I_low": 401, "I_high": 500}
        ],
        "O3": [
            {"low": 0, "high": 50, "I_low": 0, "I_high": 50},
            {"low": 51, "high": 100, "I_low": 51, "I_high": 100},
            {"low": 101, "high": 168, "I_low": 101, "I_high": 200},
            {"low": 169, "high": 208, "I_low": 201, "I_high": 300},
            {"low": 209, "high": 748, "I_low": 301, "I_high": 400},
            {"low": 749, "high": 1000, "I_low": 401, "I_high": 500}
        ]
    }

    sub_indices = []

    for pollutant, value in pollutants.items():
        if pollutant in breakpoints:
            si = calculate_sub_index(value, breakpoints[pollutant])
            if si is not None:
                sub_indices.append(si)

    if not sub_indices:
        return None

    return round(max(sub_indices))


def get_aqi_category(aqi):
    if aqi <= 50:
        return "Good", "#00e400"
    elif aqi <= 100:
        return "Satisfactory", "#ffff00"
    elif aqi <= 200:
        return "Moderate", "#ff7e00"
    elif aqi <= 300:
        return "Poor", "#ff0000"
    elif aqi <= 400:
        return "Very Poor", "#8f3f97"
    else:
        return "Severe", "#7e0023"


# -----------------------------------
# LOCAL TEST (SAFE)
# -----------------------------------
if __name__ == "__main__":
    sample_data = {
        "PM2.5": 80,
        "PM10": 120,
        "NO2": 40,
        "SO2": 20,
        "CO": 2,
        "O3": 60
    }

    aqi = calculate_aqi(sample_data)
    category, _ = get_aqi_category(aqi)

    print("Calculated AQI:", aqi)
    print("Category:", category)
