import customtkinter as ctk
from datetime import datetime
import threading
import time
from weather_core import WeatherCore
import base64
import tempfile
import os
from PIL import Image, ImageTk

class WeatherApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Modern Weather App")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        
        # تنظیم آیکون برنامه
        icon_path = "weather_icon.png"  # فایل آیکون باید در همین مسیر باشه
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        
        # تنظیم تم پیش‌فرض و رنگ‌ها
        self.is_dark_mode = False
        ctk.set_appearance_mode("light")
        self.setup_colors()
        
        self.weather_core = WeatherCore()
        self.setup_header()
        self.setup_gui()
        self.running = False

    def setup_colors(self):
        """تنظیم پالت رنگی برنامه"""
        if self.is_dark_mode:
            self.primary_color = "#4f46e5"
            self.secondary_color = "#3730a3"
            self.accent_color = "#818cf8"
            self.text_color = "#ffffff"
            self.bg_color = "#1e1b4b"
        else:
            self.primary_color = "#3731de"
            self.secondary_color = "#2563eb"
            self.accent_color = "#60a5fa"
            self.text_color = "#1e293b"
            self.bg_color = "#ffffff"

    def setup_gui(self):
        # کانتینر اصلی با پدینگ
        container = ctk.CTkFrame(self.root, fg_color="transparent")
        container.pack(fill="both", expand=True, padx=20, pady=10)
        
        # کارت اصلی
        main_card = ctk.CTkFrame(
            container,
            fg_color=self.bg_color,
            corner_radius=15,
            border_width=1,
            border_color=self.accent_color
        )
        main_card.pack(fill="x", pady=10)
        
        # بخش ورودی با طراحی جدید
        input_frame = ctk.CTkFrame(main_card, fg_color="transparent")
        input_frame.pack(fill="x", padx=15, pady=15)
        
        city_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        city_frame.pack(fill="x", pady=5)
        
        city_label = ctk.CTkLabel(
            city_frame,
            text="City",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.text_color
        )
        city_label.pack(side="left")
        
        self.city_entry = ctk.CTkEntry(
            city_frame,
            placeholder_text="Enter city name",
            height=35,
            corner_radius=8,
            border_color=self.accent_color
        )
        self.city_entry.pack(side="right", fill="x", expand=True, padx=(10, 0))
        self.city_entry.insert(0, "Tehran")
        
        refresh_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        refresh_frame.pack(fill="x", pady=5)
        
        refresh_label = ctk.CTkLabel(
            refresh_frame,
            text="Refresh Interval",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=self.text_color
        )
        refresh_label.pack(side="left")
        
        self.refresh_entry = ctk.CTkEntry(
            refresh_frame,
            placeholder_text="Seconds",
            height=35,
            corner_radius=8,
            border_color=self.accent_color,
            width=100
        )
        self.refresh_entry.pack(side="right", padx=(10, 0))
        self.refresh_entry.insert(0, "60")
        
        # کارت نمایش اطلاعات
        info_card = ctk.CTkFrame(
            container,
            fg_color=self.bg_color,
            corner_radius=15,
            border_width=1,
            border_color=self.accent_color
        )
        info_card.pack(fill="x", pady=10)
        
        # عنوان کارت
        card_title = ctk.CTkLabel(
            info_card,
            text="Weather Information",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=self.text_color
        )
        card_title.pack(pady=(15, 10))
        
        # اطلاعات آب و هوا
        self.temp_label = ctk.CTkLabel(
            info_card,
            text="Temperature: --°C",
            font=ctk.CTkFont(size=24),
            text_color=self.text_color
        )
        self.temp_label.pack(pady=5)
        
        self.humidity_label = ctk.CTkLabel(
            info_card,
            text="Humidity: --%",
            font=ctk.CTkFont(size=18),
            text_color=self.text_color
        )
        self.humidity_label.pack(pady=5)
        
        self.condition_label = ctk.CTkLabel(
            info_card,
            text="Condition: --",
            font=ctk.CTkFont(size=18),
            text_color=self.text_color
        )
        self.condition_label.pack(pady=5)
        
        self.time_label = ctk.CTkLabel(
            info_card,
            text="Last Update: --:--:--",
            font=ctk.CTkFont(size=12),
            text_color=self.text_color
        )
        self.time_label.pack(pady=(5, 15))
        
        # دکمه‌های کنترل
        button_frame = ctk.CTkFrame(container, fg_color="transparent")
        button_frame.pack(pady=15)
        
        self.start_button = ctk.CTkButton(
            button_frame,
            text="Start Monitoring",
            command=self.start_monitoring,
            fg_color=self.primary_color,
            hover_color=self.secondary_color,
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_button.pack(side="left", padx=5)
        
        self.stop_button = ctk.CTkButton(
            button_frame,
            text="Stop",
            command=self.stop_monitoring,
            fg_color="#666666",
            hover_color="#555555",
            height=40,
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5)
        
        # وضعیت
        self.status_label = ctk.CTkLabel(
            container,
            text="Status: Ready",
            font=ctk.CTkFont(size=12),
            text_color=self.text_color
        )
        self.status_label.pack(pady=5)

    def start_monitoring(self):
        try:
            self.refresh_time = int(self.refresh_entry.get())
            if self.refresh_time < 30:
                raise ValueError("Refresh time must be at least 30 seconds")
        except ValueError as e:
            self.status_label.configure(text=f"Error: {str(e)}")
            return
        
        self.city = self.city_entry.get().strip()
        if not self.city:
            self.status_label.configure(text="Error: Please enter a city name")
            return
        
        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Status: Monitoring...")
        
        self.monitor_thread = threading.Thread(target=self.monitor_weather)
        self.monitor_thread.daemon = True
        self.monitor_thread.start()

    def stop_monitoring(self):
        self.running = False
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.status_label.configure(text="Status: Stopped")

    def monitor_weather(self):
        while self.running:
            try:
                weather_data = self.weather_core.get_current_weather(self.city)
                
                self.temp_label.configure(text=f"Temperature: {weather_data['temp']}°C")
                self.humidity_label.configure(text=f"Humidity: {weather_data['humidity']}%")
                self.condition_label.configure(text=f"Condition: {weather_data['condition']}")
                self.time_label.configure(text=f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
                self.status_label.configure(text="Status: Updated successfully")
                
            except Exception as e:
                self.status_label.configure(text=f"Error: {str(e)}")
            
            time.sleep(self.refresh_time)

    def setup_header(self):
        header = ctk.CTkFrame(self.root, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=10)
        
        # لوگو و عنوان
        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left")
        
        self.title_label = ctk.CTkLabel(
            title_frame,
            text="Weather Monitor",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.text_color
        )
        self.title_label.pack(side="left")
        
        # دکمه تغییر تم
        self.theme_button = ctk.CTkButton(
            header,
            text="🌓",
            width=40,
            height=40,
            command=self.toggle_theme,
            fg_color=self.primary_color,
            hover_color=self.secondary_color,
            corner_radius=20
        )
        self.theme_button.pack(side="right")

    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        new_mode = "dark" if self.is_dark_mode else "light"
        ctk.set_appearance_mode(new_mode)
        
        self.setup_colors()
        self.refresh_ui()

    def refresh_ui(self):
        self.theme_button.configure(
            fg_color=self.primary_color,
            hover_color=self.secondary_color
        )
        self.start_button.configure(
            fg_color=self.primary_color,
            hover_color=self.secondary_color
        )
        
        # به‌روزرسانی همه لیبل‌ها
        for widget in [
            self.temp_label, 
            self.humidity_label, 
            self.condition_label, 
            self.time_label,
            self.status_label,
            self.title_label,
            self.city_label,
            self.refresh_label,
            self.card_title
        ]:
            widget.configure(text_color=self.text_color)

def main():
    app = WeatherApp()
    app.root.mainloop()

if __name__ == "__main__":
    main() 