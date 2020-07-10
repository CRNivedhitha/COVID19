import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.express as px
import warnings


st.title("INDIA COVID-19")
st.markdown("A small analysis about the number of COVID-19 confirmed cases,deaths and cured count in INDIA using streamlit and python!!")
DATA=("COVID-DATASET.csv")
@st.cache(persist=True)
@st.cache(allow_output_mutation=True)
#LOAD DATA

def load_data(nrows):
    data=pd.read_csv(DATA,nrows=nrows,parse_dates=[['Date','Time']])
    data.rename(columns={"Date_Time": "date/time"}, inplace=True)
    return data
data=load_data(2000)

#VISUALIZING IN A MAP

#latitude=20.5937 
#longitude=78.9629
#st.header("Most affected region")
#affected_people=st.slider("No. of people affected ",100,200)
#st.map(data.query("Confirmed>=@affected_people")[['latitude','longitude']].dropna(how='any'))

#ON SPECIFYING THE TIME

st.header("Approximately,how many cases were found during the given time")
hour=st.slider("Hours to look at",0,23)
original_data = data
data = data[data['date/time'].dt.hour==hour]


#PLOT THE FILTERED DATA

st.markdown("No.of cases between %i:00 and %i:00"%(hour,(hour+1)%24))
st.subheader('RAW DATA')
st.write(data)


#GRAPH 
midpoint = (np.average(original_data["latitude"]), np.average(original_data["longitude"]))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
        "HexagonLayer",
        data=data[['date/time', 'latitude', 'longitude']],
        get_position=["longitude", "latitude"],
        auto_highlight=True,
        radius=100,
        extruded=True,
        pickable=True,
        elevation_scale=4,
        elevation_range=[0, 1000],
        ),
    ],
))

st.subheader("Cases by hour between %i:00 and %i:00" % (hour, (hour + 1) % 24))
filtered = data[(data['date/time'].dt.hour >= hour) & (data['date/time'].dt.hour < (hour + 1))]

hist = np.histogram(filtered['date/time'].dt.hour, bins=24, range=(0, 23))[0]
chart_data = pd.DataFrame({"hour": range(24), "Confirmed": hist})
fig = px.bar(chart_data, x='hour', y='Confirmed', hover_data=['hour', 'Confirmed'], height=400)
st.write(fig)

#SELECTING TOP 5 AFFECTED STATES(DEATHS,CONFIRMED,CURED)

st.header("Top 5 dangerous states by affected class")
select = st.selectbox('Affected class', ['Deaths','Cured','Confirmed'])

if select == 'Deaths':
    st.write(original_data.query("Deaths >= 1")[[ "Deaths"]].sort_values(by=['Deaths'], ascending=False).dropna(how="any")[:5])

elif select == 'Cured':
    st.write(original_data.query("Cured >= 1")[[ "Cured"]].sort_values(by=['Cured'], ascending=False).dropna(how="any")[:5])

else:
    st.write(original_data.query("Confirmed >= 1")[["Confirmed"]].sort_values(by=['Confirmed'], ascending=False).dropna(how="any")[:5])


if st.checkbox("Show Raw Data", False):
    st.subheader('Raw Data')
    st.write(data)


