import pandas as pd


def load_data():
    data = pd.read_excel("dataset/Telco_customer_churn_adapted_v2.xlsx")
    return data
