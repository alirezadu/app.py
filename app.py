import streamlit as st
import streamlit.components.v1 as components

# ------ WireGuard Generator Section ------
st.title("CxrolWire-Dns - WireGuard Config Generator")
st.markdown("""
<style>
    .main {
        background-color: #1e1e1e;
        color: white;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .stButton>button {
        background-color: #ff003c;
        color: white;
        border-radius: 8px;
        padding: 8px 18px;
        font-weight: bold;
        border: none;
        transition: background-color 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #cc0030;
        color: white;
    }
    .stTextInput>div>input, .stSelectbox>div>div>div>select {
        background-color: #333333;
        color: white;
        border-radius: 5px;
        border: 1px solid #ff003c;
        padding: 8px;
    }
    hr {
        border: 1px solid #ff003c;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("### Generate WireGuard Configuration")

operator = st.text_input("Operator")
country = st.selectbox("Country", ["Bangladesh", "USA", "UAE", "Turkey", "Russia", "France", "Spain", "Germany", "Japan", "Portugal", "Saudi Arabia", "Switzerland", "Argentina", "Brazil", "Sweden", "Canada", "Iraq"])
volume = st.text_input("Config Volume")
days = st.text_input("Number of Days")
users = st.selectbox("Number of Users (1-6)", list(range(1,7)))
config_name = st.text_input("Config Name")

if st.button("Generate Config"):
    import random
    key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=42)) + 'c='
    address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    allowed_ips = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    port = random.randint(1000, 3000)
    config = f"[Interface]\nPrivateKey = {key}\nAddress = {address}\n\n[Peer]\nPublicKey = {key}\nAllowedIPs = {allowed_ips}\nEndpoint = {address}:{port}\n"
    
    # Save to file
    with open(f"{config_name}.conf", "w") as f:
        f.write(config)

    st.success(f"Config '{config_name}.conf' created!")
    st.download_button("Download Config", config, file_name=f"{config_name}.conf", mime="text/plain")

st.markdown("---")

# ------ DNS Section ------
st.markdown("## 🧠 DNS Generator")

dns_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            text-align: center;
            margin: 0;
            padding: 10px;
        }

        h1 {
            color: #ff003c;
            font-size: 32px;
            margin-bottom: 15px;
        }

        table {
            width: 90%;
            margin: 0 auto 20px auto;
            border-collapse: collapse;
            background-color: rgba(30, 30, 30, 0.85);
            border-radius: 10px;
            box-shadow: 0 0 10px #ff003c;
        }

        th, td {
            padding: 12px;
            text-align: center;
            border: 1px solid #ff003c;
        }

        th {
            background-color: #1a1a1a;
            color: #ff003c;
        }

        .btn {
            background-color: #ff003c;
            color: white;
            border: none;
            padding: 10px 20px;
            font-size: 18px;
            cursor: pointer;
            border-radius: 5px;
            margin-bottom: 10px;
            transition: background-color 0.3s ease;
        }

        .btn:hover {
            background-color: #cc0030;
        }

        .ping-low { color: #00ff00; }
        .ping-medium { color: #ffff00; }
        .ping-high { color: #ff3300; }

        .status-low { color: #00ff00; }
        .status-medium { color: #ffff00; }
        .status-high { color: #ff3300; }
    </style>
</head>
<body>
    <h1>🔥 DNS Generator</h1>

    <button class="btn" onclick="generateNewDNS()">NEW DNS</button>

    <table id="dns-table">
        <thead>
            <tr>
                <th>Country</th>
                <th>IPv4</th>
                <th>Ping</th>
                <th>Status</th>
            </tr>
        </thead>
        <tbody></tbody>
    </table>

    <script>
        const countries = [
            { name: 'GERMANY🇩🇪', dns: '89.19.x.x' },
            { name: 'Emirate🇦🇪', dns: '193.123.x.x' },
            { name: 'Türkiye🇹🇷', dns: '85.105.x.x' },
            { name: 'Qatar🇶🇦', dns: '86.36.x.x' },
            { name: 'Finland🇫🇮', dns: '135.181.x.x' },
            { name: 'Arabia🇸🇦', dns: '89.237.x.x' },
            { name: 'Sweden🇸🇪', dns: '46.254.x.x' },
            { name: 'Bahrain🇧🇭', dns: '80.95.x.x' }
        ];

        function getRandomNumber(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }

        function generateRandomPing() {
            return getRandomNumber(20, 400);
        }

        function getStatus(ping) {
            if (ping <= 100) {
                return { status: 'Perfect for gaming ✅', class: 'status-low' };
            } else if (ping <= 200) {
                return { status: 'Playable ✴️', class: 'status-medium' };
            } else {
                return { status: 'Not good ❌', class: 'status-high' };
            }
        }

        function generateRandomDNSData() {
            const selectedCountries = [];
            while (selectedCountries.length < 3) {
                const country = countries[Math.floor(Math.random() * countries.length)];
                if (!selectedCountries.includes(country)) {
                    selectedCountries.push(country);
                }
            }

            const tableBody = document.querySelector("#dns-table tbody");
            tableBody.innerHTML = '';

            let bestPing = Infinity;
            let bestCountry = null;
            let bestDns = '';

            selectedCountries.forEach(country => {
                const ping = generateRandomPing();
                const { status, class: statusClass } = getStatus(ping);
                const randomDns = country.dns.replace(/x/g, () => getRandomNumber(10, 250));
                const pingClass = ping <= 100 ? 'ping-low' : (ping <= 200 ? 'ping-medium' : 'ping-high');

                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${country.name}</td>
                    <td>${randomDns}</td>
                    <td class="${pingClass}">${ping} ms</td>
                    <td class="${statusClass}">${status}</td>
                `;
                tableBody.appendChild(row);

                if (ping < bestPing) {
                    bestPing = ping;
                    bestCountry = country.name;
                    bestDns = randomDns;
                }
            });

            const bestRow = document.createElement('tr');
            bestRow.innerHTML = `
                <td colspan="4">
                    🔥 Best DNS for Gaming: ${bestCountry} (${bestDns}) - ${bestPing} ms
                </td>
            `;
            tableBody.appendChild(bestRow);
        }

        function generateNewDNS() {
            generateRandomDNSData();
        }

        generateNewDNS();
    </script>
</body>
</html>
"""

components.html(dns_html, height=600, scrolling=True)
