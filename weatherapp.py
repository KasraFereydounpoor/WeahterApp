import requests 
import time 
import sqlite3

def sql_connector():
    #connector for database and  cursor 
    con = sqlite3.connect("weather.db")
    cur = con.cursosr()
    return con,cur

def create_table(con , cur):
    cur.excute("CREATE TABLE IF NOT EXISTS weather(name TEXT, datetime TEXT , temp TEXT , humidity TEXT)")
    con.commit()


def insert_data(con,cur,data):
    
    cur.excute("INSET INTO wather values(?,?,?,?)" , entity)
    con.commit()

def proccess_data(data):
    return {}


def get_weather_data(city='Tehran', appid='24ebee4c281907fa73640f7e3f5dd073'):
    

con , cur = sql_connector()
city = 'Tehran'
app_id = '24ebee4c281907fa73640f7e3f5dd073'

URL =  