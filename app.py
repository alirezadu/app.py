import streamlit as st
import random
import socket
import time

st.set_page_config(page_title="CxrolWire-Dns", layout="centered")

st.markdown(
    """
    <h1 style='text-align: center; color: red;'>🎮 CxrolWire-Dns</h1>
    <hr style='border: 1px solid red;'>
    """,
    unsafe_allow_html=True
)

# فرم اطلاعات کانفیگ
with st.form("wireguard_form"):
    st.subheader("🔧 تنظیمات کانفیگ WireGuard")
    operator = st.text_input("👨‍💻 اپراتور")
    country = st.selectbox("🌍 کشور", ["Bangladesh", "USA", "UAE", "Turkey", "Russia", "France", "Spain", "Germany", "Japan", "Portugal", "Saudi Arabia", "Switzerland", "Argentina", "Brazil", "Sweden", "Canada", "Iraq"])
    volume = st.text_input("💾 حجم کانفیگ (GB)")
    days = st.text_input("📅 مدت زمان (روز)")
    users = st.selectbox("👥 تعداد کاربران", list(range(1, 7)))
    config_name = st.text_input("📝 نام کانفیگ (نام فایل خروجی بدون .conf)")

    submitted = st.form_submit_button("⚡ ساخت کانفیگ")

# تولید فایل
if submitted:
    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    allowed_ips = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    port = random.randint(1000, 3000)

    config_content = f"""[Interface]
PrivateKey = {key}
Address = {address}

[Peer]
PublicKey = {key}
AllowedIPs = {allowed_ips}
Endpoint = {address}:{port}
"""

    st.success("✅ کانفیگ ساخته شد! می‌تونی فایل رو دانلود کنی.")
    st.download_button(
        label="📥 دانلود فایل کانفیگ",
        data=config_content,
        file_name=f"{config_name}.conf",
        mime="text/plain"
    )

# جداکننده
st.markdown("<hr style='border: 1px solid red;'>", unsafe_allow_html=True)

# بخش بررسی DNS
st.subheader("📡 بررسی DNS Ping")

dns_ip = st.text_input("🌐 آدرس سرور DNS (مثلاً 8.8.8.8)")
if st.button("🔍 تست پینگ DNS"):
    try:
        start = time.time()
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.settimeout(2)
        sock.sendto(b'', (dns_ip, 53))
        sock.recvfrom(512)
        end = time.time()
        elapsed = round((end - start) * 1000, 2)
        st.success(f"✅ پاسخ از {dns_ip} در {elapsed} ms")
    except Exception as e:
        st.error(f"❌ دسترسی به {dns_ip} ممکن نیست")
