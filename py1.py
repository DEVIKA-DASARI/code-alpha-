import tkinter as tk
from tkinter import ttk, messagebox
import requests
import folium
from io import BytesIO
from PIL import Image, ImageTk
import matplotlib.pyplot as plt

def fetch_geolocation(ip):
    try:
        response = requests.get(f"https://ipapi.co/{ip}/json/")
        return response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Error fetching data: {e}")
        return None

def display_location_on_map(lat, lon):
    map_ = folium.Map(location=[lat, lon], zoom_start=10)
    folium.Marker([lat, lon]).add_to(map_)
    map_data = map_._to_png(5)
    return Image.open(BytesIO(map_data))

def on_search():
    ip = ip_entry.get()
    data = fetch_geolocation(ip)
    if data:
        city = data.get("city", "Unknown")
        country = data.get("country_name", "Unknown")
        lat = data.get("latitude", 0)
        lon = data.get("longitude", 0)
        result_label.config(text=f"Location: {city}, {country}\nLatitude: {lat}, Longitude: {lon}")
        map_image = display_location_on_map(lat, lon)
        map_photo = ImageTk.PhotoImage(map_image)
        map_label.config(image=map_photo)
        map_label.image = map_photo

        # Plot a bar graph of latitude and longitude
        plt.figure(figsize=(5, 3))
        plt.bar(["Latitude", "Longitude"], [lat, lon], color=['blue', 'green'])
        plt.ylabel("Degrees")
        plt.title("Geolocation Coordinates")
        plt.tight_layout()
        plt.show()

def create_gradient(canvas, width, height, color1, color2):
    # Create a gradient by drawing many small rectangles
    steps = 100
    for i in range(steps):
        r = int(color1[1:3], 16) + (int(color2[1:3], 16) - int(color1[1:3], 16)) * i // steps
        g = int(color1[3:5], 16) + (int(color2[3:5], 16) - int(color1[3:5], 16)) * i // steps
        b = int(color1[5:7], 16) + (int(color2[5:7], 16) - int(color1[5:7], 16)) * i // steps
        color = f'#{r:02x}{g:02x}{b:02x}'
        canvas.create_rectangle(0, i * height // steps, width, (i + 1) * height // steps, outline="", fill=color)



app = tk.Tk()
app.title("IP Geolocation Finder")

app.geometry("500x400")
# Create a canvas for gradient background
canvas = tk.Canvas(app, width=500, height=400)
canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
create_gradient(canvas, 500, 400, "#ff7f50", "#6a5acd")

frame = ttk.Frame(app, padding=10)
frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

ip_label = ttk.Label(frame, text="Enter IP Address:")
ip_label.grid(row=0, column=0, padx=5, pady=5)

ip_entry = ttk.Entry(frame, width=20)
ip_entry.grid(row=0, column=1, padx=5, pady=5)

search_button = ttk.Button(frame, text="Search", command=on_search)
search_button.grid(row=0, column=2, padx=5, pady=5)

result_label = ttk.Label(frame, text="")
result_label.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

map_label = ttk.Label(frame)
map_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

app.mainloop()
