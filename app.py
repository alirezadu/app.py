import tkinter as tk
from tkinter import ttk
import random
import subprocess
import platform

# DNS لیست اصلی
country_dns_map = {
    "Bangladesh": ["202.4.96.5", "202.4.96.6", "203.76.96.150"],
    "USA": ["8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1", "9.9.9.9"],
    "UAE": ["213.42.20.30", "195.229.241.222", "213.42.20.20", "185.44.64.10"],
    "Turkey": ["193.140.100.100", "195.175.39.49", "193.255.255.2"],
    "Russia": ["77.88.8.8", "77.88.8.1", "94.140.14.14"],
    "France": ["80.67.169.12", "80.67.169.40", "9.9.9.9"],
    "Spain": ["80.58.61.250", "80.58.61.254", "212.230.135.1"],
    "Germany": ["185.12.64.1", "80.241.218.68", "94.140.14.14"],
    "Japan": ["203.0.113.1", "8.8.8.8", "1.1.1.1"],
    "Portugal": ["194.117.207.100", "213.228.128.4", "193.137.29.1"],
    "Saudi Arabia": ["212.26.18.41", "212.26.18.42", "188.95.48.1"],
    "Switzerland": ["77.109.128.2", "77.109.128.4", "185.228.168.9"],
    "Argentina": ["200.49.130.44", "200.49.130.45", "200.51.211.7"],
    "Brazil": ["200.160.0.8", "200.189.40.8", "8.8.8.8"],
    "Sweden": ["194.14.192.20", "194.14.192.21", "193.180.250.210"],
    "Canada": ["64.59.135.133", "64.59.135.135", "205.151.222.251"],
    "Iraq": ["109.224.160.39", "185.94.172.16", "185.94.172.17"],
    "Qatar": ["89.211.0.30", "89.211.5.9", "212.77.203.4"],
    "Bahrain": ["193.188.97.100", "193.188.97.101", "193.188.97.102"]
}

# کش دی‌ان‌اس استفاده‌نشده‌ها
dns_cache = {}

def get_random_unique_dns(country):
    # اگر کش کشور خالی بود، یه کپی جدید از لیست اصلی بساز
    if country not in dns_cache or not dns_cache[country]:
        dns_cache[country] = country_dns_map.get(country, []).copy()
        random.shuffle(dns_cache[country])  # ترتیب رو هم بریز به هم

    # بکش بیرون و حذفش کن
    return dns_cache[country].pop()

def get_ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    try:
        output = subprocess.check_output(command, universal_newlines=True)
        for line in output.split("\n"):
            if "time=" in line or "زمان=" in line:
                return line.strip()
        return "✅ Ping sent, no latency found."
    except Exception as e:
        return f"❌ Ping error: {e}"

def generate_config():
    operator = operator_var.get()
    country = country_var.get()
    volume = volume_entry.get()
    days = days_entry.get()
    users = users_var.get()
    config_name = config_name_entry.get()

    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = f"10.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}"
    selected_dns = get_random_unique_dns(country)
    port = random.randint(1000, 3000)
    ping_result = get_ping(selected_dns)

    config = f"""# 🛡️ CxrolVPN Config
# 🌍 Country: {country}
# 📶 Operator: {operator}
# 📦 Volume: {volume} GB
# ⏳ Days: {days}
# 👥 Users: {users}
# 📡 Ping: {ping_result}

[Interface]
PrivateKey = {key}
Address = {address}
DNS = {selected_dns}

[Peer]
PublicKey = {key}
AllowedIPs = 0.0.0.0/0
Endpoint = {selected_dns}:{port}
"""

    with open(f"{config_name}.conf", "w") as f:
        f.write(config)

    status_label.config(text=f"✅ ساخته شد: {config_name}.conf")

# GUI
app = tk.Tk()
app.title("🛡️ CxrolVPN Config Generator")
app.configure(bg='black')

style = ttk.Style()
style.theme_use("default")
style.configure("TLabel", background='black', foreground='red')
style.configure("TButton", background='black', foreground='red')
style.configure("TEntry", fieldbackground='black', foreground='red')
style.configure("TCombobox", fieldbackground='black', foreground='red')

operator_var = tk.StringVar()
country_var = tk.StringVar()
users_var = tk.StringVar()

ttk.Label(app, text="👤 Operator:").pack()
ttk.Entry(app, textvariable=operator_var).pack()

ttk.Label(app, text="🌍 Country:").pack()
ttk.Combobox(app, textvariable=country_var, values=list(country_dns_map.keys())).pack()

ttk.Label(app, text="📦 Volume (GB):").pack()
volume_entry = ttk.Entry(app)
volume_entry.pack()

ttk.Label(app, text="⏳ Days:").pack()
days_entry = ttk.Entry(app)
days_entry.pack()

ttk.Label(app, text="👥 Users (1-6):").pack()
ttk.Combobox(app, textvariable=users_var, values=list(range(1, 7))).pack()

ttk.Label(app, text="📝 Config File Name:").pack()
config_name_entry = ttk.Entry(app)
config_name_entry.pack()

ttk.Button(app, text="🚀 Generate Config", command=generate_config).pack(pady=10)
status_label = ttk.Label(app, text="", font=("Arial", 10, "bold"))
status_label.pack()

app.mainloop()
