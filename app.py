import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")
st.title("Renewable Energy Dashboard")

st.write("""
A mini project dashboard showing **simulated renewable energy data**.
It models real-world variation in production due to factors like weather, season, and maintenance.
""")

# Select energy source
energy_sources = ["Solar", "Wind", "Hydro", "Biomass"]
selected_source = st.selectbox("Select Energy Source", energy_sources, key="source_select")

# Generate semi-realistic data
np.random.seed(42)
years = np.arange(2015, 2025)
base = {
    "Solar": 60,
    "Wind": 50,
    "Hydro": 40,
    "Biomass": 25
}[selected_source]

# Add fluctuations
trend = base + np.cumsum(np.random.normal(0.8, 2.5, len(years)))
trend = np.maximum(trend, 0)  # ensure no negative values

df = pd.DataFrame({"Year": years, "Production (MW)": trend})

# Plot
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(df["Year"], df["Production (MW)"], marker='o', linestyle='-', color='tab:green')
ax.set_title(f"{selected_source} Energy Production (2015–2024)", fontsize=13)
ax.set_xlabel("Year")
ax.set_ylabel("Production (MW)")
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)

# Add some insights
growth = ((df["Production (MW)"].iloc[-1] - df["Production (MW)"].iloc[0]) / df["Production (MW)"].iloc[0]) * 100
st.metric(label=f"{selected_source} Growth (2015–2024)", value=f"{growth:.2f}%")
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

st.set_page_config(page_title="Renewable Energy Dashboard", layout="wide")
st.title("Renewable Energy Dashboard")

st.write("""
A mini project dashboard showing **simulated renewable energy data**.
It models real-world variation in production due to factors like weather, season, and maintenance.
""")

# Select energy source
energy_sources = ["Solar", "Wind", "Hydro", "Biomass"]
selected_source = st.selectbox("Select Energy Source", energy_sources)

# Generate semi-realistic data
np.random.seed(42)
years = np.arange(2015, 2025)
base = {
    "Solar": 60,
    "Wind": 50,
    "Hydro": 40,
    "Biomass": 25
}[selected_source]

# Add fluctuations
trend = base + np.cumsum(np.random.normal(0.8, 2.5, len(years)))
trend = np.maximum(trend, 0)  # ensure no negative values

df = pd.DataFrame({"Year": years, "Production (MW)": trend})

# Plot
fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(df["Year"], df["Production (MW)"], marker='o', linestyle='-', color='tab:green')
ax.set_title(f"{selected_source} Energy Production (2015–2024)", fontsize=13)
ax.set_xlabel("Year")
ax.set_ylabel("Production (MW)")
ax.grid(True, linestyle="--", alpha=0.6)

st.pyplot(fig)

# Add some insights
growth = ((df["Production (MW)"].iloc[-1] - df["Production (MW)"].iloc[0]) / df["Production (MW)"].iloc[0]) * 100
st.metric(label=f"{selected_source} Growth (2015–2024)", value=f"{growth:.2f}%")
