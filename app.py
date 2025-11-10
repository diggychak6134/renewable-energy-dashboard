# -----------------------------------------------------------
# 🌍 Renewable Energy Transition Dashboard – EU vs India
# By Diganto Chakraborty
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")
st.title("🌞 Renewable Energy Transition Dashboard: EU vs India (2014–2023)")
st.caption("Data: Eurostat (EU), MNRE/IEA (India) • Dashboard by Diganto Chakraborty")
st.markdown("---")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    eu = pd.read_csv("eu_data.csv")
    india = pd.read_csv("india_data.csv")
    return eu, india

eu_data, india_data = load_data()

# -------------------- SELECTION --------------------
col1, col2 = st.columns(2)
with col1:
    region = st.selectbox("Select region", ["EU", "India", "Both"])
with col2:
    show_map = st.checkbox("Show Renewable Energy Map", value=True)

st.markdown("---")

# -------------------- METRIC CALCULATION --------------------
TWH_PER_PERCENT = 15      # rough scaling factor
CO2_SAVED_PER_TWH = 0.7   # million tonnes of CO₂ avoided per TWh

if region in ["EU", "India"]:
    df = eu_data if region == "EU" else india_data
    latest = df["Renewable Share (%)"].iloc[-1]
    first = df["Renewable Share (%)"].iloc[0]
    avg = df["Renewable Share (%)"].mean()
    growth = ((latest - first) / first) * 100
    total_twh = latest * TWH_PER_PERCENT
    co2_saved = total_twh * CO2_SAVED_PER_TWH

    st.subheader(f"📊 {region} Renewable Energy Summary (2014–2023)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Energy (TWh est.)", f"{total_twh:.1f}")
    m2.metric("Avg. Renewable Share", f"{avg:.2f}%")
    m3.metric("Growth (2014–2023)", f"{growth:.1f}%")
    m4.metric("CO₂ Saved (Mt est.)", f"{co2_saved:.2f}")

    st.markdown("---")

# -------------------- GOAL TRACKER --------------------
st.subheader("🎯 Renewable Goal Progress")

goal = 40 if region == "EU" else 30     # assumed 2030 goal
current = eu_data["Renewable Share (%)"].iloc[-1] if region == "EU" else india_data["Renewable Share (%)"].iloc[-1]
progress = min(current / goal, 1.0)

st.write(f"**{region}** current renewable share: {current:.1f}% (Goal: {goal}%)")
st.progress(progress)
st.write(f"{progress*100:.1f}% progress toward 2030 target")

st.markdown("---")

# -------------------- CHART --------------------
fig, ax = plt.subplots(figsize=(8, 4))
if region == "EU":
    ax.plot(eu_data["Year"], eu_data["Renewable Share (%)"], marker="o", color="green", label="EU")
    st.subheader("🇪🇺 EU Renewable Energy Trend")
elif region == "India":
    ax.plot(india_data["Year"], india_data["Renewable Share (%)"], marker="o", color="orange", label="India")
    st.subheader("🇮🇳 India Renewable Energy Trend")
else:
    ax.plot(eu_data["Year"], eu_data["Renewable Share (%)"], marker="o", color="green", label="EU")
    ax.plot(india_data["Year"], india_data["Renewable Share (%)"], marker="s", color="orange", label="India")
    st.subheader("🌏 Comparison: EU vs India")

ax.set_xlabel("Year")
ax.set_ylabel("Renewable Share (%)")
ax.set_title("Renewable Energy Growth (2014–2023)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# -------------------- MAP SECTION --------------------
if show_map:
    st.subheader("🗺️ Renewable Energy Clusters and Potential Sites")
    st.caption("Demo dataset – approximate coordinates for renewable clusters")

    data = pd.DataFrame({
        "lat": [48.5, 41.3, 28.5, 22.3, 19.1, 51.0, 37.9],
        "lon": [10.0, 2.1, 77.2, 70.8, 72.8, 0.1, 23.7],
        "Region": ["Germany", "Spain", "India (North)", "India (West)", "India (West Coast)", "UK", "Greece"],
        "Type": ["Solar", "Solar", "Solar", "Wind", "Wind", "Offshore Wind", "Solar"],
        "Potential Score": [8.7, 9.1, 8.5, 8.2, 7.9, 8.9, 9.0]
    })

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=data,
        get_position=["lon", "lat"],
        get_color="[200, 30, 0, 160]",
        get_radius="Potential Score * 20000",
        pickable=True
    )

    view_state = pdk.ViewState(latitude=30, longitude=40, zoom=2)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{Region}\nType: {Type}\nScore: {Potential Score}"}))

    st.markdown("---")

# -------------------- COST & EFFICIENCY SIMULATOR --------------------
st.subheader("💰 Energy Cost & Efficiency Simulation")

col1, col2, col3 = st.columns(3)
with col1:
    capacity = st.number_input("Installed capacity (MW)", 100, 10000, 500)
with col2:
    efficiency = st.slider("System efficiency (%)", 10, 100, 80)
with col3:
    cost_per_mw = st.number_input("Installation cost per MW (Million $)", 0.1, 10.0, 1.5)

energy_output_twh = capacity * (efficiency / 100) * 8760 / 1e6  # TWh per year
total_cost = capacity * cost_per_mw
co2_saved_sim = energy_output_twh * CO2_SAVED_PER_TWH

c1, c2, c3 = st.columns(3)
c1.metric("Annual Energy Output", f"{energy_output_twh:.2f} TWh")
c2.metric("Total Installation Cost", f"${total_cost:.1f} M")
c3.metric("CO₂ Saved (est.)", f"{co2_saved_sim:.2f} Mt")

st.markdown("---")

# -------------------- SUMMARY --------------------
st.subheader("📈 Insights Summary")
if region == "EU":
    st.write("""
    - The EU achieved **~23.5% renewable share** in 2023, showing a steady growth pattern.
    - Strong policy support, carbon pricing, and technological advancement drive this progress.
    - Future growth will depend on grid modernization and offshore wind expansion.
    """)
elif region == "India":
    st.write("""
    - India reached **~22.4% renewable share** in 2023, growing rapidly through solar and wind installations.
    - High solar potential in western and southern regions can push future capacity.
    - Policy consistency and storage technology adoption will be key to hitting 30%+ by 2030.
    """)
else:
    st.write("""
    - The EU maintains a higher current share, but India shows a faster annual growth rate.
    - Both regions are on track for significant renewable expansion by 2030.
    - Collaboration on technology transfer and investment could accelerate the transition globally.
    """)

st.caption("© 2025 Renewable Energy Dashboard by Diganto Chakraborty")




