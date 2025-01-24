import customtkinter as ctk
from datetime import datetime
import threading
import time
from weather_core import WeatherCore
import base64
import tempfile
import os

class WeatherApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Modern Weather App")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        
        # تنظیم آیکون برنامه
        self.set_app_icon()
        
        # تنظیم تم پیش‌فرض و رنگ‌ها
        self.is_dark_mode = False
        ctk.set_appearance_mode("light")
        self.setup_colors()
        
        self.weather_core = WeatherCore()
        self.setup_header()
        self.setup_gui()
        self.running = False

    def set_app_icon(self):
        """تنظیم آیکون برنامه"""
        # آیکون به صورت base64
        icon_data = """
        iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAA
        7AAAAOwBeShxvQAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAMASURBVFiF7ZZN
        iBtVGIafb2aSzGQymWQmu7Pr/nRXa10p/lAUqnXxUBD0IIqCUBQKngQP3r0IghfBkwh6Fg8iCFYUDxVE
        UGqFIq092KV2t9t1dzvJJJnM/H0eJtm4ye5m0pUIffeTgeTL+z7v9+bLd+Aa/u/QrkbIGPPsc8/0Xejr
        b9yXNxKxnR0dYRgSRRGu6xKGIVprms0mQRDgOA6u6xKGYfu5rmvCMCQIgrZGFEWEYYjrujiOQxAEbY3/
        hNaawWCQer3O7OwsDx+f4L4jR7F0RKVSplqtUiqVKBaLVCoVKpUKxWKRUqlEuVymUqlQKpUol8tUq1VK
        pRKVSoVyuUy1WqVcLlOr1ahWq5TLZer1OtVqlXK5TK1Wo1KpUKlU2N7eJooibMep1Wp0d3f/qxNaa3p7
        e+nt7WVwcJCBgQH6+/vp6+ujp6eH7u5uenp66O7upquri87OTrq6uujo6KC7u5vu7m46Ozvp6uqio6OD
        zs5OHMdhfX2dWq3G0tISs7OzTE9PMzU1xfT0NDMzM8zNzbG4uMjKygqbm5usr6+zs7NDEAQopZBSopRC
        KdX+llJijEFrjVIKYwxKKbTWGGPQWqOUQkqJlBKtNVJKjDHt2BiDlBKlFFJKoigiDEOUUkRRhFKKKIow
        xrSPbKUUxhiMMW2NKIowxrR/G2MwxrR/G2MwxrQbVEoRRRFRFBFFUfu7vQP7RZIkJEly4H2SJMRxTJIk
        xHFMkiQkSUIcx8RxTBzHJElCHMckSUIcx8RxTBzH7OzssLW1RaFQYGFhgfn5eRYWFpifn2dxcZGlpSVW
        V1fZ2NhgY2ODra0ttra22NzcZHt7m+3tbTY3N9na2mJra4utrS22t7fZ3Nxka2uLjY0NNjY22NzcZHNz
        k42NDba3t9ne3mZra4sgCNBaY/f09KCUQkqJMQatNcaY9sC11m1nWh601u2Taa3RWrfFW8IHxbXWSCnb
        J1NKobVuD7y1qFYjrQvVarT1rrVGKdVWa2m0Tm6MQSmFlLI98FYjLXf2N3kV+BPZvfTkag0HkwAAAABJ
        RU5ErkJggg==
        """
        
        # ذخیره آیکون در یک فایل موقت
        icon_data_decoded = base64.b64decode(icon_data)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ico')
        temp_file.write(icon_data_decoded)
        temp_file.close()
        
        # تنظیم آیکون
        self.root.iconbitmap(temp_file.name)
        
        # حذف فایل موقت
        os.unlink(temp_file.name)

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

        self.running = True
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.status_label.configure(text="Status: Running")
        
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
                city = self.city_entry.get()
                weather_data = self.weather_core.get_current_weather(city)
                
                self.temp_label.configure(text=f"Temperature: {weather_data['temp']}°C")
                self.humidity_label.configure(text=f"Humidity: {weather_data['humidity']}%")
                self.condition_label.configure(text=f"Condition: {weather_data['condition']}")
                self.time_label.configure(text=f"Last Update: {datetime.now().strftime('%H:%M:%S')}")
                
                self.status_label.configure(text="Status: Data updated successfully")
                
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
        """به‌روزرسانی رنگ‌های رابط کاربری"""
        # به‌روزرسانی دکمه‌ها
        self.theme_button.configure(
            fg_color=self.primary_color,
            hover_color=self.secondary_color
        )
        self.start_button.configure(
            fg_color=self.primary_color,
            hover_color=self.secondary_color
        )
        
        # به‌روزرسانی رنگ متن‌ها
        for widget in [self.temp_label, self.humidity_label, 
                      self.condition_label, self.time_label,
                      self.status_label, self.title_label]:
            widget.configure(text_color=self.text_color)

def main():
    app = WeatherApp()
    app.root.mainloop()

if __name__ == "__main__":
    main() 