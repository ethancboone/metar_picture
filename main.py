import requests
import time

led_pins = {
    'KNGP':1,
    'KCRP':2,
    'KVCT':3
}

api_url = 'https://aviationweather.gov/api/data/metar'

# Function to fetch METAR data for an airfield
def get_metar(icao):
    
    params = {
        'ids':icao,
        'format':'json',
        'hours':1
    }

    response = requests.get(api_url, params=params)
    data = response.json()[0]

    return data

def flight_cat(data: dict):
    
    #Getting our visibility and ceiling information
    visib = data['visib']
    ceil = data['clouds'][0]['base']
    
    # Making our ceiling information an integer
    visib = int(visib.replace('+',''))
    
    if visib < 1 or ceil < 500:
        return "LIFR"  # Low IFR
    elif (visib >= 1 and visib < 3) and (ceil >= 500 and ceil < 1000):
        return "IFR"  # Instrument Flight Rules
    elif (visib >= 3 and visib <= 5) and (ceil >= 1000 and ceil <= 3000):
        return "MVFR"  # Marginal VFR
    else:
        return "VFR"  # Visual Flight Rules
    
while True:
    for airfield, pin in led_pins.items():
        metar = get_metar(airfield)
        if metar:
            led_color = flight_cat(metar)
            print(f'{airfield}: {led_color}')
        else:
            # Turn off LED if weather data is not available
            print(f'FAIL\n{airfield}: {led_color}')
            
    # Fetch weather data every 5 minutes
    time.sleep(300)