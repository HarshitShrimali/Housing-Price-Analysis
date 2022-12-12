import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium import Choropleth, Circle, Marker
from folium.plugins import HeatMap, MarkerCluster
from streamlit_folium import st_folium
data = pd.read_csv('HousingPrices.csv')
data=data.drop(['id','date'], axis=1)
data['bathrooms'] = data['bathrooms'].round()
data['floors']= data['floors'].round()
data = data.astype({"bathrooms":'int', "floors":'int'})
df = data.groupby(['zipcode']).mean()
df = df[['lat','long']]
df.columns = ['latitude', 'longitude']
df = df.reset_index()
zipcode = data['zipcode'].unique()
zipcode.sort()
location = {}
for i in range(len(df)):
    location[df['zipcode'][i]] = [df['latitude'][i],df['longitude'][i]]

data['count']=(data.groupby("yr_built")['yr_built'].transform('count'))
page_bg_image = """
<style>
[data-testid="stAppViewContainer"]{
    background: linear-gradient(90deg, #0700b8 0%, #00ff88 100%);
}
[data-testid="stSidebar"]{
    background-color: rgba(0,0,0,0);
}
[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}
div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]{
    background-color: #ffffff;
}
div.stSlider > div[data-baseweb="slider"] > div > div > div > div{ 
    color: #ffffff; 
}
button[data-baseweb="tab"] {
  background-color: rgba(0,0,0,0);
  color: #ffffff;
  font-size: 16px
}
div.stSlider > label{ 
    font-size: 16px; 
}
[data-testid="stTickBarMin"]{
    font-size: 15px;
}
[data-testid="stTickBarMax"]{
    font-size: 15px;
}
div.row-widget stSelectbox > label{ 
    font-size: 16px; 
}
</style>
"""
st.markdown(page_bg_image, unsafe_allow_html=True)

st.title("Housing prices in Kings County Washington")
st.sidebar.title("Please make Selection")
year_range = st.sidebar.slider('Select a range of House Year Build',data['yr_built'].min(),data['yr_built'].max(), (data['yr_built'].min(),data['yr_built'].max()))
Zipcod_select = st.sidebar.selectbox("Select Zipcode",zipcode)

dat = data[((data['yr_built'] > year_range[0]) & (data['yr_built'] <= year_range[1])) & ((data.zipcode == Zipcod_select))]
da = (dat.groupby(['yr_built']).mean())
da = da.reset_index()

if "button_click" not in st.session_state:
    st.session_state.button_click = False
def Feature_plot():
    #placeholder = st.empty()
    # st.session_state.page = 0
    # if st.session_state.page == 0:
    st.session_state.button_click =True
    container2 = st.container()
    with container2:
        st.title("House features Analysis")
        tab1,tab2,tab3,tab4,tab5 = st.tabs(['Year Built Analysis', 'Bedrooms Count','Bathrooms Count','House conditions Distribution','DataFrame(Year_Build)'])
        with tab1:
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            fig.add_trace(
                go.Scatter(x=da['yr_built'], y=da['price'], name="price", mode="lines",marker=dict(color = 'green')),
                secondary_y=True)

            fig.add_trace(
                go.Bar(x=da['yr_built'], y=da['count'], name="count",marker=dict(color = 'lightblue')),
                secondary_y=False)

            fig.update_xaxes(title_text="yr_built")

            # Set y-axes titles
            fig.update_yaxes(title_text="count", secondary_y=False)
            fig.update_yaxes(title_text="price", secondary_y=True)
            fig.update_layout(title_text="Avg. Price as per build Year and No. of houses built per year",width=900)

            st.plotly_chart(fig)
        with tab2:
            fig1, ax = plt.subplots(1,figsize=(15,7))
            plt.title("Bedroom Count Plot", fontsize = 18)
            a = sns.countplot(x= 'bedrooms', data=dat)
            for container in a.containers:
                a.bar_label(container, fontsize = 12)
            a.set_xlabel('Bedrooms', fontsize = 15)
            a.set_ylabel('Count of Houses', fontsize = 15)
            a.tick_params(labelsize=15)
            st.pyplot(fig1)
        with tab3:
            fig2, ax = plt.subplots(1,figsize=(15,7))
            plt.title("Bathroom Count Plot", fontsize = 18)
            b= sns.countplot(x= 'bathrooms', data=dat)
            for container in b.containers:
                b.bar_label(container, fontsize = 12)
            b.set_xlabel('Bathrooms', fontsize = 15)
            b.set_ylabel('Count of Houses', fontsize = 15)
            b.tick_params(labelsize=15)
            st.pyplot(fig2)
        with tab4:
            y =dat.groupby('condition').size()
            y=y.to_frame()
            y.reset_index(inplace=True)
            y = y.rename(columns={0: "count"})
            fig3, ax = plt.subplots(1,figsize=(8,3))
            plt.title('House Conditions',fontsize = 10)
            plt.pie(y['count'], autopct='%1.1f%%',labels=y['condition'])
            st.pyplot(fig3)
        with tab5:
            dt = (dat.groupby(['yr_built']).mean())
            dt = dt.reset_index()
            dt['bathrooms'] = dt['bathrooms'].round()
            dt['floors']= dt['floors'].round()
            dt['bedrooms'] = dt['bedrooms'].round()
            dt['condition']= dt['condition'].round()
            dt['grade']= dt['grade'].round()
            dt = dt.astype({"bathrooms":'int', "floors":'int',"bedrooms":'int', "condition":'int',"grade":'int',"zipcode":'int',"count":'int'})
            dt = dt.drop(['waterfront','view','yr_renovated','lat','long','sqft_living15','sqft_lot15'], axis=1)
            st.dataframe(dt)         

container1 = st.container()
with container1:
    col1, col2,col3,col4 = st.columns(4)
    with col1:
        Bedroom_select = st.selectbox("No. of Bedrooms",[1,2,3,4,5])
    with col2:
        Bathroom_select = st.selectbox("No. of Bathrooms",[1,2,3])
    with col3:
        Floors_select = st.selectbox("No. of Floors",[1,2,3])
    with col4:
        Condition_select = st.selectbox("House Condition",[1,2,3,4,5])

map = folium.Map(location=location[Zipcod_select], tiles='openstreetmap', zoom_start=8)
for idx, row in dat[(dat.bedrooms == Bedroom_select) & (dat.bathrooms == Bathroom_select) & (dat.condition == Condition_select) & ((dat.floors == Floors_select))].iterrows():
    Marker([row['lat'], row['long']]).add_to(map)
    popup_text = "Price: {}, Sqft: {}, Condition:{}, Beds: {}, Baths: {}, Floors: {}, Year: {}".format(row['price'],row['sqft_living'],row['condition'], row['bedrooms'],row['floors'],row['bathrooms'],row['yr_built'])
    popup = folium.Popup(popup_text, parse_html=True)
    marker = folium.Marker([row['lat'], row['long']], popup=popup).add_to(map)
st_data = st_folium(map, height=500, width= 900)
Features = st.sidebar.button("Show Analysis", on_click=Feature_plot,key='button_click')