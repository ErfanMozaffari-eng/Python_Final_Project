import tkinter as tk

class Card:
    def __init__(self, balance):
        self.balance = balance

    def pay(self):
        if self.balance >= 10:
            self.balance -= 10
            return True
        return False

class Motor:
    def __init__(self):
        self.is_open = False

    def open_gate(self):
        self.is_open = True

    def close_gate(self):
        self.is_open = False

class Gate:
    def __init__(self):
        self.motor = Motor()
        self.is_locked = True

    def let_pass(self, card):
        if card.pay():
            self.is_locked = False
            self.motor.open_gate()
            return True
        else:
            return False

class Passenger:
    def __init__(self, name, card):
        self.name = name
        self.card = card

class MetroGateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("500x450")
        
        self.card = Card(balance=50)
        self.passenger = Passenger("User", self.card)
        self.gate = Gate()
        
        self.is_animating = False
        
        self.canvas = tk.Canvas(self.root, width=400, height=300, bg="#f0f0f0")
        self.canvas.pack(pady=20)
        
        self.info_label = tk.Label(self.root, text="50", font=("Arial", 12), fg="blue")
        self.info_label.pack()
        
        self.pass_btn = tk.Button(self.root, text="Pass", bg="lightgreen", command=self.start_pass_animation)
        self.pass_btn.pack(pady=10)
        
        self.draw_gate()

    def draw_gate(self):
        self.canvas.delete("all")
        
        self.canvas.create_rectangle(100, 50, 300, 250, fill="#d3d3d3", outline="black", width=2)
        self.canvas.create_rectangle(100, 50, 110, 250, fill="gray", outline="black")
        self.canvas.create_rectangle(290, 50, 300, 250, fill="gray", outline="black")
        
        if self.gate.motor.is_open:
            self.canvas.create_rectangle(110, 130, 140, 250, fill="white", outline="white")
            self.canvas.create_rectangle(260, 130, 290, 250, fill="white", outline="white")
        else:
            self.canvas.create_rectangle(110, 130, 200, 250, fill="red", outline="black")
            self.canvas.create_rectangle(200, 130, 290, 250, fill="red", outline="black")
        
        if self.is_animating:
            self.canvas.create_oval(170, 70, 190, 90, fill="blue")
            self.canvas.create_line(180, 90, 180, 160, width=3, fill="blue")
            self.canvas.create_line(180, 120, 160, 160, width=3, fill="blue")
            self.canvas.create_line(180, 120, 200, 160, width=3, fill="blue")

    def start_pass_animation(self):
        if self.is_animating:
            return
            
        self.is_animating = True
        self.pass_btn.config(state=tk.DISABLED)
        
        self.root.after(0, self.animation_step_1)

    def animation_step_1(self):
        if self.card.pay():
            self.gate.gate.motor.open_gate()
            self.draw_gate()
            self.info_label.config(text=str(self.card.balance))
            self.root.after(1000, self.animation_step_2)
        else:
            self.is_animating = False
            self.pass_btn.config(state=tk.NORMAL)
            self.draw_gate()

    def animation_step_2(self):
        self.draw_gate()
        self.root.after(1500, self.animation_step_3)

    def animation_step_3(self):
        self.gate.gate.motor.close_gate()
        self.gate.is_locked = True
        self.draw_gate()
        self.is_animating = False
        self.pass_btn.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = MetroGateGUI(root)
    root.mainloop()