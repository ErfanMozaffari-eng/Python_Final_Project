import tkinter as tk
import random
import math

class Tank:
    def __init__(self, max_height):
        self.current_level = 0
        self.max_height = max_height
        self.inflow = 0
        self.outflow = 0

    def update(self):
        self.current_level += (self.inflow - self.outflow)
        if self.current_level < 0: self.current_level = 0
        if self.current_level > self.max_height: self.current_level = self.max_height

class Pump:
    def __init__(self):
        self.is_on = False

    def turn_on(self):
        self.is_on = True

    def turn_off(self):
        self.is_on = False

class Controller:
    def __init__(self, tank, pump):
        self.tank = tank
        self.pump = pump
        self.min_level = 10
        self.max_level = 40

    def control_on_off(self):
        if self.tank.current_level < self.min_level:
            self.pump.turn_on()
        elif self.tank.current_level > self.max_level:
            self.pump.turn_off()

class Simulation:
    def __init__(self, root, a=2):
        self.root = root
        self.root.title("Water Tank Simulator")
        self.root.geometry("700x600")
        
        self.max_height = 50 * a
        self.tank = Tank(self.max_height)
        self.pump = Pump()
        self.controller = Controller(self.tank, self.pump)
        
        self.history = []
        self.time_step = 0
        
        self.setup_ui()
        self.update_simulation()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, width=400, height=400, bg="#f0f0f0")
        self.canvas.pack(pady=10)
        
        self.info_label = tk.Label(self.root, text="Status: Init...", font=("Arial", 12))
        self.info_label.pack(pady=5)
        
        self.graph_canvas = tk.Canvas(self.root, width=600, height=150, bg="white")
        self.graph_canvas.pack(pady=10)

    def draw_tank(self):
        self.canvas.delete("all")
        
        tank_x1, tank_y1 = 100, 50
        tank_x2, tank_y2 = 300, 350
        
        self.canvas.create_rectangle(tank_x1, tank_y1, tank_x2, tank_y2, outline="black", width=3)
        
        level_height = (self.tank.current_level / self.max_height) * (tank_y2 - tank_y1)
        water_y = tank_y2 - level_height
        
        self.canvas.create_rectangle(tank_x1 + 5, water_y, tank_x2 - 5, tank_y2 - 5, fill="blue", outline="")
        
        self.canvas.create_text(200, 380, text=f"Level: {self.tank.current_level:.1f} / {self.max_height}", font=("Arial", 12))
        
        status = "Pump: ON" if self.pump.is_on else "Pump: OFF"
        color = "red" if self.pump.is_on else "green"
        self.canvas.create_text(200, 410, text=status, font=("Arial", 12, "bold"), fill=color)

    def draw_graph(self):
        self.graph_canvas.delete("all")
        
        width = 600
        height = 150
        margin = 30
        
        self.graph_canvas.create_line(margin, height - margin, width - margin, height - margin, fill="black")
        self.graph_canvas.create_line(margin, margin, margin, height - margin, fill="black")
        
        if len(self.history) < 2:
            return
            
        max_val = self.max_height
        step_x = (width - 2 * margin) / max(1, len(self.history) - 1)
        scale_y = (height - 2 * margin) / max_val
        
        points = []
        for i, val in enumerate(self.history):
            x = margin + i * step_x
            y = (height - margin) - (val * scale_y)
            points.append((x, y))
            
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i+1]
            self.graph_canvas.create_line(x1, y1, x2, y2, fill="blue", width=2)

    def update_simulation(self):
        self.time_step += 1
        
        self.tank.inflow = 2.0 if self.pump.is_on else 0.0