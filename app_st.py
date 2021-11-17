import streamlit as st
from streamlit_player import st_player
import pandas as pd
from decouple import config
import requests
import re

from movie_recommender import get_movie_recommendation, return_titles_users
from GENRE import recommend_top_5_existing_user
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
reg_user = sd_bar.radio("Are you registered user?", ["Yes", "No"])
param_0 = False
titles_list, users_list = return_titles_users()
error_message = None
recommendations = None
# to check if the user is registered, then to ask for id
if reg_user == "Yes":
    with sd_bar.form(key="user_form"):
        user_id = st.text_input("Enter you id here")
        submit_button = st.form_submit_button(label="Submit")
        if user_id.isnumeric():
            user_id = int(user_id)
            if user_id not in users_list:
                error_message = "User id was not recognized"
            else:
                recommendations = recommend_top_5_existing_user(user_id)
        else:
            error_message = "The format of user id is wrong"
    

else:
    with sd_bar.form(key="user_form"):
        movies_list = titles_list
        movie_select = st.selectbox("Select your favourite movie",
                                       movies_list,
                                       )
        submit_button = st.form_submit_button(label="Submit")
        recommendations = get_movie_recommendation(movie_select)
        submit_button = True
    param_0 = sd_bar.checkbox("No movie preference", False)
    # no need to submit the form then
    
        # with sd_bar.form(key="user_form"):
        #     # to add from data
        #     age_list = dict(
        #         {0: "<18",
        #          1: "18-40",
        #          2: "40-65",
        #          3: ">65"}
        #     )
        #     age_input = st.radio("Age group", age_list.values())

        #     genres_list = ['Drama', 'Horror', 'Romantic']
        #     genres_input = st.multiselect("Select your favourite genres",
        #                                genres_list,
        #                                )
        #     param_3 = st.slider("Maximum length in mins", 0, 300)
        #     submit_button = st.form_submit_button(label="Submit")


# ------------------------ OUTPUTS------------------------------------
def get_movie_trailer(name):
    r = requests.get(f'https://www.youtube.com/results?search_query={name}+trailer')
    video_link = None
    if r.status_code == 200:
        video_code = re.findall('watch\?v..{11}', r.text)
        video_link = 'https://www.youtube.com/watch?v=' + video_code[0][-11:]
    return video_link



if not submit_button and not param_0:
    st.markdown('<h3 style="color:red">Please enter the data on the left panel and submit</h3>', unsafe_allow_html=True)
elif error_message:
    st.markdown(f'<h3 style="color:red">{error_message}</h3>', unsafe_allow_html=True)
elif param_0:
    recommendations = pd.read_csv('top5.csv')
    print(param_0)
    param_0 = False

if not recommendations is None:
    # to get embedded youtube video
    # get all columns to lower
    # and to write down all recommendations
    recommendations.columns = map(lambda col: col.lower(), recommendations.columns)
    
    for count, (_, row) in enumerate(recommendations.iterrows()):
        cur_title = row['title']
        st.markdown(f'<h3 style="color:violet">{count+1}. {cur_title}</h3>', unsafe_allow_html=True)
        video_link = get_movie_trailer(cur_title)
        if not video_link is None:
            st.markdown("### *Youtube search results*")
            print(video_link)
            st_player(video_link)
        st.markdown("")
    recommendations = None

