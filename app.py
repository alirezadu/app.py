import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import random
import qrcode
from PIL import Image, ImageTk
import os

# ---------- Config Generator ----------
def generate_config():
    operator = operator_var.get()
    country = country_var.get()
    volume = volume_entry.get()
    days = days_entry.get()
    users = users_var.get()
    config_name = config_name_entry.get()

    if not config_name:
        messagebox.showerror("Error", "Please enter a config name.")
        return

    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    allowed_ips = "0.0.0.0/0"
    port = random.randint(1000, 3000)

    config = f"""[Interface]
PrivateKey = {key}
Address = {address}

[Peer]
PublicKey = {key}
AllowedIPs = {allowed_ips}
Endpoint = {address}:{port}
PersistentKeepalive = 25
"""

    file_path = f"{config_name}.conf"
    with open(file_path, "w") as f:
        f.write(config)

    # Generate QR Code
    qr = qrcode.make(config)
    qr.save("qr_code.png")
    qr_img = Image.open("qr_code.png").resize((150, 150))
    qr_photo = ImageTk.PhotoImage(qr_img)
    qr_label.config(image=qr_photo)
    qr_label.image = qr_photo

    status_label.config(text="✅ WireGuard config generated successfully!")

# ---------- DNS Generator ----------
def generate_dns():
    dns_name = dns_name_entry.get()
    ttl = ttl_entry.get()
    ip = f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"

    if not dns_name or not ttl:
        messagebox.showerror("Error", "Please fill in DNS name and TTL.")
        return

    dns_output = f"{dns_name} A {ip} TTL={ttl}"
    dns_result_label.config(text=f"🔗 DNS Record:\n{dns_output}")

# ---------- GUI Setup ----------
app = tk.Tk()
app.title("Cxrol Wire-Dns")
app.configure(bg="#0b0b0c")
app.geometry("500x820")

# ---------- Style ----------
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", background="#0b0b0c", foreground="#e10600", font=("Courier", 11))
style.configure("TButton", background="#e10600", foreground="white", font=("Courier", 10))
style.configure("TEntry", fieldbackground="#1c1c1c", foreground="white")

# ---------- Title ----------
title = tk.Label(app, text="Cxrol Wire-Dns", font=("Courier New", 24, "bold"), fg="#ff1a1a", bg="#0b0b0c")
title.pack(pady=10)

# ---------- WireGuard Section ----------
operator_var = tk.StringVar()
country_var = tk.StringVar()
users_var = tk.StringVar()

ttk.Label(app, text="Operator:").pack()
ttk.Entry(app, textvariable=operator_var).pack()

ttk.Label(app, text="Country:").pack()
countries = ["UAE", "Turkey", "Qatar", "Bahrain"]
ttk.Combobox(app, textvariable=country_var, values=countries).pack()

ttk.Label(app, text="Data Volume (GB):").pack()
volume_entry = ttk.Entry(app)
volume_entry.pack()

ttk.Label(app, text="Days Valid:").pack()
days_entry = ttk.Entry(app)
days_entry.pack()

ttk.Label(app, text="Users (1-6):").pack()
ttk.Combobox(app, textvariable=users_var, values=list(range(1, 7))).pack()

ttk.Label(app, text="Config Name:").pack()
config_name_entry = ttk.Entry(app)
config_name_entry.pack()

ttk.Button(app, text="Generate WireGuard Config", command=generate_config).pack(pady=10)

# ---------- QR Code ----------
qr_label = tk.Label(app, bg="#0b0b0c")
qr_label.pack(pady=10)

status_label = ttk.Label(app, text="")
status_label.pack()

# ---------- DNS Section ----------
separator = ttk.Separator(app, orient="horizontal")
separator.pack(fill='x', pady=15)

dns_title = tk.Label(app, text="DNS Builder", font=("Courier New", 18, "bold"), fg="#ff1a1a", bg="#0b0b0c")
dns_title.pack()

ttk.Label(app, text="DNS Name (e.g., dns.cxrolvpn.com):").pack()
dns_name_entry = ttk.Entry(app)
dns_name_entry.pack()

ttk.Label(app, text="TTL (Time To Live):").pack()
ttl_entry = ttk.Entry(app)
ttl_entry.pack()

ttk.Button(app, text="Generate DNS", command=generate_dns).pack(pady=10)

dns_result_label = ttk.Label(app, text="")
dns_result_label.pack()

app.mainloop()
