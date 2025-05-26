import streamlit as st
import random
import qrcode
from PIL import Image
from io import BytesIO

st.set_page_config(page_title="Cxrol Wire-Dns", page_icon="🛡️", layout="centered")

st.markdown(
    """
    <style>
    body {
        background-color: #0f0f0f;
    }
    .title {
        font-size: 50px;
        font-family: 'Orbitron', sans-serif;
        color: #ff0033;
        text-align: center;
        text-shadow: 0px 0px 10px red;
    }
    .section-title {
        font-size: 25px;
        font-weight: bold;
        color: #ffffff;
        margin-top: 30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<p class="title">Cxrol Wire-Dns</p>', unsafe_allow_html=True)

st.markdown("### VPN Configuration Generator")

# --- Form Inputs ---
with st.form("config_form"):
    operator = st.text_input("Operator Name")
    country = st.selectbox("Select Country", ["UAE", "Qatar", "Bahrain", "Turkey"])
    volume = st.text_input("Data Volume (e.g. 5GB)")
    days = st.number_input("Valid Days", min_value=1, max_value=365)
    users = st.slider("Number of Users", 1, 6)
    config_name = st.text_input("Config Name")

    submitted = st.form_submit_button("Generate Config")

# --- DNS Mapping ---
dns_map = {
    "UAE": ["185.93.3.123", "91.75.122.21"],
    "Qatar": ["89.211.106.11", "89.211.106.12"],
    "Bahrain": ["185.70.40.65", "185.70.40.66"],
    "Turkey": ["185.15.33.10", "185.15.33.11"]
}

# --- Generate Config ---
if submitted:
    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    port = random.randint(1000, 3000)
    address = f"10.0.{random.randint(0,255)}.{random.randint(1,254)}"
    peer = f"192.168.{random.randint(0,255)}.{random.randint(1,254)}"
    dns = random.choice(dns_map[country])

    config = f"""
[Interface]
PrivateKey = {key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {key}
AllowedIPs = 0.0.0.0/0
Endpoint = vpn.cxrol.com:{port}
PersistentKeepalive = 25
"""

    st.code(config, language="ini")

    # QR Code
    qr = qrcode.make(config)
    buf = BytesIO()
    qr.save(buf)
    buf.seek(0)
    st.image(Image.open(buf), caption="QR Code for WireGuard Config", use_column_width=True)

    # Download Button
    st.download_button("Download Config File", data=config, file_name=f"{config_name}.conf")

# --- DNS Section ---
st.markdown("### DNS Generator (Based on Country)")

selected_dns_country = st.selectbox("Choose Country for DNS", ["UAE", "Qatar", "Bahrain", "Turkey"])
if st.button("Generate DNS"):
    selected_dns = random.choice(dns_map[selected_dns_country])
    st.success(f"DNS for {selected_dns_country}: `{selected_dns}`")
