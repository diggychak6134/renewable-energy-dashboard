# -----------------------------------------------------------
# 🌍 Renewable Energy Transition Dashboard – EU, India & USA
# By Diganto Chakraborty
# -----------------------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import pydeck as pdk

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")
st.title("🌞 Renewable Energy Transition Dashboard: EU vs India vs USA (2014–2023)")
st.caption("Data: Eurostat (EU), MNRE/IEA (India), EIA (US) • Dashboard by Diganto Chakraborty")
st.markdown("---")

# -------------------- LOAD DATA (ensure US included) --------------------
@st.cache_data
def load_data():
    eu = pd.read_csv("eu_data.csv")
    india = pd.read_csv("india_data.csv")
    us = pd.read_csv("us_data.csv")   # <-- must exist in repo root
    return {"EU": eu, "INDIA": india, "US": us}

data_dict = load_data()
countries = list(data_dict.keys())  # ['EU','INDIA','US']

# -------------------- REGION SELECTION --------------------
col1, col2 = st.columns(2)
with col1:
    region = st.selectbox("Select region", countries + ["ALL"])
with col2:
    show_map = st.checkbox("Show Renewable Energy Map", value=True)

st.markdown("---")

# -------------------- METRIC CALCULATION --------------------
TWH_PER_PERCENT = 15
CO2_SAVED_PER_TWH = 0.7

if region != "ALL":
    df = data_dict[region]
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
goal_map = {"EU": 40, "INDIA": 30, "US": 35}
if region != "ALL":
    goal = goal_map.get(region, 40)
    current = data_dict[region]["Renewable Share (%)"].iloc[-1]
    progress = min(current / goal, 1.0)
    st.write(f"**{region}** current renewable share: {current:.1f}% (Goal: {goal}%)")
    st.progress(progress)
    st.write(f"{progress*100:.1f}% progress toward 2030 target")
    st.markdown("---")

# -------------------- RENEWABLE TREND CHART --------------------
st.subheader("📈 Renewable Energy Growth Trend")
fig, ax = plt.subplots(figsize=(8, 4))
if region == "ALL":
    for country, df in data_dict.items():
        ax.plot(df["Year"], df["Renewable Share (%)"], marker='o', label=country)
else:
    df = data_dict[region]
    ax.plot(df["Year"], df["Renewable Share (%)"], marker='o', label=region)
ax.set_xlabel("Year")
ax.set_ylabel("Renewable Share (%)")
ax.set_title("Renewable Energy Share (2014–2023)")
ax.legend()
ax.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig)

# -------------------- FORECASTING (2024–2030) --------------------
st.subheader("🔮 Forecast: Projected Renewable Share (2024–2030)")
def forecast(df):
    x = df["Year"].values
    y = df["Renewable Share (%)"].values
    slope, intercept = np.polyfit(x, y, 1)
    future_years = np.arange(2024, 2031)
    future_pred = slope * future_years + intercept
    return future_years, future_pred

fig2, ax2 = plt.subplots(figsize=(8, 4))
if region == "ALL":
    for country, df in data_dict.items():
        fy, fp = forecast(df)
        ax2.plot(df["Year"], df["Renewable Share (%)"], 'o-', label=f"{country} Actual")
        ax2.plot(fy, fp, '--', label=f"{country} Forecast")
else:
    fy, fp = forecast(data_dict[region])
    ax2.plot(data_dict[region]["Year"], data_dict[region]["Renewable Share (%)"], 'o-', label=f"{region} Actual")
    ax2.plot(fy, fp, '--', label=f"{region} Forecast")
ax2.set_xlabel("Year")
ax2.set_ylabel("Renewable Share (%)")
ax2.legend()
ax2.set_title("Renewable Share Forecast (2024–2030)")
ax2.grid(True, linestyle="--", alpha=0.5)
st.pyplot(fig2)
st.markdown("---")

