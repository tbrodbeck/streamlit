import streamlit as st
import pandas as pd

# ----------------------------------------Basic configs------------------------------------------------------------------
st.set_page_config(layout="wide")

st.markdown("# What you would like to watch next?")

# Page layout
sd_bar = st.sidebar
sd_bar.header("User input")

expander = st.expander("Sources and libraries")
expander.markdown("""
* Data source ...;
* IBM tools:
* Python packages such as pandas, 
* Python packages and corresponding libraries such as pandas, requests, streamlit, plotly and BeautifulSoup;
* Inspiration from out DS EMEA bootcamp2
"""
                  )

# --------------------- USER INPUTS ------------------------------
param_0 = sd_bar.checkbox("I do not want to fill your inputs", False)

param_1_list = dict(
    {0: "<18",
     1: "18-40",
     2: "40-65",
     3: ">65"}
)
param_1 = sd_bar.radio("Age group", param_1_list.values())

param_2_list = ['Drama', 'Horror', 'Romantic']
param_2 = sd_bar.multiselect("Select your favourite genres",
                           param_2_list,
                           )
param_3 = sd_bar.slider("Maximum length in mins", 0, 300)

#------------------------ OUTPUTS------------------------------------
st.markdown("### Initial prediction")

st.markdown("Harry Potter")
st.markdown("[Link to imdb] (https://www.imdb.com/title/tt0241527/?ref_=tt_mv_close)")