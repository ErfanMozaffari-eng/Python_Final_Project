import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class TransferFunction:
    def __init__(self, k, c, omega):
        self.k = k
        self.c = c
        self.omega = omega

class StepResponse:
    def __init__(self, tf):
        self.tf = tf
        self.rise_time = 0
        self.settling_time = 0
        self.overshoot = 0
        
    def calculate_metrics(self):
        tf = self.tf
        if tf.c >= 1:
            self.overshoot = 0
            self.rise_time = 2.2 / tf.omega
            self.settling_time = 4 / tf.omega
        else:
            wd = tf.omega * math.sqrt(1 - tf.c**2)
            self.rise_time = (math.pi - math.acos(tf.c)) / wd
            self.settling_time = 4 / (tf.c * tf.omega)
            self.overshoot = math.exp(-(tf.c * math.pi) / math.sqrt(1 - tf.c**2)) * 100
            
    def get_response_data(self, t):
        tf = self.tf
        if tf.c >= 1:
            s1 = -tf.c * tf.omega + tf.omega * math.sqrt(tf.c**2 - 1)
            s2 = -tf.c * tf.omega - tf.omega * math.sqrt(tf.c**2 - 1)
            return tf.k * (1 + (s2 * np.exp(s1 * t) - s1 * np.exp(s2 * t)) / (s1 - s2))
        else:
            wd = tf.omega * math.sqrt(1 - tf.c**2)
            part1 = 1 - np.exp(-tf.c * tf.omega * t)
            part2 = (tf.c / math.sqrt(1 - tf.c**2)) * np.sin(wd * t) + np.cos(wd * t)
            return tf.k * (part1 * part2)

class Analyzer:
    def __init__(self, response):
        self.response = response
        
    def get_report(self):
        return {
            "Rise Time (Tr)": f"{self.response.rise_time:.3f} s",
            "Settling Time (Ts)": f"{self.response.settling_time:.3f} s",
            "Overshoot (Mp)": f"{self.response.overshoot:.2f} %"
        }

class SystemAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("System Response Analyzer")
        self.root.geometry("850x700")
        
        self.setup_ui()

    def setup_ui(self):
        input_frame = tk.Frame(self.root, pady=10)
        input_frame.pack()
        
        tk.Label(input_frame, text="Gain (K):", font=("Arial", 10)).grid(row=0, column=0, padx=5)
        self.entry_k = tk.Entry(input_frame, width=8)
        self.entry_k.insert(0, "1.0")
        self.entry_k.grid(row=0, column=1, padx=5)
        
        tk.Label(input_frame, text="Damping Ratio (C):", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.entry_c = tk.Entry(input_frame, width=8)
        self.entry_c.insert(0, "0.5")
        self.entry_c.grid(row=0, column=3, padx=5)
        
        tk.Label(input_frame, text="Natural Freq (ωn):", font=("Arial", 10)).grid(row=0, column=4, padx=5)
        self.entry_omega = tk.Entry(input_frame, width=8)
        self.entry_omega.insert(0, "5.0")
        self.entry_omega.grid(row=0, column=5, padx=5)
        
        self.btn_plot = tk.Button(input_frame, text="Plot & Analyze", bg="lightblue", command=self.analyze_and_plot)
        self.btn_plot.grid(row=0, column=6, padx=10)
        
        self.plot_frame = tk.Frame(self.root)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_frame = tk.Frame(self.root, pady=5)
        self.result_frame.pack()
        self.result_label = tk.Label(self.result_frame, text="Enter parameters and click Plot", font=("Arial", 10), fg="gray")
        self.result_label.pack()

    def analyze_and_plot(self):
        try:
            k = float(self.entry_k.get())
            c = float(self.entry_c.get())
            omega = float(self.entry_omega.get())
        except ValueError:
            self.result_label.config(text="Error: Please enter valid numbers.", fg="red")
            return

        if k <= 0 or omega <= 0:
            self.result_label.config(text="Error: K and ωn must be positive.", fg="red")
            return
            tf = TransferFunction(k, c, omega)
        response = StepResponse(tf)
        response.calculate_metrics()
        
        analyzer = Analyzer(response)
        report = analyzer.get_report()
        
        for widget in self.plot_frame.winfo_children():
            widget.destroy()
        for widget in self.result_frame.winfo_children():
            widget.destroy()

        t = np.linspace(0, 5, 500)
        y = response.get_response_data(t)
        
        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.plot(t, y, 'b-', linewidth=2)
        ax.axhline(k, color='r', linestyle='--', alpha=0.5, label='Target (K)')
        ax.set_title("Step Response")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.grid(True, alpha=0.3)
        ax.legend()
        
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        res_text = f"Tr: {report['Rise Time (Tr)']} | Ts: {report['Settling Time (Ts)']} | Mp: {report['Overshoot (Mp)']}"
        self.result_label = tk.Label(self.result_frame, text=res_text, font=("Arial", 11, "bold"), fg="blue")
        self.result_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = SystemAnalyzerGUI(root)
    root.mainloop()