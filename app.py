
import streamlit as st
import random
import subprocess
import platform

# ---------- Data ----------
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

# ---------- UI ----------
st.set_page_config(page_title="CxrolVPN", layout="centered", initial_sidebar_state="auto")
st.markdown("<h1 style='text-align: center; color: #FF0000;'>CxrolVPN Config Generator</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: 1px solid #FF0000;'>", unsafe_allow_html=True)

country = st.selectbox("Select Country", list(country_data.keys()))
volume = st.number_input("Data Volume (GB)", min_value=1, max_value=500, value=10)
days = st.number_input("Validity (Days)", min_value=1, max_value=365, value=30)
profile_name = st.text_input("Profile Name", value="CxrolVPN_Profile")

if st.button("Generate Config"):
    ip = random.choice(country_data[country]["ips"])
    dns = random.choice(country_data[country]["dns"])
    private_key = generate_key()
    public_key = generate_key()
    address = f"{random.randint(10, 250)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 254)}/24"
    port = random.randint(1000, 3000)

    dns_ping = get_ping(dns)
    server_ping = get_ping(ip)

    config_text = f"""[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns}

[Peer]
PublicKey = {public_key}
Endpoint = {ip}:{port}
AllowedIPs = 0.0.0.0/0
PersistentKeepalive = 25"""

    st.code(config_text, language="ini")
    st.download_button("Download Config", config_text, file_name=f"{profile_name}.conf")

    st.success("Configuration generated successfully!")
    st.markdown(f"**Server IP**: `{ip}`  â¢  **Ping**: `{server_ping}`")
    st.markdown(f"**DNS Used**: `{dns}`  â¢  **Ping**: `{dns_ping}`")
