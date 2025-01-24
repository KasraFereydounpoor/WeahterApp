import tkinter as tk
from tkinter import ttk, messagebox
import threading
import sqlite3
import time
from datetime import datetime
from weather_core import WeatherCore

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("400x500")
        
        self.weather_core = WeatherCore()
        self.setup_gui()
        self.running = False
        
    def setup_gui(self):
        # City input
        ttk.Label(self.root, text="City:").pack(pady=5)
        self.city_var = tk.StringVar(value="Tehran")
        ttk.Entry(self.root, textvariable=self.city_var).pack(pady=5)
        
        # Interval input
        ttk.Label(self.root, text="Update Interval (seconds):").pack(pady=5)
        self.interval_var = tk.StringVar(value="5")
        ttk.Entry(self.root, textvariable=self.interval_var).pack(pady=5)
        
        # Weather info display
        self.info_frame = ttk.LabelFrame(self.root, text="Weather Information")
        self.info_frame.pack(pady=10, padx=10, fill="x")
        
        self.temp_label = ttk.Label(self.info_frame, text="Temperature: --")
        self.temp_label.pack(pady=5)
        
        self.humidity_label = ttk.Label(self.info_frame, text="Humidity: --")
        self.humidity_label.pack(pady=5)
        
        self.time_label = ttk.Label(self.info_frame, text="Last Update: --")
        self.time_label.pack(pady=5)
        
        # Control buttons
        self.start_button = ttk.Button(self.root, text="Start", command=self.start_monitoring)
        self.start_button.pack(pady=10)
        
        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop_monitoring, state="disabled")
        self.stop_button.pack(pady=5)
        
        # Status
        self.status_label = ttk.Label(self.root, text="Status: Ready")
        self.status_label.pack(pady=10)

    def update_weather(self):
        while self.running:
            try:
                city = self.city_var.get()
                data = self.weather_core.get_weather_data(city)
                
                if data:
                    self.temp_label.config(text=f"Temperature: {data['temp']}°C")
                    self.humidity_label.config(text=f"Humidity: {data['humidity']}%")
                    self.time_label.config(text=f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
                    
                    with sqlite3.connect("weather.db") as con:
                        cur = con.cursor()
                        self.weather_core.insert_data(con, cur, data)
                    
                    self.status_label.config(text="Status: Running")
                
                interval = int(self.interval_var.get())
                time.sleep(interval)
            
            except Exception as e:
                messagebox.showerror("Error", str(e))
                self.stop_monitoring()
                break

    def start_monitoring(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        
        self.weather_thread = threading.Thread(target=self.update_weather)
        self.weather_thread.daemon = True
        self.weather_thread.start()

    def stop_monitoring(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.status_label.config(text="Status: Stopped")

def main():
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()

if __name__ == "__main__":
    main() 