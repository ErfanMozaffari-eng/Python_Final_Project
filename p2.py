import tkinter as tk
import random

class Car:
    def __init__(self, car_id, direction):
        self.id = car_id
        self.direction = direction

class TrafficLight:
    def __init__(self):
        self.color = "Red"

    def change(self):
        if self.color == "Red": self.color = "Green"
        elif self.color == "Green": self.color = "Yellow"
        elif self.color == "Yellow": self.color = "Red"

class Lane:
    def __init__(self, direction):
        self.direction = direction
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def pop_car(self):
        return self.cars.pop(0) if self.cars else None

class Intersection:
    def __init__(self):
        self.lanes = {d: Lane(d) for d in ["North", "South", "East", "West"]}
        self.lights = {d: TrafficLight() for d in ["North", "South", "East", "West"]}
        self.car_counter = 0

class Controller:
    def __init__(self, intersection):
        self.intersection = intersection
        self.timer = 0
        self.phase = 0

    def update(self):
        self.timer += 1
        
        if random.random() < 0.25:
            d = random.choice(["North", "South", "East", "West"])
            self.intersection.car_counter += 1
            self.intersection.lanes[d].add_car(Car(self.intersection.car_counter, d))

        if self.timer % 5 == 0:
            if self.phase == 0:
                self.intersection.lights["North"].change()
                self.intersection.lights["South"].change()
                self.phase = 1
            else:
                self.intersection.lights["East"].change()
                self.intersection.lights["West"].change()
                self.phase = 0

        if self.phase == 0:
            if self.intersection.lights["North"].color == "Green" and self.intersection.lanes["North"].cars:
                self.intersection.lanes["North"].pop_car()
            if self.intersection.lights["South"].color == "Green" and self.intersection.lanes["South"].cars:
                self.intersection.lanes["South"].pop_car()
        else:
            if self.intersection.lights["East"].color == "Green" and self.intersection.lanes["East"].cars:
                self.intersection.lanes["East"].pop_car()
            if self.intersection.lights["West"].color == "Green" and self.intersection.lanes["West"].cars:
                self.intersection.lanes["West"].pop_car()

class TrafficGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Simulator")
        self.root.geometry("750x750")
        
        self.intersection = Intersection()
        self.controller = Controller(self.intersection)
        
        self.canvas = tk.Canvas(self.root, width=750, height=750, bg="#e0e0e0")
        self.canvas.pack()
        
        self.draw_roads()
        self.update_simulation()

    def draw_roads(self):
        self.canvas.create_rectangle(250, 0, 500, 750, fill="#333333", outline="")
        self.canvas.create_rectangle(0, 250, 750, 500, fill="#333333", outline="")
        
        self.canvas.create_line(375, 0, 375, 250, fill="white", width=2, dash=(10, 10))
        self.canvas.create_line(375, 500, 375, 750, fill="white", width=2, dash=(10, 10))
        self.canvas.create_line(0, 375, 250, 375, fill="white", width=2, dash=(10, 10))
        self.canvas.create_line(500, 375, 750, 375, fill="white", width=2, dash=(10, 10))
        
        self.canvas.create_rectangle(250, 250, 500, 500, fill="#444444", outline="")

        self.light_shapes = {}
        self.light_shapes["North"] = self.canvas.create_oval(280, 270, 300, 290, fill="red", outline="black")
        self.light_shapes["South"] = self.canvas.create_oval(450, 460, 470, 480, fill="red", outline="black")
        self.light_shapes["East"] = self.canvas.create_oval(460, 270, 480, 290, fill="red", outline="black")
        self.light_shapes["West"] = self.canvas.create_oval(270, 460, 290, 480, fill="red", outline="black")
        self.canvas.create_text(375, 50, text="N", font=("Arial", 12, "bold"), fill="black")
        self.canvas.create_text(375, 700, text="S", font=("Arial", 12, "bold"), fill="black")
        self.canvas.create_text(50, 375, text="W", font=("Arial", 12, "bold"), fill="black")
        self.canvas.create_text(700, 375, text="E", font=("Arial", 12, "bold"), fill="black")

    def update_simulation(self):
        self.controller.update()
        self.canvas.delete("car")
        
        for direction, lane in self.intersection.lanes.items():
            for index, car in enumerate(lane.cars):
                if direction == "North":
                    x, y = 360, 600 - (index * 30)
                elif direction == "South":
                    x, y = 390, 150 + (index * 30)
                elif direction == "East":
                    x, y = 150 + (index * 30), 360
                elif direction == "West":
                    x, y = 600 - (index * 30), 390
                
                self.canvas.create_rectangle(x, y, x+30, y+30, fill="blue", outline="black", tags="car")
                self.canvas.create_text(x+15, y+15, text=str(car.id), fill="white", font=("Arial", 8), tags="car")

        for direction, shape in self.light_shapes.items():
            if self.intersection.lights[direction].color == "Red":
                self.canvas.itemconfig(shape, fill="red")
            elif self.intersection.lights[direction].color == "Green":
                self.canvas.itemconfig(shape, fill="green")
            elif self.intersection.lights[direction].color == "Yellow":
                self.canvas.itemconfig(shape, fill="yellow")
            
        self.root.after(600, self.update_simulation)

if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficGUI(root)
    root.mainloop()