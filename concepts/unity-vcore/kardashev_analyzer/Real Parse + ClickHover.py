import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Polygon
import json
import os
from decimal import Decimal

class MarkhamDashboard(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Markham Excellence Framework - Secure Offline Mode")
        self.geometry("1600x1000")
        self.configure(bg="#f0f0f0")
        
        # Load Real GeoJSON
        self.geo_data = {
            "Bicycle_Routes": self.load_geojson("Bicycle_Routes.geojson"),
            "Parks": self.load_geojson("Parks.geojson"),
            "Fire_Stations": self.load_geojson("Fire_Stations.geojson"),
            "Special_Areas": self.load_geojson("Site_Plan_Control_-_Special_Areas.geojson")
        }
        
        self.layer_vars = {key: tk.BooleanVar(value=True) for key in self.geo_data}
        
        self.create_widgets()
        
    def load_geojson(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            messagebox.showinfo("Loaded", f"{filename} parsed")
            return data
        except Exception as e:
            messagebox.showwarning("Error", f"{filename} issue: {e}—mock")
            return {"features": []}
        
    def create_widgets(self):
        # Header/Tree/Alerts (prior)
        # ...
        
        # Interactive Map Panel
        map_frame = tk.LabelFrame(main_panes, text="Markham Interactive Map (Click/Hover Features)", font=("Helvetica", 12, "bold"))
        main_panes.add(map_frame, weight=3)
        
        self.fig, self.ax = plt.subplots(figsize=(12, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, map_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        toolbar = NavigationToolbar2Tk(self.canvas, map_frame)
        toolbar.update()
        
        # Click/Hover Events
        self.canvas.mpl_connect('pick_event', self.on_map_click)
        self.canvas.mpl_connect('motion_notify_event', self.on_map_hover)
        
        # Layer Controls
        controls = tk.Frame(map_frame)
        controls.pack(fill="x")
        for layer, var in self.layer_vars.items():
            tk.Checkbutton(controls, text=layer.replace("_", " "), variable=var, command=self.plot_map).pack(side="left")
        
        self.plot_map()
        
        # Actions (prior)
        
    def plot_map(self):
        self.ax.clear()
        plotted = []
        
        if self.layer_vars["Bicycle_Routes"].get():
            for feature in self.geo_data["Bicycle_Routes"]["features"]:
                if feature["geometry"]["type"] == "LineString":
                    coords = feature["geometry"]["coordinates"]
                    line, = self.ax.plot([c[0] for c in coords], [c[1] for c in coords], 'g-', linewidth=2, picker=True, pickradius=5)
                    line.feature = feature
                    plotted.append("Bike Routes")
        
        if self.layer_vars["Parks"].get():
            for feature in self.geo_data["Parks"]["features"]:
                if feature["geometry"]["type"] == "Polygon":
                    for ring in feature["geometry"]["coordinates"]:
                        poly = Polygon(ring, facecolor='green', alpha=0.3, picker=True)
                        self.ax.add_patch(poly)
                        poly.feature = feature
                    plotted.append("Parks")
        
        if self.layer_vars["Fire_Stations"].get():
            for feature in self.geo_data["Fire_Stations"]["features"]:
                if feature["geometry"]["type"] == "Point":
                    lon, lat = feature["geometry"]["coordinates"]
                    point = self.ax.plot(lon, lat, 'r^', markersize=12, picker=True, pickradius=10)[0]
                    point.feature = feature
                    plotted.append("Fire Stations")
        
        if self.layer_vars["Special_Areas"].get():
            for feature in self.geo_data["Special_Areas"]["features"]:
                if feature["geometry"]["type"] == "Polygon":
                    for ring in feature["geometry"]["coordinates"]:
                        poly = Polygon(ring, facecolor='blue', alpha=0.2, picker=True)
                        self.ax.add_patch(poly)
                        poly.feature = feature
                    plotted.append("Special Areas")
        
        self.ax.set_title("Markham Map - Click/Hover for Regime Details")
        self.ax.grid(True)
        self.canvas.draw()
        
    def on_map_click(self, event):
        if event.artist and hasattr(event.artist, 'feature'):
            feature = event.artist.feature
            props = feature.get("properties", {})
            name = props.get("NAME", "Unknown Feature")
            regime = "Development_Control" if "Special" in name else "Mobility_Harmony" if "Bike" in str(feature) else "Sustainable_Harmony"
            messagebox.showinfo("Feature Click", f"{name}\nLinked Regime: {regime}\nGauge Impact: +0.12\nDetails: {json.dumps(props, indent=2)}")
        
    def on_map_hover(self, event):
        # Future: Tooltip (matplotlib annotation)
        pass
        
if __name__ == "__main__":
    app = MarkhamDashboard()
    app.mainloop()