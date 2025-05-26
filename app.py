import streamlit as st
import random
import base64
import os
from datetime import datetime
import streamlit.components.v1 as components

st.set_page_config(page_title="CxrolWire-DNS", page_icon="🧠", layout="centered")
st.markdown("<h1 style='text-align: center; color: red;'>CxrolWire-DNS</h1>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🛠️ Generate WireGuard Config")

# --- COUNTRY + DNS CONFIG ---
country_dns = {
    "Bahrain 🇧🇭": ["80.95.123.45", "80.95.130.66", "80.95.110.27"],
    "UAE 🇦🇪": ["193.123.98.100", "193.123.50.20", "193.123.45.80"],
    "Saudi Arabia 🇸🇦": ["89.237.12.34", "89.237.45.67", "89.237.78.90"],
    "Turkey 🇹🇷": ["85.105.100.50", "85.105.200.60", "85.105.150.70"]
}

# --- FORM UI ---
with st.form("config_form"):
    operator = st.text_input("Operator Name")
    country = st.selectbox("Country", list(country_dns.keys()))
    volume = st.text_input("Config Volume (e.g., 5GB)")
    days = st.text_input("Days (e.g., 30)")
    users = st.selectbox("Number of Users", [1, 2, 3, 4, 5, 6])
    config_name = st.text_input("Config File Name (no extension)")

    submitted = st.form_submit_button("Generate Config")

if submitted:
    private_key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    public_key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    allowed_ips = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    port = random.randint(1000, 3000)
    dns_server = random.choice(country_dns[country])

    config = f"""[Interface]
PrivateKey = {private_key}
Address = {address}
DNS = {dns_server}

[Peer]
PublicKey = {public_key}
AllowedIPs = {allowed_ips}
Endpoint = {address}:{port}
"""

    filename = f"{config_name}.conf"
    with open(filename, "w") as f:
        f.write(config)

    with open(filename, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    href = f'<a href="data:file/conf;base64,{b64}" download="{filename}">📥 Download {filename}</a>'
    st.markdown(href, unsafe_allow_html=True)
    st.success("✅ Configuration created successfully!")

# --- DNS SECTION ---
st.markdown("---")
st.markdown("### 🌐 DNS Game Performance (Randomized)")

components.html(
    """
    <style>
    body {
        background-color: #1e1e1e;
        color: white;
        font-family: 'Segoe UI', sans-serif;
    }
    .btn {
        background-color: #ff003c;
        color: white;
        padding: 10px 20px;
        border: none;
        font-size: 16px;
        cursor: pointer;
        margin: 10px auto;
        display: block;
        border-radius: 5px;
    }
    .btn:hover {
        background-color: #cc002e;
    }
    table {
        width: 90%;
        margin: 20px auto;
        border-collapse: collapse;
        background-color: #2c2c2c;
    }
    th, td {
        padding: 10px;
        text-align: center;
        border: 1px solid #444;
    }
    th {
        background-color: #111;
    }
    .ping-low { color: green; }
    .ping-medium { color: yellow; }
    .ping-high { color: red; }
    </style>

    <button class="btn" onclick="generateDNS()">Generate New DNS</button>
    <table id="dns-table">
        <thead>
            <tr><th>Country</th><th>IPv4</th><th>Ping</th><th>Status</th></tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
    const countries = [
        { name: "Bahrain 🇧🇭", dns: "80.95.x.x" },
        { name: "UAE 🇦🇪", dns: "193.123.x.x" },
        { name: "Saudi Arabia 🇸🇦", dns: "89.237.x.x" },
        { name: "Turkey 🇹🇷", dns: "85.105.x.x" }
    ];

    function getRandom(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    }

    function generatePing() {
        return getRandom(20, 300);
    }

    function getStatus(ping) {
        if (ping <= 100) return ["Great for Gaming ✅", "ping-low"];
        if (ping <= 200) return ["Average ✴️", "ping-medium"];
        return ["Bad ❌", "ping-high"];
    }

    function generateDNS() {
        const tbody = document.querySelector("#dns-table tbody");
        tbody.innerHTML = "";
        countries.forEach(c => {
            const ping = generatePing();
            const [status, cls] = getStatus(ping);
            const ip = c.dns.replace(/x/g, () => getRandom(10, 250));
            tbody.innerHTML += `
                <tr>
                    <td>${c.name}</td>
                    <td>${ip}</td>
                    <td class="${cls}">${ping} ms</td>
                    <td class="${cls}">${status}</td>
                </tr>
            `;
        });
    }

    generateDNS();
    </script>
    """,
    height=500
)
