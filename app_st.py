import streamlit as st
from streamlit_player import st_player
import pandas as pd
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
            error_message = "The format of user id is wrong"
    recommendations = return_titles_users(user_id)

else:
    with sd_bar.form(key="user_form"):
        movies_list = titles_list
        movie_select = st.selectbox("Select your favourite movie",
                                       movies_list,
                                       )
        submit_button = st.form_submit_button(label="Submit")
        recommendations = get_movie_recommendation(movie_select)
    param_0 = sd_bar.checkbox("No movie preference", False)
    # no need to submit the form then
    submit_button = True

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

if not submit_button and not param_0:
    st.markdown('<h3 style="color:red">Please enter the data on the left panel and submit</h3>', unsafe_allow_html=True)
elif error_message:
    st.markdown(f'<h3 style="color:red">{error_message}</h3>', unsafe_allow_html=True)

elif param_0:
    top5 = pd.read_csv('top5.csv')
    top5.index = range(1, 6)
    st.write(top5)
    param_0 = False
else:
    st.markdown("### Initial prediction is")
    # st.markdown('<h3 style="color:violet">Harry Potter</h3>', unsafe_allow_html=True)
    # st.markdown("### *Youtube search results*")
    # # to get embedded youtube video
    # # enter https://codefather.tech/blog/youtube-search-python/
    # """ query is like this
    # https: // www.youtube.com / results?search_query = harry + potter + trailer"""
    # st_player('https://www.youtube.com/watch?v=VyHV0BRtdxo')

    # to get embedded youtube video

    print(recommendations)
    st.write(recommendations)
    submit_button = False
