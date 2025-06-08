
class Mapping:

    
    openweather_aqi_scale_by_index = {
        1: {
            "qualitative_name": "Good",
            "description": "Air quality is considered satisfactory, and air pollution poses little or no risk.",
            "pollutant_ranges_ug_m3": {
                "SO2": "[0; 20)",
                "NO2": "[0; 40)",
                "PM10": "[0; 20)",
                "PM2.5": "[0; 10)",
                "O3": "[0; 60)",
                "CO": "[0; 4400)"
            },
            "health_advisory": "None."
        },
        2: {
            "qualitative_name": "Fair",
            "description": "Air quality is acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution.",
            "pollutant_ranges_ug_m3": {
                "SO2": "[20; 80)",
                "NO2": "[40; 70)",
                "PM10": "[20; 50)",
                "PM2.5": "[10; 25)",
                "O3": "[60; 100)",
                "CO": "[4400; 9400)"
            },
            "health_advisory": "Unusually sensitive people should consider limiting prolonged or heavy exertion outdoors."
        },
        3: {
            "qualitative_name": "Moderate",
            "description": "Members of sensitive groups may experience health effects. The general public is less likely to be affected.",
            "pollutant_ranges_ug_m3": {
                "SO2": "[80; 250)",
                "NO2": "[70; 150)",
                "PM10": "[50; 100)",
                "PM2.5": "[25; 50)",
                "O3": "[100; 140)",
                "CO": "[9400-12400)"
            },
            "health_advisory": "People with lung disease (such as asthma), children, older adults, and people who are active outdoors should reduce prolonged or heavy exertion. Everyone else should limit prolonged or heavy exertion."
        },
        4: {
            "qualitative_name": "Poor",
            "description": "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.",
            "pollutant_ranges_ug_m3": {
                "SO2": "[250; 350)",
                "NO2": "[150; 200)",
                "PM10": "[100; 200)",
                "PM2.5": "[50; 75)",
                "O3": "[140; 180)",
                "CO": "[12400; 15400)"
            },
            "health_advisory": "People with lung disease (such as asthma), children, older adults, and people who are active outdoors should avoid prolonged or heavy exertion. Everyone else should reduce prolonged or heavy exertion."
        },
        5: {
            "qualitative_name": "Very Poor",
            "description": "Health warnings of emergency conditions. The entire population is more likely to be affected.",
            "pollutant_ranges_ug_m3": {
                "SO2": "⩾350",
                "NO2": "⩾200",
                "PM10": "⩾200",
                "PM2.5": "⩾75",
                "O3": "⩾180",
                "CO": "⩾15400"
            },
            "health_advisory": "Everyone should avoid all outdoor exertion."
        }
    }
