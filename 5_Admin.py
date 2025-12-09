import streamlit as st
from datetime import datetime

# ✅ Page Setup
st.set_page_config(page_title="Admin Panel", page_icon="🛠️", layout="wide")

# 🎨 Custom Styling
st.markdown("""
    <style>
        body { background-color: #0b0c10; color: #f8f9fa; font-family: 'Segoe UI', sans-serif; }
        h1, h2 { color: #66fcf1 !important; font-weight: 700; text-align: center; }
        .section { background: #1f2833; padding: 30px; border-radius: 15px; 
                   box-shadow: 0 6px 25px rgba(0,0,0,0.5); margin: 25px 0; text-align: center; }
        .tile { background: linear-gradient(135deg, #45a29e, #66fcf1);
                color: #0b0c10; border-radius: 15px; padding: 25px; text-align: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.4); transition: all 0.3s ease; cursor: pointer; }
        .tile:hover { transform: scale(1.03); box-shadow: 0 6px 25px rgba(102,252,241,0.5); }
        .tile h3 { color: #0b0c10; font-weight: 700; margin-bottom: 10px; }
        .tile p { color: #0b0c10; font-size: 14px; margin: 0; }
        footer { text-align: center; color: #c5c6c7; margin-top: 50px; font-size: 13px; }
    </style>
""", unsafe_allow_html=True)

# 🏠 Header
st.title("🛠️ MSME BI — Admin Panel")
st.markdown("### A calm and clear space to oversee your Business Intelligence environment.")

# 📊 Overview Section
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("📈 Quick Insights")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Active Dashboards", "12", "+3 this week")
with col2:
    st.metric("AI Predictions Generated", "248", "+12 today")
with col3:
    st.metric("Reports Downloaded", "57", "+9 today")
st.markdown("</div>", unsafe_allow_html=True)

# 🧭 Navigation Tiles
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("🧩 Admin Functional Areas")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📊 Dashboard Overview"):
        st.info("Navigating to Dashboard Overview...")
with col2:
    if st.button("🤖 AI Prediction Center"):
        st.info("Opening AI Prediction Insights...")
with col3:
    if st.button("📂 Report Management"):
        st.info("Accessing Report Downloads...")

st.markdown("</div>", unsafe_allow_html=True)

# 💡 Highlights Section
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.subheader("💡 System Highlights")
st.markdown("""
- MSME BI system operating **optimally**.
- AI modules running at **92% accuracy**.
- Recent data sync completed successfully.
- Reports updated **{}**.
""".format(datetime.now().strftime("%B %d, %Y %H:%M")), unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# 🪶 Footer
st.markdown("""
<footer>
    <hr>
    <p>✨ MSME BI Admin Panel | Designed for clarity and performance ✨</p>
</footer>
""", unsafe_allow_html=True)
