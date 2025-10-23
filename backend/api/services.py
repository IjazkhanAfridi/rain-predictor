import requests
from datetime import datetime, timedelta


class RainPredictionService:
    BASE_URL = "https://api.open-meteo.com/v1/forecast"
    GEOCODING_URL = "https://geocoding-api.open-meteo.com/v1/search"
    
    @classmethod
    def get_coordinates(cls, location):
        try:
            params = {
                'name': location,
                'count': 1,
                'language': 'en',
                'format': 'json'
            }
            response = requests.get(cls.GEOCODING_URL, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                return result['latitude'], result['longitude']
            return None, None
        except Exception as e:
            print(f"Error getting coordinates: {e}")
            return None, None
    
    @classmethod
    def get_weather_forecast(cls, latitude, longitude, date):
        try:
            if isinstance(date, datetime):
                date_str = date.strftime('%Y-%m-%d')
            else:
                date_str = str(date)
            
            today = datetime.now().date()
            target_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            
            params = {
                'latitude': latitude,
                'longitude': longitude,
                'daily': 'precipitation_sum,precipitation_probability_max,weathercode',
                'timezone': 'auto',
                'start_date': date_str,
                'end_date': date_str
            }
            
            response = requests.get(cls.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
        except Exception as e:
            print(f"Error getting weather forecast: {e}")
            return None
    
    @classmethod
    def predict_rain(cls, location, date):
        latitude, longitude = cls.get_coordinates(location)
        
        if latitude is None or longitude is None:
            return {
                'success': False,
                'error': 'Location not found',
                'prediction': 'Unknown',
                'confidence': 0.0,
                'weather_data': None
            }
        
        weather_data = cls.get_weather_forecast(latitude, longitude, date)
        
        if weather_data is None:
            return {
                'success': False,
                'error': 'Unable to fetch weather data',
                'prediction': 'Unknown',
                'confidence': 0.0,
                'weather_data': None
            }
        
        try:
            daily = weather_data.get('daily', {})
            precipitation_sum = daily.get('precipitation_sum', [0])[0]
            precipitation_probability = daily.get('precipitation_probability_max', [0])[0]
            weathercode = daily.get('weathercode', [0])[0]
            
            rain_codes = [51, 53, 55, 56, 57, 61, 63, 65, 66, 67, 80, 81, 82, 95, 96, 99]
            will_rain = weathercode in rain_codes or precipitation_sum > 0.1
            
            if precipitation_probability is not None and precipitation_probability > 0:
                confidence = precipitation_probability / 100.0
            elif precipitation_sum > 0:
                confidence = min(0.5 + (precipitation_sum / 10.0), 1.0)
            else:
                confidence = 0.1
            
            prediction = "Rain" if will_rain else "No Rain"
            
            return {
                'success': True,
                'prediction': prediction,
                'confidence': round(confidence, 2),
                'weather_data': {
                    'location': location,
                    'latitude': latitude,
                    'longitude': longitude,
                    'date': str(date),
                    'precipitation_sum': precipitation_sum,
                    'precipitation_probability': precipitation_probability,
                    'weathercode': weathercode
                }
            }
        except Exception as e:
            print(f"Error parsing weather data: {e}")
            return {
                'success': False,
                'error': f'Error parsing weather data: {str(e)}',
                'prediction': 'Unknown',
                'confidence': 0.0,
                'weather_data': weather_data
            }
