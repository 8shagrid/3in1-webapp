import streamlit as st
from st_on_hover_tabs import on_hover_tabs


def show_hover_tabs():
    st.markdown(
        "<style>" + open("css/style.css").read() + "</style>", unsafe_allow_html=True
    )

    with st.sidebar:
        selected2 = on_hover_tabs(
            tabName=["Home", "Dashboard", "Advanced Analysis", "Churn Prediction"],
            iconName=["house", "bar_chart", "tune", "smart_toy"],
            styles={
                "navtab": {
                    "background-color": "#111",
                    "color": "#818181",
                    "font-size": "18px",
                    "font-weight": "bold",
                    "transition": ".3s",
                    "white-space": "nowrap",
                    "text-transform": "capitalize",
                },
                "tabOptionsStyle": {
                    ":hover :hover": {"color": "white", "cursor": "pointer"}
                },
                "iconStyle": {
                    "position": "fixed",
                    "left": "7.5px",
                    "text-align": "left",
                },
                "tabStyle": {
                    "list-style-type": "none",
                    "margin-bottom": "30px",
                    "padding-left": "30px",
                },
            },
            key="1",
            default_choice=0,
        )

    return selected2
