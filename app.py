import streamlit as st
import random

st.set_page_config(page_title="CxrolVPN Generator", layout="centered", page_icon=":lock:")
st.markdown("""
    <style>
        body {
            background-color: #0d0d0d;
            color: white;
        }
        .stApp {
            background-color: #0d0d0d;
        }
        .title {
            font-size: 40px;
            color: red;
            font-weight: bold;
            text-align: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🔥 CxrolVPN 🔥</div>', unsafe_allow_html=True)
st.write("### Generate a secure VPN config file")

operator = st.text_input("🔧 Operator")
country = st.selectbox("🌐 Country", [
    "Bangladesh", "USA", "UAE", "Turkey", "Russia", "France", "Spain", "Germany",
    "Japan", "Portugal", "Saudi Arabia", "Switzerland", "Argentina", "Brazil", "Sweden",
    "Canada", "Iraq", "Bahrain", "Qatar", "Emirates"
])
volume = st.text_input("📦 Volume (e.g., 10GB)")
days = st.text_input("📅 Valid Days")
users = st.selectbox("👥 Number of Users", list(range(1, 7)))
config_name = st.text_input("📁 Config Name")

if st.button("🚀 Generate Config"):
    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = ".".join(str(random.randint(1, 255)) for _ in range(4))
    allowed_ips = ".".join(str(random.randint(1, 255)) for _ in range(4))
    port = random.randint(1000, 3000)

    config = f"""[Interface]
PrivateKey = {key}
Address = {address}

[Peer]
PublicKey = {key}
AllowedIPs = {allowed_ips}
Endpoint = {address}:{port}
"""

    st.success("✅ Configuration created!")
    st.download_button("📥 Download Config", config, file_name=f"{config_name}.conf")
