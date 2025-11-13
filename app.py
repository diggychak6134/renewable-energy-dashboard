# -----------------------------------------------------------
# 🌍 Renewable Energy Transition Dashboard – Final Combined
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
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)
plt.style.use("dark_background" if dark_mode else "default")

# -------------------- LOAD DATA --------------------
@st.cache_data
def load_data():
    eu = pd.read_csv("eu_data.csv")
    india = pd.read_csv("india_data.csv")
    us = pd.read_csv("us_data.csv")
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

# -------------------- CONSTANTS --------------------
TWH_PER_PERCENT = 15      # approx mapping: 1% share = ~15 TWh (visual/estimate)
CO2_SAVED_PER_TWH = 0.7   # Mt CO2 avoided per TWh (estimate)

# -------------------- HELPERS --------------------
def calc_metrics_for_df(df):
    latest = df["Renewable Share (%)"].iloc[-1]
    first = df["Renewable Share (%)"].iloc[0]
    avg = df["Renewable Share (%)"].mean()
    growth = ((latest - first) / first) * 100
    total_twh = latest * TWH_PER_PERCENT
    co2_saved = total_twh * CO2_SAVED_PER_TWH
    return {"latest": latest, "first": first, "avg": avg, "growth": growth, "twh": total_twh, "co2_saved": co2_saved}

# -------------------- AGGREGATED METRICS FOR "ALL" --------------------
if region == "ALL":
    # Compute per-country metrics
    per = {c: calc_metrics_for_df(df) for c, df in data_dict.items()}
    # Average renewable share (simple mean of latest shares)
    avg_share_all = np.mean([per[c]["latest"] for c in per])
    # Total energy (sum of each country's estimated TWh)
    total_twh_all = np.sum([per[c]["twh"] for c in per])
    # Average growth (simple mean of growth percent)
    avg_growth_all = np.mean([per[c]["growth"] for c in per])
    # Total CO2 saved (sum of each country's co2_saved)
    total_co2_saved_all = np.sum([per[c]["co2_saved"] for c in per])
    # Default global goal (you can tune)
    global_goal = st.sidebar.slider("Set GLOBAL 2030 renewable target (%)", 30, 60, 40)
    global_progress = min(avg_share_all / global_goal, 1.0)

    # Display aggregated metrics
    st.subheader("📊 ALL — Aggregated Renewable Metrics (EU, India, US)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Avg Renewable Share (%)", f"{avg_share_all:.2f}")
    m2.metric("Total Energy (TWh est.)", f"{total_twh_all:.1f}")
    m3.metric("Avg Growth (2014–2023)", f"{avg_growth_all:.1f}%")
    m4.metric("CO₂ Saved (Mt est.)", f"{total_co2_saved_all:.2f}")
    st.markdown("---")
    st.write(f"Global progress toward {global_goal}% target:")
    st.progress(global_progress)
    st.write(f"{global_progress*100:.1f}% progress toward global 2030 target")
    st.markdown("---")

# -------------------- PER-REGION METRICS (EU/INDIA/US) --------------------
if region != "ALL":
    df = data_dict[region]
    metrics = calc_metrics_for_df(df)
    st.subheader(f"📊 {region} Renewable Energy Summary (2014–2023)")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Energy (TWh est.)", f"{metrics['twh']:.1f}")
    m2.metric("Avg. Renewable Share", f"{metrics['avg']:.2f}%")
    m3.metric("Growth (2014–2023)", f"{metrics['growth']:.1f}%")
    m4.metric("CO₂ Saved (Mt est.)", f"{metrics['co2_saved']:.2f}")
    st.markdown("---")

# -------------------- GOAL SLIDER (per-region) --------------------
st.subheader("🎯 Renewable Goal Progress")
goal_defaults = {"EU": 40, "INDIA": 30, "US": 35}
if region != "ALL":
    goal = st.sidebar.slider(f"Set {region}'s 2030 renewable target (%)", 20, 60, goal_defaults.get(region, 40))
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

# -------------------- RENEWABLE MIX (per-region + ALL average) --------------------
st.subheader("⚡ Renewable Energy Mix (2023)")
mix_map = {
    "EU": {"Solar": 35, "Wind": 40, "Hydro": 20, "Biomass": 5},
    "INDIA": {"Solar": 50, "Wind": 30, "Hydro": 18, "Biomass": 2},
    "US": {"Solar": 30, "Wind": 45, "Hydro": 20, "Geothermal": 5}
}

if region in mix_map:
    mix = mix_map[region]
elif region == "ALL":
    # simple average across the three regions
    all_sources = {}
    for m in mix_map.values():
        for k, v in m.items():
            all_sources[k] = all_sources.get(k, 0) + v
    mix = {k: v / len(mix_map) for k, v in all_sources.items()}
else:
    mix = None

if mix:
    fig3, ax3 = plt.subplots()
    ax3.pie(list(mix.values()), labels=list(mix.keys()), autopct='%1.1f%%', startangle=90)
    ax3.set_title(f"{region} Renewable Source Breakdown (2023)")
    st.pyplot(fig3)
st.markdown("---")

# -------------------- CO₂ INTENSITY COMPARISON --------------------
st.subheader("🌫️ CO₂ Intensity of Electricity Generation")
co2_df = pd.DataFrame({
    "Region": ["EU", "India", "US"],
    "CO₂ Intensity (g/kWh)": [230, 680, 370]
}).set_index("Region")
st.bar_chart(co2_df)
st.markdown("---")

