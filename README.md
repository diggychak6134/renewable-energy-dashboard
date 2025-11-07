# ☀️ Solar Power Efficiency Simulator

A simple Streamlit web app that simulates solar energy generation based on panel power, efficiency, and sunlight hours.

---

## 🔍 Overview
This app helps visualize how much electricity a small solar setup can produce per day or over multiple days.  
It’s ideal for understanding renewable energy output for different conditions.

---

## ⚙️ How It Works
The app takes user inputs such as:
- Average sunlight hours per day  
- Solar panel rated power (in Watts)  
- Panel efficiency (in %)  
- Duration (in days)

It then calculates:
- **Daily Energy Output (Wh/day)**
- **Total Energy Generated over time**

and displays an interactive chart of cumulative energy.

---

## 🧰 Tools Used
- Python  
- Streamlit  
- Matplotlib  
- NumPy  
- Pandas  

---

## 🚀 How to Run
### Option 1: Online
View it live here:  
👉 [Your Streamlit App Link](https://yourusername-renewable-energy-dashboard.streamlit.app)

### Option 2: Local (if running on PC)
```bash
pip install streamlit pandas numpy matplotlib
streamlit run app.py