# -------------------- MAP SECTION (includes USA) --------------------
if show_map:
    st.subheader("🗺️ Renewable Energy Strength Map: Potential vs Deployment")
    st.caption("Interactive comparison of potential, deployment, and composite score.")

    data = pd.DataFrame({
        "lat": [51.1657, 40.4637, 28.6139, 22.7196, 19.0760, 55.3781, 37.9838, 37.0902],
        "lon": [10.4515, -3.7492, 77.2090, 75.8577, 72.8777, -3.4360, 23.7275, -95.7129],
        "Region": [
            "Germany", "Spain", "India (North)", "India (Central)",
            "India (West)", "UK", "Greece", "USA"
        ],
        "Type": ["Wind+Solar", "Solar", "Solar", "Wind", "Solar+Wind", "Offshore Wind", "Solar", "Wind+Solar"],
        "Potential Score": [8.8, 9.5, 8.6, 8.3, 8.1, 9.2, 9.0, 9.5],
        "Deployment Index": [9.8, 7.5, 7.8, 7.2, 7.5, 9.0, 6.8, 9.2]
    })

    weight = st.slider("⚙️ Adjust Deployment Weight (Composite Calculation)", 0.0, 1.0, 0.6)
    data["Composite Score"] = (data["Deployment Index"] * weight) + (data["Potential Score"] * (1 - weight))

    view_option = st.radio("Select score to visualize:", ["Natural Potential", "Deployment Strength", "Composite Score"], horizontal=True)
    if view_option == "Natural Potential":
        score_column = "Potential Score"; color = [255,165,0]
    elif view_option == "Deployment Strength":
        score_column = "Deployment Index"; color = [0,200,255]
    else:
        score_column = "Composite Score"; color = [0,255,127]

    data["Radius"] = data[score_column] * 40000
    layer = pdk.Layer("ScatterplotLayer", data=data, get_position=["lon","lat"], get_color=color, get_radius="Radius", pickable=True, auto_highlight=True)
    view_state = pdk.ViewState(latitude=30, longitude=10, zoom=2.5, pitch=0)
    tooltip = {"text": "{Region}\nType: {Type}\n" + score_column + ": {" + score_column + "}"}
    st.pydeck_chart(pdk.Deck(map_style=None, layers=[layer], initial_view_state=view_state, tooltip=tooltip))
    st.markdown(f"**Legend:** Colored circles indicate {view_option.lower()} (size = higher score).")
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

energy_output_twh = capacity * (efficiency / 100) * 8760 / 1e6
total_cost = capacity * cost_per_mw
co2_saved_sim = energy_output_twh * CO2_SAVED_PER_TWH

c1, c2, c3 = st.columns(3)
c1.metric("Annual Energy Output", f"{energy_output_twh:.2f} TWh")
c2.metric("Total Installation Cost", f"${total_cost:.1f} M")
c3.metric("CO₂ Saved (est.)", f"{co2_saved_sim:.2f} Mt")
st.markdown("---")

# -------------------- INSIGHTS --------------------
st.subheader("📈 Insights Summary")
if region == "EU":
    st.write("""
    - The EU achieved **~23.5% renewable share** in 2023, showing steady growth under strong policy frameworks.
    - Forecast suggests reaching **~41% by 2030**, consistent with EU Green Deal goals.
    """)
elif region == "INDIA":
    st.write("""
    - India reached **~22.4% renewable share** in 2023, led by solar and wind projects.
    - Forecasts show crossing **~30% by 2030** with continued infrastructure investment.
    """)
elif region == "US":
    st.write("""
    - The United States reached **~24% renewable share** in 2023, driven by wind and solar expansion.
    - Forecasts show potential to exceed **35% by 2030**, especially with federal incentives and private innovation.
    """)
else:
    st.write("""
    - EU leads in policy and deployment, India excels in growth speed, and the US balances innovation and scale.
    - Global transition is accelerating with strong contributions from all three regions.
    """)
st.caption("© 2025 Renewable Energy Dashboard by Diganto Chakraborty")




