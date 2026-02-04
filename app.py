import streamlit as st
import pandas as pd

st.set_page_config(page_title="Streamlit Azure PFE")

st.title("Hello Streamlit on Azure 🎉")

file = st.file_uploader("Upload CSV", type="csv")

if file:
    df = pd.read_csv(file)
    st.dataframe(df)
