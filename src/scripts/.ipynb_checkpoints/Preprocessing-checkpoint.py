
#-----------------date_process----------------------
def date_process(x):
    """
    Function that converts a float value into a pandas datestamp.
    This function can takes both date and datetime formats.
    x = accepts float with length 14 or 8, no special characters
    returns x as timestamp
        if x is null, returns string 'error', 
        if x is of a length other than 14 or 4, returns string 'error'.
    """
    if x > 0:
        x = str(round(x))
        if len(x) == 14: 
            return pd.to_datetime(x, format="%Y%m%d%H%M%S")
            
        elif len(x) == 8:
            return pd.to_datetime(x, format="%Y%m%d") 
                        
        else:
            return 'error'
    else:
        return 'error'
#----------------------------------------------------
import pandas as pd
#------------------drop_null_30----------------------
def drop_null_30(df):
    """
    drops all columns from input df with missing data of over 30%
    """
    percent_missing = round(df.isnull().sum() * 100 / len(df))
    missing_values = pd.DataFrame({'column_name': df.columns, 'percent_missing': percent_missing})
    
    cols_30 = missing_values[missing_values['percent_missing'] > 30].index
    df.drop(cols_30, inplace=True, axis = 1)
    return f'The following columns have been dropped: {cols_30}'
#-------------------------------------------------------
import requests
import time
#-----------------open_weather_api----------------------
def open_weather_api(lat, long, date, timezone = "America%2FLos_Angeles"):
    """
    Function returns individual api calls by location and date using the open weather api
    PARAMS:
    lat = latitude
    long = longitude
    date = YYYY-MM-DD as a string
    timezone = Continent/city
    """
    
    url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={long}&start_date={date}&end_date={date}&hourly=temperature_2m,relativehumidity_2m,windspeed_10m,windgusts_10m,et0_fao_evapotranspiration,vapor_pressure_deficit,soil_temperature_0_to_7cm,soil_temperature_7_to_28cm,soil_moisture_0_to_7cm,soil_moisture_7_to_28cm&daily=temperature_2m_max,temperature_2m_min,precipitation_sum,rain_sum,snowfall_sum&timezone={timezone}"
    
    response = requests.get(url)
    return response.json()
#----------------------------------------------------
import statistics 
#-----------------Weather Condition------------------    
#import statistics
#-------Weather Condition for Steamlit------------------    
def weather_condition(lat, long, date, timezone = "America%2FLos_Angeles"):
    """
    Function returns several meterological conditions for a single date and location. 
    PARAMS: 
    lat and long as int
    date = 2020-01-01 as string 
    Returns:
    Returns dictionary with the following:
        Features:
        Elevation (m)
        Maximum Temperature (2 m)
        Minimum Temperature (2 m)
        Precipitation Sum
        Rain Sum
        Snowfall Sum
        Temperature (2 m)
        Wind Gusts (10 m)
        Soil Temperature (0-7 cm)
        Soil Temperature (7-28 cm)
        Soil Moisture (0-7 cm)
        Soil Moisture (7-28 cm)
        
    Units:
        Temperature (°C)
        Windgusts (km/h)
        Evapotranspiration ()
        Moisture (m³/m³)
    """
    #call the weather api
    if lat and long:         
        json_result = open_weather_api(lat, long, date, timezone)
        elevation = float(json_result['elevation'])
        
        try:
            precip_sum = int(json_result['daily']['precipitation_sum'][0])              # mm        
        except:
            precip_sum = None
            
        if  precip_sum == 0:
            rain_sum = 0
            snow_sum = 0
        else:
            try:
                rain_sum = int(json_result['daily']['rain_sum'][0])                  # mm
            except: 
                rain_sum = None
            try:
                snow_sum = int(json_result['daily']['snowfall_sum'][0])              # cm, need to convert       
            except:
                snow_sum = None

        try:
            temp_max = int(json_result['daily']['temperature_2m_max'][0])              # celcius        
        except:
            temp_max = None
        try:
            temp_min = int(json_result['daily']['temperature_2m_min'][0])              # celcius        
        except:
            temp_min = None
        try:
            mean_temp_2m = int(statistics.mean(json_result['hourly']['temperature_2m']))              # celcius        
        except:
            mean_temp_2m = None           
        
        # Wind Gusts (10 m)
        try:
            mean_wind_10m = int(statistics.mean(json_result['hourly']['windgusts_10m']))              # km/h        
        except:
            mean_wind_10m = None   
        
        # Soil Temperature (0-7 cm)
        try:
            mean_soil_temp_7cm = int(statistics.mean(json_result['hourly']['soil_temperature_0_to_7cm']))              # celcius        
        except:
            mean_soil_temp_7cm = None  
            
        # Soil Temperature (7-28 cm)
        try:
            mean_soil_temp_28cm = int(statistics.mean(json_result['hourly']['soil_temperature_7_to_28cm']))              # celcius        
        except:
            mean_soil_temp_28cm = None 
        
        # Soil Moisture (0-7 cm)
        try:
            mean_soil_moist_7cm = int(statistics.mean(json_result['hourly']['soil_moisture_0_to_7cm']))              # m³/m³        
        except:
            mean_soil_moist_7cm = None 
        
        # Soil Moisture (7-28 cm)
        try:
            mean_soil_moist_28cm = int(statistics.mean(json_result['hourly']['soil_moisture_7_to_28cm']))              # m³/m³        
        except:
            mean_soil_moist_28cm = None        
            
        # Relative Humidity (2 m)
        # N/A
        # Wind Speed (10 m)
        # N/A          
        # Reference Evapotranspiration (ET₀)
        # N/A
        # Vapor Pressure Deficit
        # N/A
        
        result_dict = {'Elevation': elevation,
                       'Temperature (2 m)': mean_temp_2m,
                       'Wind Gusts (10 m)': mean_wind_10m, 
                       'Soil Temperature (0-7 cm)': mean_soil_temp_7cm, 
                       'Soil Temperature (7-28 cm)': mean_soil_temp_28cm,
                       'Soil Moisture (0-7 cm)': mean_soil_moist_7cm, 
                       'Soil Moisture (7-28 cm)': mean_soil_moist_28cm, 
                       'Maximum Temperature (2 m)': temp_max,
                       'Minimum Temperature (2 m)': temp_min, 
                       'Precipitation Sum': precip_sum, 
                       'Rain Sum': rain_sum, 
                       'Snowfall Sum': snow_sum
        }

        return result_dict
#-------------------------------------