# -------------------- CORRELATION PLOT --------------------
st.subheader("🔗 Total CO₂ Emissions vs Renewable Share (National Scale)")

cor_df = pd.DataFrame({
    "Region": ["EU", "India", "US"],
    "Renewable Share (%)": [
        data_dict["EU"]["Renewable Share (%)"].iloc[-1],
        data_dict["INDIA"]["Renewable Share (%)"].iloc[-1],
        data_dict["US"]["Renewable Share (%)"].iloc[-1],
    ],
    "CO₂ Emissions (Mt)": [2400, 2800, 4700]  # realistic values
})

fig4, ax4 = plt.subplots()

# Scatter points
ax4.scatter(cor_df["Renewable Share (%)"], cor_df["CO₂ Emissions (Mt)"], color='orange')

# Labels
for i, txt in enumerate(cor_df["Region"]):
    ax4.annotate(txt, (
        cor_df["Renewable Share (%)"][i] + 0.1,
        cor_df["CO₂ Emissions (Mt)"][i] + 50
    ))

# Regression line
x = cor_df["Renewable Share (%)"]
y = cor_df["CO₂ Emissions (Mt)"]
slope, intercept = np.polyfit(x, y, 1)
x_line = np.linspace(min(x)-1, max(x)+1, 100)
y_line = slope * x_line + intercept
ax4.plot(x_line, y_line, linestyle='--', color='white', linewidth=1)

ax4.set_xlabel("Renewable Share (%)")
ax4.set_ylabel("Total CO₂ Emissions (Mt)")
ax4.set_title("Higher Renewable Share → Lower CO₂ Emissions Trend")
ax4.grid(True, linestyle='--', alpha=0.4)

st.pyplot(fig4)


# -------------------- MAP SECTION (same countries & scores) --------------------
if show_map:
    st.subheader("🗺️ Renewable Energy Strength Map: Potential vs Deployment")
    st.caption("Interactive map showing natural potential, deployment index, and composite score (weighted).")

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
st.subheader("📊 Countries Compared – Summary Table")
#---------------------------COUNTRY COMPARISION SUMMARY---------------------------
summary_table = pd.DataFrame({
    "Region": ["EU", "India", "US"],
    "Latest Renewable Share (%)": [
        data_dict["EU"]["Renewable Share (%)"].iloc[-1],
        data_dict["INDIA"]["Renewable Share (%)"].iloc[-1],
        data_dict["US"]["Renewable Share (%)"].iloc[-1]
    ],
    "CO₂ Intensity (g/kWh)": [230, 680, 370],
    "Total CO₂ Emissions (Mt)": [2400, 2800, 4700],
    "Avg Yearly Growth (%)": [
        ((data_dict[c]["Renewable Share (%)"].iloc[-1] -
          data_dict[c]["Renewable Share (%)"].iloc[0]) /
         data_dict[c]["Renewable Share (%)"].iloc[0]) * 100
        for c in ["EU", "INDIA", "US"]
    ]
})

st.dataframe(summary_table)


# -------------------- DOWNLOAD SUMMARY --------------------
st.subheader("📥 Download / Export")
if region == "ALL":
    # prepare aggregated summary CSV
    summary = pd.DataFrame([
        {"Region": c,
         "Latest Renewable Share (%)": data_dict[c]["Renewable Share (%)"].iloc[-1],
         "Avg Renewable Share (%)": data_dict[c]["Renewable Share (%)"].mean(),
         "Growth (2014-2023 %)": ((data_dict[c]["Renewable Share (%)"].iloc[-1] - data_dict[c]["Renewable Share (%)"].iloc[0]) / data_dict[c]["Renewable Share (%)"].iloc[0]) * 100,
         "Estimated TWh": data_dict[c]["Renewable Share (%)"].iloc[-1] * TWH_PER_PERCENT,
         "Estimated CO2 Saved (Mt)": data_dict[c]["Renewable Share (%)"].iloc[-1] * TWH_PER_PERCENT * CO2_SAVED_PER_TWH
        } for c in data_dict.keys()
    ])
    csv = summary.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Download ALL Summary CSV", csv, file_name="all_summary.csv", mime="text/csv")
else:
    csv = data_dict[region].to_csv(index=False).encode("utf-8")
    st.download_button(f"📥 Download {region} Data CSV", csv, file_name=f"{region}_data.csv", mime="text/csv")
st.markdown("---")

# -------------------- QUICK FACTS & INSIGHTS --------------------
st.subheader("🌍 Quick Facts & Insights")
facts = {
    "EU": "🇪🇺 The EU added strong solar and wind capacity; Germany & Spain lead in deployments.",
    "INDIA": "🇮🇳 India’s solar rollout is fastest; Rajasthan, Gujarat and Tamil Nadu are major contributors.",
    "US": "🇺🇸 The U.S. has huge wind & solar buildouts; Texas, Midwest, and the Southwest lead."
}
if region in facts:
    st.info(facts[region])
elif region == "ALL":
    st.info("Global view: EU leads in policy & grid integration; India leads growth rates; US leads scale and private innovation.")
st.markdown("---")

# -------------------- CREDITS --------------------
st.markdown("""
**Developed by [Diganto Chakraborty](https://github.com/diganto)**  
Data sources: Eurostat, MNRE, EIA • © 2025 Renewable Energy Dashboard
""")

