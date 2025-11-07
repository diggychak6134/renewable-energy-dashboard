import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Renewable Energy Comparison", layout="wide")

st.title("🌍 Renewable Energy Share: EU vs India (2014–2023)")
st.write("Data sources: Eurostat (EU) and MNRE/IEA (India)")

# Load the data
eu_data = pd.read_csv("eu_data.csv")
india_data = pd.read_csv("india_data.csv")

# Dropdown for selecting countries
option = st.selectbox("Select country or comparison", ["EU", "India", "Both"])

fig, ax = plt.subplots(figsize=(10, 6))

if option == "EU":
    ax.plot(eu_data["Year"], eu_data["Renewable Share (%)"], marker='o', label="EU", color="green")
    st.subheader("🇪🇺 European Union Renewable Energy Trend")

elif option == "India":
    ax.plot(india_data["Year"], india_data["Renewable Share (%)"], marker='o', label="India", color="orange")
    st.subheader("🇮🇳 India Renewable Energy Trend")

else:
    ax.plot(eu_data["Year"], eu_data["Renewable Share (%)"], marker='o', label="EU", color="green")
    ax.plot(india_data["Year"], india_data["Renewable Share (%)"], marker='s', label="India", color="orange")
    st.subheader("🌏 Comparison: EU vs India")

ax.set_xlabel("Year")
ax.set_ylabel("Renewable Energy Share (%)")
ax.set_title("Growth of Renewable Energy (2014–2023)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.markdown("---")
st.write("📊 *This dashboard compares the growth of renewable energy in the EU and India using verified public datasets (2014–2023).*")


