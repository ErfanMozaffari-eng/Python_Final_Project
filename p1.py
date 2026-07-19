import tkinter as tk
from tkinter import messagebox

class Person:
    def __init__(self, name, start_floor, dest_floor):
        self.name = name
        self.start_floor = start_floor
        self.dest_floor = dest_floor

class Elevator:
    def __init__(self, total_floors):
        self.current_floor = 1
        self.total_floors = total_floors
        self.direction = 0
        self.passengers = []
        self.capacity = 10
        self.door_open = False

    def move_one_step(self, target_floor):
        if self.current_floor < target_floor:
            self.current_floor += 1
            self.direction = 1
        elif self.current_floor > target_floor:
            self.current_floor -= 1
            self.direction = -1
        else:
            self.direction = 0
        return self.current_floor

class Controller:
    def __init__(self, building):
        self.building = building
        self.requests = []
        self.is_busy = False

    def add_request(self, floor):
        if floor not in self.requests and 1 <= floor <= self.building.total_floors:
            self.requests.append(floor)
            return True
        return False

    def get_next_target(self):
        if not self.requests:
            return None
        current = self.building.elevator.current_floor
        closest = min(self.requests, key=lambda x: abs(x - current))
        return closest

    def process_next_request(self):
        if not self.requests:
            return None
        target = self.get_next_target()
        self.requests.remove(target)
        return target

class Building:
    def __init__(self, floors):
        self.total_floors = floors
        self.elevator = Elevator(floors)
        self.controller = Controller(self)

class ElevatorGUI:
    def __init__(self, root, a=2):
        self.root = root
        self.root.title("Elevator Simulator")
        self.root.geometry("500x650")
        
        self.a = a
        self.total_floors = 10 * a
        
        self.building = Building(self.total_floors)
        self.is_moving = False
        
        self.setup_ui()

    def setup_ui(self):
        top_frame = tk.Frame(self.root, pady=10)
        top_frame.pack()

        tk.Label(top_frame, text="Enter Floor:", font=("Arial", 12)).pack(side=tk.LEFT, padx=5)
        
        self.floor_entry = tk.Entry(top_frame, width=5, font=("Arial", 12))
        self.floor_entry.pack(side=tk.LEFT, padx=5)
        
        self.call_btn = tk.Button(top_frame, text="Call Elevator", bg="lightblue", command=self.call_elevator)
        self.call_btn.pack(side=tk.LEFT, padx=5)

        status_frame = tk.Frame(self.root, pady=5)
        status_frame.pack()
        
        self.status_label = tk.Label(status_frame, text="Status: Idle", font=("Arial", 12), fg="green")
        self.status_label.pack()

        self.canvas = tk.Canvas(self.root, width=400, height=550, bg="#f0f0f0")
        self.canvas.pack(pady=10, padx=20)

        self.draw_building()

        btn_frame = tk.Frame(self.root, pady=10)
        btn_frame.pack()
        tk.Button(btn_frame, text="Open Door", command=self.open_door_gui).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Close Door", command=self.close_door_gui).pack(side=tk.LEFT, padx=5)

    def draw_building(self):
        self.canvas.delete("all")
        floor_height = 25
        elevator_width = 40
        elevator_height = 20
        
        for i in range(self.total_floors, 0, -1):
            y_pos = 520 - (i * floor_height)
            self.canvas.create_line(50, y_pos, 350, y_pos, fill="gray", width=2)
            self.canvas.create_text(80, y_pos - 5, text=str(i), font=("Arial", 10, "bold"))
            
            current_floor = self.building.elevator.current_floor
            if i == current_floor:
                x1, y1 = 250, y_pos - elevator_height
                x2, y2 = 250 + elevator_width, y_pos
                self.elevator_shape = self.canvas.create_rectangle(x1, y1, x2, y2, fill="orange", outline="black", width=2)
                self.canvas.create_text(x1 + elevator_width/2, y1 + elevator_height/2, text="ELEV", font=("Arial", 8))

        self.canvas.create_line(250, 10, 250, 520, fill="gray", dash=(4, 4))
        self.canvas.create_line(290, 10, 290, 520, fill="gray", dash=(4, 4))

    def update_elevator_position(self):
        self.draw_building()
        self.root.update()

    def call_elevator(self):
        if self.is_moving:
            messagebox.showwarning("Error", "Elevator is moving. Please wait.")
            return

        try:
            target = int(self.floor_entry.get())
            if target < 1 or target > self.total_floors:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", f"Please enter a number between 1 and {self.total_floors}.")
            return

        if self.building.controller.add_request(target):
            self.floor_entry.delete(0, tk.END)
            self.status_label.config(text=f"Request for floor {target} registered.", fg="blue")
            self.start_elevator_animation()
        else:
            messagebox.showinfo("Notice", "This floor has already been requested.")

    def start_elevator_animation(self):
        if self.is_moving:
            return
        
        self.is_moving = True
        self.call_btn.config(state=tk.DISABLED)
        
        while self.building.controller.requests:
            target = self.building.controller.process_next_request()
            if target is None:
                break
                
            self.status_label.config(text=f"Moving to floor {target}...", fg="orange")
            
            current = self.building.elevator.current_floor
            while current != target:
                current = self.building.elevator.move_one_step(target)
                self.update_elevator_position()
                self.root.after(300)
                
            self.status_label.config(text=f"Arrived at floor {target}", fg="green")
            self.root.after(500)
        
        self.is_moving = False
        self.call_btn.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Idle", fg="green")

    def open_door_gui(self):
        if self.is_moving:
            messagebox.showwarning("Error", "Cannot open door while moving.")
            return
        self.building.elevator.door_open = True
        self.status_label.config(text="Door is Open", fg="blue")
        self.canvas.itemconfig(self.elevator_shape, fill="lightgreen")
        self.root.update()

    def close_door_gui(self):
        self.building.elevator.door_open = False
        self.status_label.config(text="Door is Closed", fg="black")
        self.canvas.itemconfig(self.elevator_shape, fill="orange")
        self.root.update()

if __name__ == "__main__":
    root = tk.Tk()
    app = ElevatorGUI(root, a=2)
    root.mainloop()