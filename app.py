import streamlit as st
import plost
import pandas as pd 
#st.header("BTCUSD Price Prediction")
st.title('BTCUSD Price Prediction')
st.write("This is my first app")
df = pd.read_csv('https://raw.githubusercontent.com/pseksa/webapp/main/BTC-USD.csv')
st.write (df)
st.line_chart(df['Close'])


plost.line_chart(
    data=df,
    x='Date',
    y=('Open', 'Close', 'High', 'Low'))
