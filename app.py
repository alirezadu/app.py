
import streamlit as st
import random

# ----- Country-specific IPs and DNS -----
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

# ----- UI Layout -----
st.set_page_config(page_title="CxrolVPN", layout="centered", initial_sidebar_state="collapsed")

# ----- Custom Styling -----
st.markdown("""
    <style>
    html, body, [class*="css"] {
        background-color: #0b0b0c !important;
        color: #e10600 !important;
        font-family: 'Courier New', monospace;
    }
    .stTextInput>div>div>input,
    .stNumberInput>div>input,
    .stSelectbox>div>div>div {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #e10600 !important;
    }
    .stButton>button {
        background-color: #e10600;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.6em 2em;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #ff1a1a;
        transform: scale(1.05);
    }
    h1 {
        text-align: center;
        font-size: 3em;
        color: #ff0000;
        text-shadow: 0 0 10px red;
    }
    hr {
        border: none;
        height: 2px;
        background-color: #ff0000;
        margin: 20px 0;
    }
    </style>
""", unsafe_allow_html=True)

# ----- Title -----
st.markdown("<h1>CxrolVPN Generator</h1><hr>", unsafe_allow_html=True)

# ----- User Inputs -----
country = st.selectbox("Select Country", list(country_data.keys()))
volume = st.number_input("Data Volume (GB)", min_value=1, max_value=500, value=10)
days = st.number_input("Validity (Days)", min_value=1, max_value=365, value=30)
profile_name = st.text_input("Config Name", value="CxrolVPN_Profile")

# ----- Generate Config -----
if st.button("Generate WireGuard Config"):
    ip = random.choice(country_data[country]["ips"])
    dns = random.choice(country_data[country]["dns"])
    private_key = generate_key()
    public_key = generate_key()
    address = f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}/24"
    port = random.randint(1000, 3000)

    config_text = f"""[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {public_key}
Endpoint = {ip}:{port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25"""

    st.success("✅ Config generated successfully!")
    st.code(config_text, language="ini")
    st.download_button("Download Config", config_text, file_name=f"{profile_name}.conf")
