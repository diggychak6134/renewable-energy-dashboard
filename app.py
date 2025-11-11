# -----------------------------------------------------------
# 🌍 Renewable Energy Transition Dashboard – Full Version
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

# -------------------- THEME TOGGLE --------------------
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)
plt.style.use("dark_background" if dark_mode else "default")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    eu = pd.read_csv("eu_data.csv")
    india = pd.read_csv("india_data.csv")
    us = pd.read_csv("us_data.csv")
    return {"EU": eu, "INDIA": india, "US": us}

data_dict = load_data()
countries = list(data_dict.keys())

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

# -------------------- GOAL SLIDER --------------------
st.subheader("🎯 Renewable Goal Progress")
goal_map = {"EU": 40, "INDIA": 30, "US": 35}
if region != "ALL":
    goal = st.sidebar.slider(f"Set {region}'s 2030 renewable target (%)", 20, 60, goal_map.get(region, 40))
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

# -------------------- ENERGY MIX PIE CHART --------------------
st.subheader("⚡ Renewable Energy Mix (2023)")

mix_map = {
    "EU": {"Solar": 35, "Wind": 40, "Hydro": 20, "Biomass": 5},
    "INDIA": {"Solar": 50, "Wind": 30, "Hydro": 18, "Biomass": 2},
    "US": {"Solar": 30, "Wind": 45, "Hydro": 20, "Geothermal": 5}
}

if region in mix_map:
    mix = mix_map[region]
elif region == "ALL":
    # Compute average of all countries
    all_sources = {}
    for m in mix_map.values():
        for k, v in m.items():
            all_sources[k] = all_sources.get(k, 0) + v
    mix = {k: v / len(mix_map) for k, v in all_sources.items()}
else:
    mix = None

if mix:
    fig3, ax3 = plt.subplots()
    ax3.pie(mix.values(), labels=mix.keys(), autopct='%1.1f%%', startangle=90)
    ax3.set_title(f"{region} Renewable Source Breakdown (2023)")
    st.pyplot(fig3)


# -------------------- CO₂ INTENSITY COMPARISON --------------------
st.subheader("🌫️ CO₂ Intensity of Electricity Generation")
co2_df = pd.DataFrame({
    "Region": ["EU", "India", "US"],
    "CO₂ Intensity (g/kWh)": [230, 680, 370]
}).set_index("Region")
st.bar_chart(co2_df)
st.markdown("---")

# -------------------- CORRELATION PLOT --------------------
st.subheader("🔗 Correlation: Renewable Share vs Estimated CO₂ Emissions")
cor_df = pd.DataFrame({
    "Region": ["EU", "India", "US"],
    "Renewable Share (%)": [24.5, 22.4, 24.2],
    "CO₂ Emissions (Mt)": [2400, 2600, 4800]
})
fig4, ax4 = plt.subplots()
ax4.scatter(cor_df["Renewable Share (%)"], cor_df["CO₂ Emissions (Mt)"])
for i, txt in enumerate(cor_df["Region"]):
    ax4.annotate(txt, (cor_df["Renewable Share (%)"][i], cor_df["CO₂ Emissions (Mt)"][i]))
ax4.set_xlabel("Renewable Share (%)")
ax4.set_ylabel("CO₂ Emissions (Mt)")
ax4.set_title("Higher Renewable Share → Lower Emissions Trend")
st.pyplot(fig4)
st.markdown("---")

# -------------------- DOWNLOAD SUMMARY --------------------
if region != "ALL":
    csv = data_dict[region].to_csv(index=False).encode("utf-8")
    st.download_button(f"📥 Download {region} Data CSV", csv, file_name=f"{region}_data.csv", mime="text/csv")
st.markdown("---")

# -------------------- COUNTRY FACTS --------------------
st.subheader("🌍 Quick Facts")
facts = {
    "EU": "🇪🇺 The EU added 57 GW of new solar capacity in 2023, led by Germany and Spain.",
    "INDIA": "🇮🇳 India’s solar power share rose 26% YoY, with Rajasthan and Gujarat leading installations.",
    "US": "🇺🇸 The U.S. generated 24% of its electricity from renewables in 2023, mainly wind and solar."
}
if region in facts:
    st.info(facts[region])
elif region == "ALL":
    st.info("Global transition accelerating — Europe leads in policy, India in growth, US in scale.")
st.markdown("---")

# -------------------- CREDITS --------------------
st.markdown("""
---
**Developed by [Diganto Chakraborty](https://github.com/diganto)**  
Data sources: Eurostat, MNRE, EIA  
© 2025 Renewable Energy Dashboard  
""")

