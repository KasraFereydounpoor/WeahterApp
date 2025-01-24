import requests 
import time 
import sqlite3
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='weather_app.log'
)

class WeatherCore:
    def __init__(self):
        self.setup_database()
    
    def setup_database(self):
        with sqlite3.connect("weather.db") as con:
            cur = con.cursor()
            self.create_table(con, cur)
    
    @staticmethod
    def create_table(con, cur):
        cur.execute("CREATE TABLE IF NOT EXISTS weather(name TEXT, datetime TEXT, temp TEXT, humidity TEXT)")
        con.commit()
    
    @staticmethod
    def insert_data(con, cur, data):
        cur.execute("INSERT INTO weather VALUES(?,?,?,?)", tuple([v for k,v in data.items()]))
        con.commit()
    
    @staticmethod
    def process_data(data):
        temp_kelvin = float(data['main']['temp'])
        temp_celsius = temp_kelvin - 273.15
        return {
            "city": data['name'],
            "datetime": time.ctime(int(data['dt'])),
            "temp": f"{temp_celsius:.1f}",
            "humidity": data['main']['humidity'],
            "condition": data['weather'][0]['main']
        }
    
    def get_weather_data(self, city='Tehran', appid='24ebee4c281907fa73640f7e3f5dd073'):
        URL = "https://api.openweathermap.org/data/2.5/weather"
        PARAMS = {'q':city, 'appid':appid}
        try:
            r = requests.get(url=URL, params=PARAMS)
            r.raise_for_status()
            logging.info(f"Weather data for city {city} successfully received")
            return self.process_data(r.json())
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting weather data: {e}")
            raise 

    def get_forecast_data(self, city='Tehran', appid='24ebee4c281907fa73640f7e3f5dd073'):
        """Get 3-day forecast data"""
        URL = "https://api.openweathermap.org/data/2.5/forecast"
        PARAMS = {'q': city, 'appid': appid}
        try:
            r = requests.get(url=URL, params=PARAMS)
            r.raise_for_status()
            logging.info(f"Forecast data for city {city} successfully received")
            return self.process_forecast_data(r.json())
        except requests.exceptions.RequestException as e:
            logging.error(f"Error getting forecast data: {e}")
            raise

    def process_forecast_data(self, data):
        """Process forecast data for next 2 days"""
        forecasts = []
        # گروه‌بندی بر اساس روز
        daily_forecasts = {}
        
        for item in data['list'][:16]:  # 16 تا برای 2 روز آینده (هر 3 ساعت یک پیش‌بینی)
            temp_celsius = float(item['main']['temp']) - 273.15
            date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
            
            if date not in daily_forecasts:
                daily_forecasts[date] = {
                    'temps': [],
                    'descriptions': [],
                    'date': date
                }
            
            daily_forecasts[date]['temps'].append(temp_celsius)
            daily_forecasts[date]['descriptions'].append(item['weather'][0]['main'])
        
        # محاسبه میانگین دما و وضعیت غالب هوا برای هر روز
        for date, data in daily_forecasts.items():
            avg_temp = sum(data['temps']) / len(data['temps'])
            most_common_desc = max(set(data['descriptions']), key=data['descriptions'].count)
            forecasts.append({
                'date': datetime.strptime(date, '%Y-%m-%d').strftime('%A'),  # نام روز هفته
                'temp': f"{avg_temp:.1f}",
                'description': most_common_desc
            })
        
        return forecasts[:2]  # فقط 2 روز آینده 