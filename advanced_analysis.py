import streamlit as st
import pygwalker as pyg
import streamlit.components.v1 as components
from data_manager import load_data


def show_advanced_analysis():
    st.header("Advanced Analysis")

    pyg_html = pyg.walk(load_data(), return_html=True)
    components.html(pyg_html, height=1000, scrolling=True)
