# -*- coding: utf-8 -*-
# importing libraries 
import streamlit as st 
import pandas as pd
import numpy as np
import scipy as sp
import plotly.offline as py
from  plotly.offline import plot
import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

from plotly.offline import init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)
import cufflinks as cf
cf.go_offline()

# logistics: changing page icon and setting title
st.set_page_config(
  page_title= 'FAID and Fertility',
  page_icon= ':smiley:', 
  initial_sidebar_state= 'expanded')
st.title("Welcome to my Streamlit webpage!")

# page 1: 
st.markdown("# Financial AID at AUB 💰")
st.sidebar.markdown("# Financial AID at AUB 💰")

st.markdown('In this page, we will generate some visuals trying to get insights from the data of FAID applicants ar AUB in fall 2021: ')

#Reading the data
my_df=pd.read_csv("FAID.csv")
if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(my_df)
    
st.header("Students Getting Financial Aid by Mohafaza")

# some "mohafaza" values are string : "0" which makes no sense. so we will remove them 
Indexes=my_df[my_df['MOHAFAZA'] == "0" ].index
my_df.drop( Indexes , inplace=True)


# making some changes to the data: 
# changing some names of mohafazat
my_df['MOHAFAZA']=my_df['MOHAFAZA'].str.replace('Nabatieh','Nabatiyeh')
my_df['MOHAFAZA']=my_df['MOHAFAZA'].str.replace('Baalbak Hermel','Baalbek Hermel')
my_df['MOHAFAZA']=my_df['MOHAFAZA'].str.replace('Bekaa','El Beqaa El Gharbi')
my_df['MOHAFAZA']=my_df['MOHAFAZA'].str.replace('Aakar','Akkar')

MOH=pd.read_csv("lon lat MOHAFAZA.csv") #  I created this dataset
new_df=pd.merge(my_df,MOH,on="MOHAFAZA")

# figure 1 
new_df.rename(columns={"Latitude" : 'lat', 'Longitude': 'lon'}, inplace=True)
map_data = new_df[['lat','lon']]
st.map(new_df)

# figure 2: 
st.subheader("Making the map more interactive")
fig = px.density_mapbox(new_df, lat = 'lat', lon = 'lon', radius=15, 
                       center = dict(lat=33.62379, lon=35.74879), 
                       zoom = 3.5,   # zoom = 17
                       hover_name = 'MOHAFAZA', 
                
                       opacity=0.7, 
                       mapbox_style = 'open-street-map',
                       width = 1280 ,
                       height =720 ,
                       title = 'Mohafazat where students getting FAID')
st.plotly_chart(fig)
#  figure 3:
FAID_approved_df=my_df[my_df['PERC']>0]  # this is to filter students with FAID more than zero- students who got FAID
fig = px.pie(FAID_approved_df,  names=my_df['MOHAFAZA'])
st.plotly_chart(fig)

# figure 4:
st.header('Count of students with FAID % with gender and if he/she is a medicine student')
fig = px.histogram(my_df, x="PERC",color='GENDER',pattern_shape="Med Student (Yes/No)")
st.plotly_chart(fig)

# Third figure: 
st.header('FAID % vs father income with tuition (size) and Mohafaza (color)')
my_df.dropna(inplace=True)
fig=px.scatter(my_df, y="PERC", x="FATHER_INCOME", color="MOHAFAZA", size="TUITION", size_max=30,
          hover_name="TUITION")
st.plotly_chart(fig)

# page 2: 
st.markdown("# Fertility Rate Across the World 👦")
st.sidebar.markdown("# Fertility rate 👦")

# Fertility: 
st.markdown('In this page we will look into the different fertility rate trends across the world. ')
link= 'https://www.gapminder.org/data/'

st.markdown("We're using 3 different datasets from the [GapMinder website.](%s)" %  link)
st.markdown("""First one is about countries GDP per Capita,
second one is about countries population size, and third one is about countries fertility rates. We concatenated them into one dataset 
to come up with meaningful insights.""")

# Reading the data:
df=pd.read_csv("Fertility.csv")

# Setting a sidebar:
df_container= st.container()


Menu_Items= ['Filter by Fertility Rate', 'View all fertility rates']
Menu_choice= st.sidebar.selectbox('Select the Option', Menu_Items)


if Menu_choice== 'View all fertility rates':
    with df_container:    
        st.subheader("Full Data with all Fertility Rates:")
        st.write(df)

elif Menu_choice== 'Filter by Fertility Rate':
        st.header('Determine Fertility Rate Range:')
        range= st.slider('Slide & Pick', 0.0,10.0, (2.0,7.0))
    
        st.write(range)
        filtered_table= df[df['Fertility'].between(range[0], range[1])]
        st.write(filtered_table)
# figure 1 
st.header("GDP and Population Growth Across Years")
page = st.sidebar.selectbox('GDP and Population Growth',
  ['Country Data','Continent Data'])

if page == 'Country Data':
  ## Countries
    clist = df['country'].unique()

    country = st.selectbox("Select a Country:",clist)
    col1, col2 = st.columns(2)

    fig = px.line(df[df['country'] == country], 
    x = "Year", y = "GDP",title = "GDP per Capita")

    col1.plotly_chart(fig,use_container_width = True)

    fig = px.line(df[df['country'] == country], 
    x = "Year", y = "Population",title = "Population Growth")
  
    col2.plotly_chart(fig,use_container_width = True)

else:
  ## Continents
    contlist = df['Continent'].unique()
 
    continent = st.selectbox("Select a continent:",contlist)
    col1,col2 = st.columns(2)
    fig = px.line(df[df['Continent'] == continent], 
    x = "Year", y = "GDP",
    title = "GDP per Capita",color = 'country')
    col1.plotly_chart(fig)

    fig = px.line(df[df['Continent'] == continent], 
    x = "Year", y = "Population",
    title = "Population",color = 'country')
  
    col2.plotly_chart(fig, use_container_width = True)

# Figure 2 

st.header("Population Growth per Continent")
year_to_filter = st.slider('year',2000, 2020, 2000)
filtered_data =df[df['Year'] == year_to_filter]

fig = px.bar(filtered_data, x="Continent", y="Population", color="Continent",
   hover_name= 'country',  range_y=[0,1000000000])
st.plotly_chart(fig)

# Figure 3 
st.subheader('Average Fertility Rate in Each Country Throughout the Years')
fig= px.line(df, x= 'Year', y= 'Fertility', color= 'Continent', line_group= 'country', hover_name= 'country', 
       line_shape= 'spline', render_mode= 'svg')
st.plotly_chart(fig)


st.sidebar.title('')
st.sidebar.title('Contact Details:')

url = "http://linkedin.com/in/rani-abudehn"
st.sidebar.write("* Name: Rani Abu Dehn")
st.sidebar.write("* LinkedIn Account: [LinkedIn](%s)" % url)
st.sidebar.write("* Email: raa179@mail.aub.edu")
