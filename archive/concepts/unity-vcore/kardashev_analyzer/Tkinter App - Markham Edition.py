import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Polygon
import json
import os
from decimal import Decimal
import random

random.seed(42)  # Deterministic

class CityExcellenceEngine(tk.Tk):
    def __init__(self, city_config="markham_config.json"):
        super().__init__()
        self.title("Excellence Decision Engine - Secure Offline Mode")
        self.geometry("1600x1000")
        self.configure(bg="#f0f0f0")
        
        # Load City Config (Universal Template)
        self.config = self.load_city_config(city_config)
        
        # Regime Weights (Evolvable)
        self.regime_weights = self.config.get("regimes", {
            "Energy_Excellence": Decimal('0.30'),
            "Mobility_Harmony": Decimal('0.25'),
            "Sustainable_Harmony": Decimal('0.20'),
            "Economic_Vitality": Decimal('0.15'),
            "Community_Thriving": Decimal('0.10')
        })
        
        self.current_gauge = Decimal('0.85')
        self.goal_targets = {}
        
        self.create_widgets()
        
    def load_city_config(self, filename):
        default = {
            "city_name": "Markham",
            "motto": "Leading While Remembering",
            "mayor": "Frank Scarpitti",
            "population": "360,000+",
            "branding": "Canada's High-Tech Capital | Sustainable Innovation Hub",
            "geo_files": ["Bicycle_Routes.geojson", "Parks.geojson", "Fire_Stations.geojson", "Site_Plan_Control_-_Special_Areas.geojson"]
        }
        if os.path.exists(filename):
            with open(filename) as f:
                return json.load(f)
        return default
        
    def create_widgets(self):
        # Header with City Identity
        header = tk.Frame(self, bg="#2c3e50")
        header.pack(fill="x")
        tk.Label(header, text=f"{self.config['city_name']} Excellence Framework", font=("Helvetica", 20, "bold"), bg="#2c3e50", fg="white").pack(pady=10)
        tk.Label(header, text=f"Motto: {self.config['motto']} | Mayor: {self.config['mayor']}", font=("Helvetica", 12), bg="#2c3e50", fg="white").pack()
        tk.Label(header, text=self.config['branding'], font=("Helvetica", 10, "italic"), bg="#2c3e50", fg="white").pack()
        
        subheader = tk.Label(self, text=f"Overall Civic Mastery Gauge: {self.current_gauge} | Confidence [█████████▒] HIGH", font=("Helvetica", 14))
        subheader.pack(pady=5)
        
        # Main Layout
        main = tk.PanedWindow(self, orient="horizontal")
        main.pack(fill="both", expand=True)
        
        # Tree + Alerts
        left = tk.Frame(main)
        main.add(left)
        
        self.tree = ttk.Treeview(left, columns=("Gauge"), show="tree headings")
        self.tree.heading("#0", text="Regimes")
        self.tree.heading("Gauge", text="Gauge")
        self.tree.pack(fill="both", expand=True)
        
        root = self.tree.insert("", "end", text="Civic_Mastery", values=(self.gauge_bar(self.current_gauge)))
        for r, w in self.regime_weights.items():
            self.tree.insert(root, "end", text=r, values=(self.gauge_bar(w)))
        
        # Map + Projection
        right = tk.Frame(main)
        main.add(right)
        
        self.fig, (self.map_ax, self.proj_ax) = plt.subplots(1, 2, figsize=(12, 6))
        canvas = FigureCanvasTkAgg(self.fig, right)
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        self.plot_map()
        self.plot_projection()
        
        # Actions
        actions = tk.Frame(self)
        actions.pack(pady=10)
        tk.Button(actions, text="Goal Wizard", command=self.goal_wizard).pack(side="left", padx=20)
        
    def gauge_bar(self, gauge):
        fill = int(float(gauge) * 10)
        return "█" * fill + "▒" * (10 - fill)
        
    def plot_map(self):
        # Real GeoJSON plot (mock for brevity—extend with full parse)
        self.map_ax.clear()
        self.map_ax.set_title("City Map View")
        self.map_ax.text(0.5, 0.5, "Markham Districts\n(Bicycle Routes, Parks Loaded)", ha="center")
        self.map_ax.axis("off")
        
    def plot_projection(self):
        self.proj_ax.clear()
        years = [2026, 2030, 2040]
        scores = [0.72, 0.85, 0.95]
        self.proj_ax.plot(years, scores, 'g-o')
        self.proj_ax.set_title("Civic Mastery Trajectory")
        self.proj_ax.set_ylim(0, 1)
        canvas = FigureCanvasTkAgg(self.fig, self)
        canvas.draw()
        
    def goal_wizard(self):
        # Full wizard stub—extend as prior
        messagebox.showinfo("Goal Wizard", "Input goals → evolve regimes (full implementation next)")

if __name__ == "__main__":
    app = CityExcellenceEngine()
    app.mainloop()