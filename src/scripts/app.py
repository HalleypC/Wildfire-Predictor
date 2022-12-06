# run in conda under the virtual environment lighthouse_env
# streamlit run app.py

import streamlit as st
import requests
from streamlit_lottie import st_lottie

# ---- LOTTIE ----
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_coding = load_lottieurl("https://assets5.lottiefiles.com/packages/lf20_uletvhke.json")

# ---- PAGE CONFIG ----
# Find more emojis here: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="My Webpage", page_icon=":fire:", layout="centered")

# ---- HEADER SECTION ----
with st.container():
    st.title("Wildfire Predictor")
    st.subheader("By: Halley Chopra")
    st.write("To more effectively develop insights, tools, and make data driven decisions for the prevention and mitigation of wildfire, the cause of the wildfire is essential. With the cause known, we can perform data driven analyses to improve the allocation of targeted resouces and strategies to improve prevention and mitigation.")
    st.write("[Explore the project Repo >](https://github.com/HalleypC/Wildfire-Predictor)")
    
# ---- PREDICTOR INTRO ----
with st.container():
    st.write("---")
    left_column, right_column = st.columns(2)
    with left_column:
        st.header("About the Predictor")
        st.write("##")
        st.write(
            """
            This model can predict the cause of a wildfire with an accuracy of up to 84%. The model will predict one of 3 possible causes.
            - Natural: Lightning
            - Human Accident: Equipment Use, Debris Burning, Campfire, Smoking, Children, Powerline, Fireworks, Railroad, Structure
            - Malicious: Arson
            Scroll down to make a prediction.
            """
        )
    with right_column:
        st_lottie(lottie_coding, height=300, key="coding")
        
# ---- PREDICTOR ----
import pickle
import bz2file as bz2
import pandas as pd
import datetime as dt

#pickle file too large for github
#model = pickle.load(open('model2.p','rb'))  
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = pickle.load(data)
    return data
model = decompress_pickle('pickle_compressed.pbz2')

from Preprocessing import weather_condition, open_weather_api     #my homemade functions

def predict_fire(date, FIRE_SIZE, LATITUDE, LONGITUDE, FIRE_DURATION, OWNER_DESCR):
    """
    returns the cause of the fire:
    (0) natural = ['Lightning']
    (1) accidental = ['Structure','Fireworks','Powerline','Railroad','Smoking','Children','Campfire','Equipment Use','Debris Burning']
    (2) malicious = ['Arson']
    
    """
    
    #calcualate date features:
    FIRE_YEAR = date.year
    DISC_MONTH = date.month 
    DISC_DAY = date.day
    DISC_DAYOFWEEK = date.weekday()
    DISCOVERY_DOY = date.timetuple().tm_yday
    
    base_dict = {'FIRE_YEAR': FIRE_YEAR, 
           'DISCOVERY_DOY': DISCOVERY_DOY, 
           'FIRE_SIZE': FIRE_SIZE, 
           'LATITUDE': LATITUDE, 
           'LONGITUDE': LONGITUDE,
           'DISC_MONTH': DISC_MONTH, 
           'DISC_DAY': DISC_DAY, 
           'FIRE_DURATION': FIRE_DURATION, 
           'DISC_DAYOFWEEK': DISC_DAYOFWEEK,
           'OWNER_DESCR': OWNER_DESCR}
    
    #call the weather api (from Preprocessing.py)
    weather_dict = weather_condition(LATITUDE, LONGITUDE, date)
    
    #add these two dictionaries together
    input = {**base_dict, **weather_dict}
    
    df_input = pd.DataFrame(input.values(), index=input.keys()).transpose()
    prediction = model.predict(df_input)
    return prediction


# ---- MODEL FORM ----
with st.container():
    st.write("---")
    #st.header("Make a Prediction")
    
    html_temp = """
    <div style="background:#025246 ;padding:10px">
    <h2 style="color:white;text-align:center;">Wildfire Cause Prediction</h2>
    </div>
    """
    st.markdown(html_temp, unsafe_allow_html = True)
    st.write("##")
    date = st.date_input("Fire Ignition Date")
    FIRE_SIZE = st.number_input("Fire Size (acres)")
    LATITUDE = st.number_input("Latitide")
    LONGITUDE = st.number_input("Longitude")
    FIRE_DURATION = st.number_input("Fire Duration (days)")
    OWNER_DESCR = st.selectbox("Choose the Land Owner Type (Name of entity responsible for managing the land at the point of origin of the fire at the time of the incident.)",
                               ['PRIVATE', 'USFS', 'BLM', 'MISSING/NOT SPECIFIED',
                                'STATE OR PRIVATE', 'COUNTY', 'UNDEFINED FEDERAL', 'STATE', 'FWS',
                                'NPS', 'BOR', 'MUNICIPAL/LOCAL', 'TRIBAL', 'OTHER FEDERAL', 'BIA'])
    
#Results:
    natural_html = """  
    <div style="background-color:#edd1cb; padding:10px >
    <h2 style="color:white;text-align:center;">Natural Cause - Lightning</h2>
    </div>
    """
    accident_html = """  
    <div style="background-color:#edd1cb ;padding:30px >
    <h2 style="color:white;text-align:left;">Accidental Human Cause</h2>
    </div>
    """
    mal_html= """
    <div style="background-color:#edd1cb; padding:10px >
    <h2 style="color:black;text-align:center;">Malicious Cause - Arson</h2>
    </div>
    """
    
#Button: 
    if st.button("Predict the cause"):
        output = predict_fire(date, FIRE_SIZE, LATITUDE, LONGITUDE, FIRE_DURATION, OWNER_DESCR)
        st.success('Prediction successful.')

        if output == 1:
            st.markdown(natural_html,unsafe_allow_html=True)
        elif output == 2:
            st.markdown(accident_html,unsafe_allow_html=True)
        elif output == 3:
            st.markdown(mal_html,unsafe_allow_html=True)

# if __name__=='__main__':
#     main()
