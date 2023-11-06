import pandas as pd
import streamlit as st
import joblib


def show_churn_prediction():
    st.header("Churn Prediction")

    col1, col2 = st.columns(2)

    with col1:
        tenure_months = st.number_input("Tenure Months", value=1)
        device_class = st.selectbox("Device Class", ["Low End", "Mid End", "High End"])
        games_product = st.selectbox("Games Product", ["Yes", "No"])
        music_product = st.selectbox("Music Product", ["Yes", "No"])
        education_product = st.selectbox("Education Product", ["Yes", "No"])
    with col2:
        call_center = st.selectbox("Call Center", ["Yes", "No"])
        video_product = st.selectbox("Video Product", ["Yes", "No"])
        use_myapp = st.selectbox("Use MyApp", ["Yes", "No"])
        payment_method = st.selectbox(
            "Payment Method", ["Pulsa", "Digital Wallet", "Debit", "Credit"]
        )
        monthly_purchase = st.number_input("Monthly Purchase (in thousands of IDR)")

    if st.button("Predict Churn"):
        prediction = predict_churn(
            tenure_months,
            device_class,
            games_product,
            music_product,
            education_product,
            call_center,
            video_product,
            use_myapp,
            payment_method,
            monthly_purchase,
        )
        if prediction == 1:
            st.error("Churn Prediction: Yes")
        else:
            st.success("Churn Prediction: No")


def predict_churn(
    tenure_months,
    device_class,
    games_product,
    music_product,
    education_product,
    call_center,
    video_product,
    use_myapp,
    payment_method,
    monthly_purchase,
):
    input_data = pd.DataFrame(
        {
            "Tenure Months": [tenure_months],
            "Device Class": [device_class],
            "Games Product": [games_product],
            "Music Product": [music_product],
            "Education Product": [education_product],
            "Call Center": [call_center],
            "Video Product": [video_product],
            "Use MyApp": [use_myapp],
            "Payment Method": [payment_method],
            "Monthly Purchase": [monthly_purchase],
        }
    )

    model = joblib.load("model/model_xgboost.pkl")
    label_encoders = joblib.load("model/label_encoders.pkl")

    for col in input_data.columns:
        if col in label_encoders:
            input_data[col] = label_encoders[col].transform(input_data[col])

    prediction = model.predict(input_data)
    return prediction[0]
