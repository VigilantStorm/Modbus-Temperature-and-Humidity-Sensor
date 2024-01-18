import socket
import tkinter as tk
from tkinter import ttk

socket.socket()

port = 50001

s.connect(("192.168.2.6", port))

sensor_temperature_payload = (s.recv(1024).decode())
sensor_humidity_payload = (s.recv(1024).decode())
api_temperature_payload = (s.recv(1024).decode())
api_humidity_payload = (s.recv(1024).decode())


class HVACApplication:
    def __init__(self, root,temperature):
        self.root = root
        self.root.title("HVAC Application")
        self.root.geometry("600x300")
        self.root.configure(bg="#2c3e50")  # Set background color to a dark blue color
        self.temperature = temperature

        self.heading_label = tk.Label(self.root, text="HVAC Application", font=("Arial", 16, "bold"), fg="orange", bg="#2c3e50")
        self.heading_label.pack(pady=10)

        # Log Out Button (moved to the top-left corner)
        self.logout_button = tk.Button(self.root, text="Log Out", command=self.logout, font=("Arial", 12),
                                       bg="#f39c12", fg="white", width=10, height=2, bd=0, borderwidth=0, highlightthickness=0)
        self.logout_button.pack(side=tk.LEFT, padx=20, pady=10)

        # Current Temperature Label (centered)
        self.temperature_label = tk.Label(self.root, text="{}°F".format(temperature), font=("Arial", 18), bg="#2ecc71", fg="white", width=10, height=3, bd=0)
        self.temperature_label.pack(pady=20)
        self.temperature_label.pack()
        
        self.increase_button = tk.Button(self.root, text="Increase", command=self.increase_temperature, font=("Arial", 10),
                                         bg="#e74c3c", fg="white", width=7, height=2, bd=0, borderwidth=0, highlightthickness=0)
        self.increase_button.pack(side=tk.RIGHT, padx=10)

        # Decrease Button (smaller and on the right)
        self.decrease_button = tk.Button(self.root, text="Decrease", command=self.decrease_temperature, font=("Arial", 10),
                                         bg="#3498db", fg="white", width=7, height=2, bd=0, borderwidth=0, highlightthickness=0)
        self.decrease_button.pack(side=tk.RIGHT, padx=10)

        # Toggle Switch for On, Off, Auto
        self.on_off_auto_var = tk.StringVar(value="Off")
        self.toggle_switch = ttk.Combobox(self.root, textvariable=self.on_off_auto_var, values=["Off", "On", "Auto"], state="readonly")
        self.toggle_switch.bind("<<ComboboxSelected>>", self.toggle_switch_callback)
        self.toggle_switch.pack(side=tk.BOTTOM, padx=20, pady=20)

    def increase_temperature(self):
        #print("test", temperature)
        # Add functionality to increase temperature
        print("Increasing temperature")
        self.temperature += 1
        self.temperature_label.config(text="{}°F".format(self.temperature))

    def decrease_temperature(self):
        # Add functionality to decrease temperature
        print("Decreasing temperature")
        self.temperature -= 1
        self.temperature_label.config(text="{}°F".format(self.temperature))

    def toggle_switch_callback(self, event):
        selected_option = self.on_off_auto_var.get()
        print(f"Toggle switch selected: {selected_option}")

    def logout(self):
        # Add functionality for logging out
        print("Logging out")
        exit

if __name__ == "__main__":
    temperature = sensor_temperature_payload
    root = tk.Tk()
    app = HVACApplication(root,temperature)
    root.mainloop()
    s.close()
