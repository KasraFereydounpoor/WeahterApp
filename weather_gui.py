import customtkinter as ctk
import threading
import sqlite3
import time
from datetime import datetime
import webbrowser
from weather_core import WeatherCore
from tkinter import messagebox  # برای نمایش خطا
from PIL import Image
import os

# تنظیم تم پیش‌فرض و رنگ‌ها
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class WeatherApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Weather App")
        self.root.geometry("400x700")  # افزایش ارتفاع برای جا دادن همه المان‌ها
        self.root.resizable(False, False)
        
        self.primary_color = "#3731de"
        
        # لود کردن آیکون‌ها
        self.load_weather_icons()
        
        self.weather_core = WeatherCore()
        self.setup_header()  # اضافه کردن هدر
        self.setup_gui()
        self.running = False

    def load_weather_icons(self):
        """لود کردن آیکون‌های مختلف وضعیت هوا"""
        icon_size = (30, 30)  # سایز آیکون‌ها
        icons_path = "icons"  # پوشه حاوی آیکون‌ها
        
        self.weather_icons = {
            "Clear": self.load_icon(os.path.join(icons_path, "clear.png"), icon_size),
            "Clouds": self.load_icon(os.path.join(icons_path, "cloudy.png"), icon_size),
            "Rain": self.load_icon(os.path.join(icons_path, "rain.png"), icon_size),
            "Drizzle": self.load_icon(os.path.join(icons_path, "drizzle.png"), icon_size),
            "Thunderstorm": self.load_icon(os.path.join(icons_path, "thunderstorm.png"), icon_size),
            "Snow": self.load_icon(os.path.join(icons_path, "snow.png"), icon_size),
            "Mist": self.load_icon(os.path.join(icons_path, "mist.png"), icon_size),
            "default": self.load_icon(os.path.join(icons_path, "default.png"), icon_size)
        }

    def load_icon(self, path, size):
        """لود و ریسایز کردن آیکون"""
        try:
            return ctk.CTkImage(
                light_image=Image.open(path),
                dark_image=Image.open(path),
                size=size
            )
        except Exception as e:
            print(f"Error loading icon {path}: {e}")
            return None

    def setup_header(self):
        """اضافه کردن بخش هدر شامل اطلاعات توسعه‌دهنده"""
        header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(10, 0))
        
        # اطلاعات توسعه‌دهنده
        dev_label = ctk.CTkLabel(
            header_frame,
            text="Developed by Kasra Fereydounpoor",
            font=ctk.CTkFont(size=12)
        )
        dev_label.pack(side="left", pady=5)
        
        # دکمه گیتهاب
        github_button = ctk.CTkButton(
            header_frame,
            text="GitHub",
            command=self.open_github,
            fg_color=self.primary_color,
            hover_color="#2820cb",
            width=70,
            height=25
        )
        github_button.pack(side="right", pady=5)

    def setup_gui(self):
        # فریم اصلی
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(padx=20, pady=10, fill="both", expand=True)
        
        # عنوان برنامه
        title_label = ctk.CTkLabel(
            main_frame,
            text="Weather Monitor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=10)
        
        # فریم ورودی‌ها
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", pady=10)
        
        # City input
        city_label = ctk.CTkLabel(input_frame, text="City:")
        city_label.pack(pady=5)
        self.city_var = ctk.StringVar(value="Tehran")
        self.city_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.city_var,
            placeholder_text="Enter city name"
        )
        self.city_entry.pack(pady=5, padx=20, fill="x")
        
        # Interval input
        interval_label = ctk.CTkLabel(input_frame, text="Update Interval (seconds):")
        interval_label.pack(pady=5)
        self.interval_var = ctk.StringVar(value="5")
        self.interval_entry = ctk.CTkEntry(
            input_frame,
            textvariable=self.interval_var,
            placeholder_text="Enter update interval"
        )
        self.interval_entry.pack(pady=5, padx=20, fill="x")
        
        # Weather info display with icons
        self.info_frame = ctk.CTkFrame(main_frame)
        self.info_frame.pack(pady=15, fill="x")
        
        info_title = ctk.CTkLabel(
            self.info_frame,
            text="Weather Information",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        info_title.pack(pady=10)
        
        # فریم برای نمایش دما و آیکون کنار هم
        temp_frame = ctk.CTkFrame(self.info_frame, fg_color="transparent")
        temp_frame.pack(fill="x", padx=20)
        
        self.weather_icon_label = ctk.CTkLabel(temp_frame, text="", image=None)
        self.weather_icon_label.pack(side="left", padx=5)
        
        self.temp_label = ctk.CTkLabel(temp_frame, text="Temperature: --")
        self.temp_label.pack(side="left", padx=5)
        
        self.humidity_label = ctk.CTkLabel(self.info_frame, text="Humidity: --")
        self.humidity_label.pack(pady=5)
        
        self.condition_label = ctk.CTkLabel(self.info_frame, text="Condition: --")
        self.condition_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(self.info_frame, text="Last Update: --")
        self.time_label.pack(pady=5)
        
        # اضافه کردن بخش پیش‌بینی
        self.forecast_frame = ctk.CTkFrame(main_frame)
        self.forecast_frame.pack(pady=15, fill="x")
        
        forecast_title = ctk.CTkLabel(
            self.forecast_frame,
            text="2-Day Forecast",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        forecast_title.pack(pady=5)
        
        # فریم‌های روزهای آینده
        self.forecast_days = []
        for _ in range(2):
            day_frame = ctk.CTkFrame(self.forecast_frame, fg_color="transparent")
            day_frame.pack(fill="x", padx=10, pady=2)
            
            day_label = ctk.CTkLabel(day_frame, text="--", font=ctk.CTkFont(size=12))
            day_label.pack(side="left", padx=5)
            
            icon_label = ctk.CTkLabel(day_frame, text="", image=None)
            icon_label.pack(side="right", padx=5)
            
            temp_label = ctk.CTkLabel(day_frame, text="--°C", font=ctk.CTkFont(size=12))
            temp_label.pack(side="right", padx=5)
            
            desc_label = ctk.CTkLabel(day_frame, text="--", font=ctk.CTkFont(size=12))
            desc_label.pack(side="right", padx=5)
            
            self.forecast_days.append({
                'day': day_label,
                'icon': icon_label,
                'temp': temp_label,
                'desc': desc_label
            })
        
        # Control buttons - اطمینان از نمایش درست دکمه‌ها
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=15)  # کاهش فاصله
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Monitoring",
            command=self.start_monitoring,
            fg_color=self.primary_color,
            hover_color="#2820cb",
            width=150
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop",
            command=self.stop_monitoring,
            fg_color="#666666",
            hover_color="#555555",
            width=150,
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # Status - انتقال به پایین‌ترین بخش
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="Status: Ready",
            font=ctk.CTkFont(size=12)
        )
        self.status_label.pack(pady=(5, 10))

    def open_github(self):
        webbrowser.open("https://github.com/KasraFereydounpoor")

    def validate_inputs(self):
        """اعتبارسنجی ورودی‌ها"""
        try:
            interval = self.interval_var.get().strip()
            if not interval:
                raise ValueError("Please enter an update interval")
            
            interval_val = int(interval)
            if interval_val <= 0:
                raise ValueError("Interval must be a positive number")
            
            city = self.city_var.get().strip()
            if not city:
                raise ValueError("Please enter a city name")
                
            return True
            
        except ValueError as e:
            self.show_error("Input Error", str(e))
            return False

    def update_weather(self):
        while self.running:
            try:
                city = self.city_var.get().strip()
                # دریافت داده‌های فعلی
                current_data = self.weather_core.get_weather_data(city)
                
                if current_data:
                    # دریافت پیش‌بینی
                    forecast_data = self.weather_core.get_forecast_data(city)
                    # آپدیت UI با هر دو داده
                    self.root.after(0, self.update_ui, current_data, forecast_data)
                    
                    with sqlite3.connect("weather.db") as con:
                        cur = con.cursor()
                        self.weather_core.insert_data(con, cur, current_data)
                
                interval = int(self.interval_var.get().strip())
                time.sleep(interval)
            
            except Exception as e:
                self.root.after(0, self.show_error, "Error", str(e))
                self.root.after(0, self.stop_monitoring)
                break

    def update_ui(self, current_data, forecast_data=None):
        """به‌روزرسانی رابط کاربری با آیکون‌ها"""
        # آپدیت وضعیت فعلی
        self.temp_label.configure(text=f"Temperature: {current_data['temp']}°C")
        self.humidity_label.configure(text=f"Humidity: {current_data['humidity']}%")
        self.condition_label.configure(text=f"Condition: {current_data['condition']}")
        self.time_label.configure(text=f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
        
        # آپدیت آیکون وضعیت فعلی
        condition = current_data.get('condition', 'default')
        icon = self.weather_icons.get(condition, self.weather_icons['default'])
        if icon:
            self.weather_icon_label.configure(image=icon)
        
        # آپدیت پیش‌بینی با آیکون‌ها
        if forecast_data:
            for i, forecast in enumerate(forecast_data):
                self.forecast_days[i]['day'].configure(text=forecast['date'])
                self.forecast_days[i]['temp'].configure(text=f"{forecast['temp']}°C")
                self.forecast_days[i]['desc'].configure(text=forecast['description'])
                
                # آپدیت آیکون پیش‌بینی
                icon = self.weather_icons.get(forecast['description'], self.weather_icons['default'])
                if icon:
                    self.forecast_days[i]['icon'].configure(image=icon)

    def show_error(self, title, message):
        """نمایش خطا با استفاده از messagebox"""
        messagebox.showerror(title, message)

    def start_monitoring(self):
        if not self.validate_inputs():
            return
            
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        
        self.weather_thread = threading.Thread(target=self.update_weather)
        self.weather_thread.daemon = True
        self.weather_thread.start()

    def stop_monitoring(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Status: Stopped")

    def on_closing(self):
        """مدیریت بستن پنجره"""
        self.running = False
        self.root.destroy()

def main():
    app = WeatherApp()
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)  # مدیریت بستن پنجره
    app.root.mainloop()

if __name__ == "__main__":
    main() 