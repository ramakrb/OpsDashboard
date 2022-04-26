import streamlit as st
import pandas as pd
import datetime
from dateutil.relativedelta import relativedelta
import base64
#from scipy import stats
import matplotlib.pyplot as plt
from matplotlib.pyplot import rc
import seaborn as sns
import numpy as np
import os
from bs4 import BeautifulSoup
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
# from climata.usgs import DailyValueIO
# from climata.usgs import InstantValueIO

st.set_page_config(page_title="USBR Dashboard", page_icon='None', layout='wide', initial_sidebar_state='auto')
# st.header("RiverOps Dashboard")
# Initial Parameters
today = datetime.date.today() + datetime.timedelta(days=-1)
lastyear = today + relativedelta(years=-1)
previous = today + datetime.timedelta(days=-7)
day7 = today + datetime.timedelta(days=-6)
t2 = today.strftime("%Y-%m-%d")
t1 = previous.strftime("%Y-%m-%d")
t3=day7.strftime("%Y-%m-%d")
ly=lastyear.strftime("%Y-%m-%d")
sdid = '1930,2100,2101,1863,2166,2146,2119,3406,2064,2065,3364,2207,3408,3407,2204,2205,2208,1721,2086,2087'
sel_int = 'DY'

#maindf=pd.DataFrame()

#col1.title("Davis and Parker Stretch")
#st.header("Make Site / Parameter selection from the sidebar")

# start_date = col1.date_input('Start Date',previous)
# end_date = col1.date_input('End Date',today)
# t1 = start_date.strftime("%Y-%m-%d")
# t2 = end_date.strftime("%Y-%m-%d")
# col1.markdown("""
# ***
# """)
@st.cache
def load_data(sdid, sel_int, t1, t2, db='lchdb', table='R',mrid='0'):
    url = "https://www.usbr.gov/pn-bin/hdb/hdb.pl?svr=" + db + "&sdi=" + str(sdid) + "&tstp=" + \
          str(sel_int) + "&t1=" + str(t1) + "&t2=" + str(t2) + "&table=" + str(table) + "&mrid=" + str(mrid) + "&format=4"
    # st.write(url)
    html = pd.read_html(url)
    df1 = html[0]
    df1['DATETIME'] = pd.to_datetime(df1['DATETIME'])
    df1.set_index('DATETIME', inplace=True)
    return df1

df_elevn = load_data(sdid,sel_int,t1,t2)
mpy = load_data('1930,1721',sel_int,ly,ly)
#st.dataframe(df_elevn.iloc[1:,])
#st.dataframe(df_elevn[t3:t2].mean(axis=0))
avg = df_elevn[t3:t2].mean(axis=0)
strDate = "(as of  " + str(df_elevn.index[7].strftime("%m-%d-%Y") + ")")
header1 = '<p style="color:black; font-size: 20px;">' + strDate +'</p>'
medifflw = round((df_elevn.iloc[0]['SDI_1930']-df_elevn.iloc[7]['SDI_1930']),2)
mediffly = round((df_elevn.iloc[7]['SDI_1930']-mpy.iloc[0]['SDI_1930']),2)
mely = round(mpy.iloc[0]['SDI_1930'],2)
msly = round(mpy.iloc[0]['SDI_1721']/1000000,3)
mslyp = round(mpy.iloc[0]['SDI_1721']/26120000*100)
msdiffly = round((df_elevn.iloc[7]['SDI_1721'] - mpy.iloc[0]['SDI_1721'])/1000000,3)
# st.write(mediffly)

# st.dataframe(mpy)
st.header("Current Elevations ")
st.markdown(header1, unsafe_allow_html=True)
col1, col2, col3,col4 = st.columns((1,1,1,1))
# col1.write('')

col1.metric(label="Mead Elevation",value=str(df_elevn.iloc[7]['SDI_1930']) + " ft", delta =str(round((df_elevn.iloc[7]['SDI_1930']-df_elevn.iloc[0]['SDI_1930']),2)) + "  ft (since last week)")
col2.metric(label="Mohave Elevation",value=str(round(df_elevn.iloc[7]['SDI_2100'],2)) + " ft", delta =str(round(round(df_elevn.iloc[7]['SDI_2100'],2)-round(df_elevn.iloc[0]['SDI_2100'],2),2)) + "  ft (since last week)")
col3.metric(label="Havasu Elevation",value=str(round(df_elevn.iloc[7]['SDI_2101'],2)) + " ft", delta =str(round(round(df_elevn.iloc[7]['SDI_2101'],2)-round(df_elevn.iloc[0]['SDI_2101'],2),2)) + "  ft (since last week)")
# col4.metric(label="as of ", value=str(df_elevn.index[7].strftime("%m-%d-%Y")))

ly1, ly2, ly3, ly4 = st.columns((1,1,1,1))
ly1.metric(label="Mead Elevation (last year)", value=str(mely) + " ft", delta=str(mediffly)+ "  ft (since last year)")

st.header("Current Storage")
col21, col22, col23,col24 = st.columns((1,1,1,1))
col21.metric(label="Mead Storage",value=  str(round(df_elevn.iloc[7]['SDI_1721']/1000000,3)) + " maf  (" + str(round(df_elevn.iloc[7]['SDI_1721']/26120000*100)) + "%)")
col22.metric(label="Mohave Storage",value=  str(round(df_elevn.iloc[7]['SDI_2086']/1000000,3)) + " maf  (" + str(round(df_elevn.iloc[7]['SDI_2086']/1809800*100)) + "%)")
col23.metric(label="Havasu Storage",value=  str(round(df_elevn.iloc[7]['SDI_2087']/1000000,3)) + " maf  (" + str(round(df_elevn.iloc[7]['SDI_2087']/619400*100)) + "%)")

lys1, lys2, lys3, lys4 = st.columns((1,1,1,1))
lys1.metric(label="Mead storage (last year)", value=str(msly) + " maf  (" + str(mslyp) + "%)" , delta = str(msdiffly) + " maf (since last year)")

st.header("Average Releases")
col31, col32, col33,col34 = st.columns((1,1,1,1))
col31.metric(label="Hoover 7-day Release (Avg)",value=  str(round(avg[3])) + " cfs") #str(round(avg[3],0)) + " cfs")
col32.metric(label="Davis 7-day Release (Avg)",value=  str(round(avg[4])) + " cfs")
col33.metric(label="Parker 7-day Release (Avg)",value=  str(round(avg[5])) + " cfs")
