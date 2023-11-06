import streamlit as st
from tabs import show_hover_tabs
from home import show_home
from dashboard import show_dashboard
from advanced_analysis import show_advanced_analysis
from churn_prediction import show_churn_prediction


def main():
    st.set_page_config(page_title="3 in 1", layout="wide")
    selected2 = show_hover_tabs()

    if selected2 == "Home":
        show_home()
    elif selected2 == "Dashboard":
        show_dashboard()
    elif selected2 == "Advanced Analysis":
        show_advanced_analysis()
    elif selected2 == "Churn Prediction":
        show_churn_prediction()


if __name__ == "__main__":
    main()
