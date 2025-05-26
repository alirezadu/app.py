
import tkinter as tk
from tkinter import ttk, messagebox
import random
import subprocess
import platform

# Country-specific IP and DNS
country_data = {
    "UAE": {
        "ips": ["5.125.88.1", "94.200.200.200", "185.54.160.1"],
        "dns": ["213.42.20.20", "217.165.0.1"]
    },
    "Qatar": {
        "ips": ["212.77.192.1", "89.211.120.1", "212.77.200.2"],
        "dns": ["212.77.192.1", "89.211.120.1"]
    },
    "Bahrain": {
        "ips": ["193.188.128.1", "193.188.135.10", "185.37.108.1"],
        "dns": ["193.188.128.1", "193.188.135.10"]
    },
    "Turkey": {
        "ips": ["195.175.39.49", "85.95.237.1", "88.255.193.1"],
        "dns": ["195.175.39.39", "212.156.4.20"]
    }
}

def generate_key():
    return ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))

def get_ping(host):
    try:
        param = "-n" if platform.system().lower() == "windows" else "-c"
        result = subprocess.run(["ping", param, "1", host], capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "time=" in line:
                return line.split("time=")[1].split()[0]
    except:
        return "Timeout"
    return "Unavailable"

def generate_config():
    country = country_var.get()
    if country not in country_data:
        messagebox.showerror("Error", "Please select a valid country.")
        return

    ip = random.choice(country_data[country]["ips"])
    dns = random.choice(country_data[country]["dns"])
    private_key = generate_key()
    public_key = generate_key()
    address = f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}/24"
    port = random.randint(1000, 3000)

    dns_ping = get_ping(dns)
    server_ping = get_ping(ip)

    dns_label.config(text=f"DNS: {dns}   Ping: {dns_ping}")
    server_label.config(text=f"Server IP: {ip}   Ping: {server_ping}")

    profile_name = name_entry.get().strip() or "config"
    config_text = f"""[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {public_key}
Endpoint = {ip}:{port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25"""

    with open(f"{profile_name}.conf", "w") as f:
        f.write(config_text)

    messagebox.showinfo("Success", f"Configuration saved as {profile_name}.conf")

# GUI Setup
root = tk.Tk()
root.title("CxrolVPN")
root.configure(bg="#111111")
root.geometry("500x600")

tk.Label(root, text="CxrolVPN", font=("Helvetica", 24, "bold"), bg="#111111", fg="#FF0000").pack(pady=20)

tk.Label(root, text="Select Country", bg="#111111", fg="white").pack()
country_var = tk.StringVar()
country_combo = ttk.Combobox(root, textvariable=country_var, values=list(country_data.keys()))
country_combo.pack(pady=5)

tk.Label(root, text="Data Volume (GB)", bg="#111111", fg="white").pack()
volume_entry = tk.Entry(root)
volume_entry.pack(pady=5)

tk.Label(root, text="Validity (Days)", bg="#111111", fg="white").pack()
days_entry = tk.Entry(root)
days_entry.pack(pady=5)

tk.Label(root, text="Profile Name", bg="#111111", fg="white").pack()
name_entry = tk.Entry(root)
name_entry.pack(pady=5)

dns_label = tk.Label(root, text="DNS: N/A", bg="#111111", fg="#FF4444")
dns_label.pack(pady=5)
server_label = tk.Label(root, text="Server IP: N/A", bg="#111111", fg="#FF4444")
server_label.pack(pady=5)

tk.Button(root, text="Generate Config", command=generate_config, bg="#FF0000", fg="white").pack(pady=10)

root.mainloop()
