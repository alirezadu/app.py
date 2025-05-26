# app.py
import streamlit as st
import random
import qrcode
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Cxrol Wire-DNS", layout="centered")

# ---------- UI Style ----------
st.markdown(
    """
    <style>
    body {
        background-color: #000000;
    }
    .title {
        font-size:48px;
        font-weight:bold;
        text-align:center;
        color: #ff003c;
        text-shadow: 0px 0px 10px red;
    }
    .section {
        color: white;
        font-size: 20px;
    }
    .stButton>button {
        background-color: #ff003c;
        color: white;
        font-weight: bold;
        border: none;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True
)

# ---------- DNS Data ----------
dns_map = {
    "UAE": ["213.42.20.30", "194.170.1.5"],
    "Qatar": ["212.77.192.1", "212.77.128.1"],
    "Bahrain": ["193.188.97.205", "193.188.97.203"],
    "Turkey": ["195.175.39.39", "195.175.39.40"]
}

# ---------- Title ----------
st.markdown("<div class='title'>Cxrol Wire-DNS</div>", unsafe_allow_html=True)
st.markdown("### WireGuard Config Generator")

# ---------- Form Inputs ----------
country = st.selectbox("Select Country", list(dns_map.keys()))
volume = st.text_input("Enter Volume (e.g. 10GB)")
days = st.text_input("Enter Validity in Days")
config_name = st.text_input("Config Name")

# ---------- Generate Config ----------
if st.button("Generate Config"):
    private_key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42))
    address = f"10.{random.randint(1, 254)}.{random.randint(1, 254)}.1/24"
    endpoint = f"{random.randint(100, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}:{random.randint(1000, 3000)}"
    dns = random.choice(dns_map[country])

    config_text = f"""[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {private_key}
AllowedIPs = 0.0.0.0/0
Endpoint = {endpoint}
"""
    st.code(config_text, language="bash")
    st.success("Config generated successfully!")

    # ---------- QR Code ----------
    img = qrcode.make(config_text)
    buf = BytesIO()
    img.save(buf)
    st.image(buf.getvalue(), caption="Scan QR Code")

# ---------- DNS Section ----------
st.markdown("---")
st.markdown("### DNS Builder")

selected_dns_country = st.selectbox("Select Country for DNS", list(dns_map.keys()), key="dns")
if st.button("Generate DNS"):
    dns_result = random.choice(dns_map[selected_dns_country])
    st.success(f"DNS for {selected_dns_country}: {dns_result}")
