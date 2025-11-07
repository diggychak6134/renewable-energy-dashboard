import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# App title
st.title("☀️ Solar Power Efficiency Simulator")

st.write("""
This simple web app simulates how much energy a small solar panel setup can generate based on sunlight, panel efficiency, and time of day.
""")

# Sidebar inputs
st.sidebar.header("🔧 Input Parameters")
sunlight_hours = st.sidebar.slider("Average Sunlight Hours per Day", 1.0, 12.0, 6.0)
panel_power = st.sidebar.number_input("Solar Panel Power (Watts)", 1, 500, 100)
efficiency = st.sidebar.slider("Panel Efficiency (%)", 5, 25, 15)
days = st.sidebar.slider("Number of Days", 1, 30, 7)

# Simulation logic
daily_output = panel_power * (efficiency / 100) * sunlight_hours
total_energy = daily_output * days

# Output
st.subheader("🔋 Energy Output Results")
st.write(f"**Daily Output:** {daily_output:.2f} Wh/day")
st.write(f"**Total Energy for {days} days:** {total_energy:.2f} Wh")

# Chart
days_arr = np.arange(1, days + 1)
energy_arr = daily_output * days_arr

fig, ax = plt.subplots()
ax.plot(days_arr, energy_arr, linewidth=2)
ax.set_xlabel("Days")
ax.set_ylabel("Total Energy (Wh)")
ax.set_title("Energy Generation Over Time")
st.pyplot(fig)

# Footer
st.markdown("---")
st.caption("Developed by Diganto Chakraborty – Renewable Energy Simulation Project")
