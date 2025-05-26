
import tkinter as tk
from tkinter import ttk, filedialog
import random
import socket
import time

# تابع ساخت کانفیگ و ذخیره
def generate_config():
    operator = operator_var.get()
    country = country_var.get()
    volume = volume_entry.get()
    days = days_entry.get()
    users = users_var.get()
    config_name = config_name_entry.get()

    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    allowed_ips = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    port = random.randint(1000, 3000)

    config = f"""[Interface]
PrivateKey = {key}
Address = {address}

[Peer]
PublicKey = {key}
AllowedIPs = {allowed_ips}
Endpoint = {address}:{port}
"""

    file_path = filedialog.asksaveasfilename(
        initialfile=f"{config_name}.conf",
        defaultextension=".conf",
        filetypes=[("WireGuard Config", "*.conf")]
    )
    if file_path:
        with open(file_path, "w") as f:
            f.write(config)
        status_label.config(text="✅ کانفیگ با موفقیت ذخیره شد!")
    else:
        status_label.config(text="❌ ذخیره‌سازی لغو شد.")

# تابع بررسی DNS
def check_dns_ping():
    dns_ip = dns_entry.get()
    try:
        start_time = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b'', (dns_ip, 53))
        sock.recvfrom(512)
        end_time = time.time()
        elapsed = round((end_time - start_time) * 1000, 2)
        dns_status.config(text=f"✅ پاسخ از {dns_ip} در {elapsed} ms")
    except Exception as e:
        dns_status.config(text=f"❌ دسترسی به {dns_ip} ممکن نیست")

# ---------- رابط گرافیکی ---------- #
app = tk.Tk()
app.title("CxrolWire-Dns")
app.geometry("550x800")
app.configure(bg='black')

# استایل گیمینگ قرمز-مشکی
style = ttk.Style()
style.theme_use("clam")
style.configure('.', background='black', foreground='red', font=('Arial', 10))
style.configure('TButton', background='red', foreground='black')
style.configure('TLabel', background='black', foreground='red')
style.configure('TEntry', fieldbackground='black', foreground='red')
style.configure('TCombobox', fieldbackground='black', foreground='red')

# عنوان اصلی
ttk.Label(app, text="🎮 CxrolWire-Dns", font=('Arial', 22, 'bold')).pack(pady=15)

# فرم ساخت کانفیگ
ttk.Label(app, text="👨‍💻 اپراتور:").pack()
operator_var = tk.StringVar()
ttk.Entry(app, textvariable=operator_var).pack(pady=3)

ttk.Label(app, text="🌍 کشور:").pack()
country_var = tk.StringVar()
countries = ["Bangladesh", "USA", "UAE", "Turkey", "Russia", "France", "Spain", "Germany", "Japan", "Portugal", "Saudi Arabia", "Switzerland", "Argentina", "Brazil", "Sweden", "Canada", "Iraq"]
ttk.Combobox(app, textvariable=country_var, values=countries).pack(pady=3)

ttk.Label(app, text="💾 حجم کانفیگ (GB):").pack()
volume_entry = ttk.Entry(app)
volume_entry.pack(pady=3)

ttk.Label(app, text="📅 مدت زمان (روز):").pack()
days_entry = ttk.Entry(app)
days_entry.pack(pady=3)

ttk.Label(app, text="👥 تعداد کاربران (1-6):").pack()
users_var = tk.StringVar()
ttk.Combobox(app, textvariable=users_var, values=list(range(1, 7))).pack(pady=3)

ttk.Label(app, text="📝 نام کانفیگ:").pack()
config_name_entry = ttk.Entry(app)
config_name_entry.pack(pady=3)

ttk.Button(app, text="⚡ ساخت کانفیگ و دانلود", command=generate_config).pack(pady=10)
status_label = ttk.Label(app, text="")
status_label.pack()

# جداکننده
ttk.Label(app, text="").pack(pady=10)
ttk.Separator(app, orient='horizontal').pack(fill='x', padx=20)
ttk.Label(app, text="🔎 بررسی DNS Ping", font=('Arial', 14, 'bold')).pack(pady=10)

# بخش بررسی DNS
ttk.Label(app, text="🌐 آدرس سرور DNS (مثلاً 8.8.8.8):").pack()
dns_entry = ttk.Entry(app)
dns_entry.pack(pady=5)

ttk.Button(app, text="📡 تست پینگ DNS", command=check_dns_ping).pack(pady=5)
dns_status = ttk.Label(app, text="")
dns_status.pack(pady=5)

# شروع برنامه
app.mainloop()
