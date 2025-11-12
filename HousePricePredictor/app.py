import streamlit as st
import numpy as np
import pickle

# Load the trained models and transformer
linear_model = pickle.load(open('linear_model.pkl', 'rb'))
poly_model = pickle.load(open('poly_model.pkl', 'rb'))
poly_transform = pickle.load(open('poly_transform.pkl', 'rb'))  # PolynomialFeatures transformer


st.set_page_config(
    page_title="California House Price Predictor",
    page_icon="🏠",
    layout="centered"
)

st.markdown("""
    <style>
    /* Reduce top and bottom padding of main content */
    .block-container {
        padding-top: 1rem !important;   /* default ~6rem होता है */
        padding-bottom: 2rem !important;
    }
    </style>
""", unsafe_allow_html=True)


st.markdown("<h1 style='text-align:center; color:#4CAF50; '>🏡 California Housing Price Predictor</h1>", unsafe_allow_html=True)
st.markdown("""
<p style='text-align:center; font-size:17px;'>
Use this app to predict the <b>Median House Value</b> based on California housing data.  
Switch between <b>Linear Regression</b> and <b>Polynomial Regression</b> for comparison.
</p>
""", unsafe_allow_html=True)


st.sidebar.header("⚙️ Model Configuration")
model_choice = st.sidebar.radio(
    "Choose Regression Model",
    ["Linear Regression", "Polynomial Regression"],
    index=0,
    help="Switch between Linear or Polynomial Regression"
)

st.sidebar.info(
    f"📊 Current Model: **{model_choice}**"
)


st.markdown("### 🧩 Enter House Features")

col1, col2 = st.columns(2)

with col1:
    MedInc = st.number_input("Median Income (×$10,000)", min_value=0.0, max_value=15.0, step=0.1, value=4.0)
    HouseAge = st.number_input("Median House Age (years)", min_value=1, max_value=60, step=1, value=20)
    AveRooms = st.number_input("Average Rooms per Household", min_value=1.0, max_value=15.0, step=0.1, value=5.0)
    AveBedrms = st.number_input("Average Bedrooms per Household", min_value=0.5, max_value=5.0, step=0.1, value=1.0)

with col2:
    Population = st.number_input("Population in Block", min_value=100, max_value=10000, step=100, value=1000)
    AveOccup = st.number_input("Average Household Size", min_value=1.0, max_value=6.0, step=0.1, value=3.0)
    Latitude = st.number_input("Latitude", min_value=32.0, max_value=42.0, step=0.1, value=36.5)
    Longitude = st.number_input("Longitude", min_value=-125.0, max_value=-114.0, step=0.1, value=-120.0)


features = np.array([[MedInc, HouseAge, AveRooms, AveBedrms, Population, AveOccup, Latitude, Longitude]])


st.markdown("---")
if st.button("🔮 Predict House Price", use_container_width=True):
    with st.spinner("Predicting... Please wait ⏳"):
        if model_choice == "Linear Regression":
            prediction = linear_model.predict(features)
        else:
            poly_features = poly_transform.transform(features)
            prediction = poly_model.predict(poly_features)
        
        st.markdown("### ✅ Predicted Median House Value:")
        st.success(f"💰 **${prediction[0] * 100000:,.2f}**")


st.markdown("""
---
<p style='text-align:center; font-size:14px; color:grey; margin-bottom:-55  px;'>
Made with ❤️ by <b>Shreya Jain</b><br>
Trained on <i>California Housing Dataset</i> using <b>scikit-learn</b>.
</p>
""", unsafe_allow_html=True)
