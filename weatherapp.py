import requests 
import time 
import sqlite3
import logging

#logging settings
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='weather_app.log'
)

def sql_connector():
    #connector for database and  cursor 
    con = sqlite3.connect("weather.db")
    cur = con.cursor()
    return con,cur

def create_table(con , cur):
    cur.execute("CREATE TABLE IF NOT EXISTS weather(name TEXT, datetime TEXT , temp TEXT , humidity TEXT)")
    con.commit()


def insert_data(con,cur,data):
    cur.execute("INSERT INTO weather values(?,?,?,?)" , tuple([v for k,v in data.items()]))
    con.commit()

def proccess_data(data):
    temp_kelvin = float(data['main']['temp'])
    temp_celsius = temp_kelvin - 273.15  # kelvin to celsius
    return {
        "city": data['name'],
        "datetime": time.ctime(int(data['dt'])),
        "temp": f"{temp_celsius:.1f}",
        "humidity": data['main']['humidity']
    }


def get_weather_data(city='Tehran', appid='24ebee4c281907fa73640f7e3f5dd073'):
    URL = "https://api.openweathermap.org/data/2.5/weather"
    PARAMS = {'q':city , 'appid':appid}
    try:
        r = requests.get(url=URL, params=PARAMS)
        r.raise_for_status()
        logging.info(f"Weather data for city {city} successfully received")
        return proccess_data(r.json())
    except requests.exceptions.RequestException as e:
        logging.error(f"Error getting weather data: {e}")
        print(f"Error getting weather data: {e}")
        return None

def main():
    city = input("Enter city name (default: Tehran): ") or "Tehran"
    interval = int(input("Enter time interval between requests in seconds (default: 5): ") or "5")
    
    with sqlite3.connect("weather.db") as con:
        cur = con.cursor()
        create_table(con, cur)
        
        try:
            logging.info(f"Program started for city {city} with interval of {interval} seconds")
            while True:
                data_weather = get_weather_data(city)
                if data_weather:
                    insert_data(con, cur, data_weather)
                    print(data_weather)
                time.sleep(interval)
        except KeyboardInterrupt:
            logging.info("Program stopped by user")
            print("\nProgram stopped.")

# https://github.com/KasraFereydounpoor