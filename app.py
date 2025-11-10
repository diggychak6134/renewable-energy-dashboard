import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")

# ---------- TITLE & INFO ----------
st.title("🌍 Renewable Energy Data Dashboard: EU vs India (2014–2023)")
st.caption("Data: Eurostat (EU), MNRE & IEA (India). Dashboard by Diganto Chakraborty")

st.markdown("---")

# ---------- DATA LOADING ----------
@st.cache_data
def load_data():
    eu_data = pd.read_csv("eu_data.csv")
    india_data = pd.read_csv("india_data.csv")
    return eu_data, india_data

eu_data, india_data = load_data()

# ---------- SELECTION ----------
col1, col2 = st.columns(2)
with col1:
    option = st.selectbox("Select Country", ["EU", "India", "Both"])

# ---------- BASIC PARAMETERS ----------
# Assume 1% renewable share ≈ 15 TWh (rough estimate, for visualization)
# You can change this factor if you get real generation data.
TWH_PER_PERCENT = 15

# ---------- DATA PROCESSING ----------
if option == "EU":
    df = eu_data.copy()
elif option == "India":
    df = india_data.copy()
else:
    df = None  # placeholder for comparison below

# ---------- METRICS SECTION ----------
if option in ["EU", "India"]:
    latest_share = df["Renewable Share (%)"].iloc[-1]
    avg_share = df["Renewable Share (%)"].mean()
    growth_rate = ((latest_share - df["Renewable Share (%)"].iloc[0]) / df["Renewable Share (%)"].iloc[0]) * 100
    total_energy_twh = latest_share * TWH_PER_PERCENT
    co2_saved = total_energy_twh * 0.0007  # Rough factor: 0.7 Mt CO₂ avoided per TWh

    st.subheader(f"📊 {option} Renewable Energy Key Metrics (2014–2023)")
    mcol1, mcol2, mcol3, mcol4 = st.columns(4)
    mcol1.metric("Total Energy (TWh est.)", f"{total_energy_twh:.1f}")
    mcol2.metric("Avg. Renewable Share (%)", f"{avg_share:.2f}")
    mcol3.metric("Growth Rate (2014–2023)", f"{growth_rate:.1f}%")
    mcol4.metric("CO₂ Saved (Mt est.)", f"{co2_saved:.2f}")

    st.markdown("---")

# ---------- CHART ----------
fig, ax = plt.subplots(figsize=(8, 4))

if option == "EU":
    ax.plot(eu_data["Year"], eu_data["Renewable Share (%)"], marker='o', color='green', label="EU")
    st.subheader("🇪🇺 European Union Renewable Energy Trend")

elif option == "India":
    ax.plot(india_data["Year"], india_data["Renewable Share (%)"], marker='o', color='orange', label="India")
    st.subheader("🇮🇳 India Renewable Energy Trend")

else:
    ax.plot(eu_data["Year"], eu_data["Renewable Share (%)"], marker='o', color='green', label="EU")
    ax.plot(india_data["Year"], india_data["Renewable Share (%)"], marker='s', color='orange', label="India")
    st.subheader("🌏 Comparison: EU vs India")

ax.set_xlabel("Year")
ax.set_ylabel("Renewable Share (%)")
ax.set_title("Renewable Energy Growth (2014–2023)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.6)
st.pyplot(fig)

st.markdown("---")

# ---------- FOOTER ----------
st.write("📈 *This dashboard visualizes renewable energy trends and estimated environmental impact between the EU and India (2014–2023).*")
st.caption("⚙️ Future additions: Map visualization, cost analysis, and renewable goal tracking.")



