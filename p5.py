import tkinter as tk
import math

class Pendulum:
    def __init__(self):
        self.angle = 0.1
        self.angular_velocity = 0
        self.length = 100
        self.gravity = 9.8
        self.mass = 1.0
        self.damping = 0.99

    def update(self, cart_acceleration):
        acceleration = (self.gravity / self.length) * self.angle - (1.0 / self.length) * cart_acceleration
        self.angular_velocity += acceleration
        self.angular_velocity *= self.damping
        self.angle += self.angular_velocity
        
        if abs(self.angle) > math.pi / 2:
            self.angle = math.copysign(math.pi / 2, self.angle)
            self.angular_velocity = 0

class Cart:
    def __init__(self):
        self.position = 0
        self.velocity = 0
        self.mass = 2.0
        self.friction = 0.95

    def update(self, force):
        acceleration = force / self.mass
        self.velocity += acceleration
        self.velocity *= self.friction
        self.position += self.velocity

class Controller:
    def __init__(self):
        self.kp = 50.0
        self.kd = 10.0

    def compute_force(self, pendulum, cart):
        force = - (self.kp * pendulum.angle) - (self.kd * pendulum.angular_velocity)
        if force > 50: force = 50
        if force < -50: force = -50
        return force

class Simulation:
    def __init__(self, root):
        self.root = root
        self.root.title("")
        self.root.geometry("700x500")
        
        self.pendulum = Pendulum()
        self.cart = Cart()
        self.controller = Controller()
        
        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack(pady=20)
        
        self.info_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.info_label.pack(pady=10)
        
        self.update_simulation()

    def update_simulation(self):
        force = self.controller.compute_force(self.pendulum, self.cart)
        
        self.cart.update(force)
        self.pendulum.update(force / self.cart.mass)
        
        self.draw_scene()
        
        angle_deg = math.degrees(self.pendulum.angle)
        self.info_label.config(text=f"{angle_deg:.2f}  {force:.1f}")
        
        self.root.after(33, self.update_simulation)

    def draw_scene(self):
        self.canvas.delete("all")
        
        center_x = 350
        ground_y = 350
        cart_width = 60
        cart_height = 30
        
        self.canvas.create_line(50, ground_y, 650, ground_y, fill="black", width=2)
        
        cart_x = center_x + self.cart.position
        
        self.canvas.create_rectangle(cart_x - cart_width/2, ground_y - cart_height, 
                                      cart_x + cart_width/2, ground_y, 
                                      fill="gray", outline="black", width=2)
        
        pivot_x = cart_x
        pivot_y = ground_y - cart_height
        
        tip_x = pivot_x + self.pendulum.length * math.sin(self.pendulum.angle)
        tip_y = pivot_y - self.pendulum.length * math.cos(self.pendulum.angle)
        
        self.canvas.create_line(pivot_x, pivot_y, tip_x, tip_y, fill="red", width=4)
        self.canvas.create_oval(tip_x - 8, tip_y - 8, tip_x + 8, tip_y + 8, fill="blue", outline="black")

if __name__== "__main__":
    root = tk.Tk()
    app = Simulation(root)
    root.mainloop()