import streamlit as st
import pandas as pd
import base64
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import yfinance as yf
import requests
import bs4
from bs4 import BeautifulSoup

st.title('Price Prediction System')

st.markdown("""
This app performs simple webscraping of Tradingview Idea data!
* **Python libraries:** base64, pandas, streamlit
* **Data source:** [Tradingview.com](https://www.tradingview.com/ideas).
""")

st.sidebar.header('User Input Features')

# Web scraping of S&P 500 data
#
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    df = html[0]
    return df
#df = pd.read_csv('Idea.csv')
df = pd.read_csv('crypto.csv')
#df = load_data()
sector = df.groupby('crypname')

# Sidebar - Sector selection
sorted_sector_unique = sorted( df['crypname'].unique() )
selected_sector = st.sidebar.multiselect('crypname', sorted_sector_unique, sorted_sector_unique)

# Filtering data
df_selected_sector = df[ (df['crypname'].isin(selected_sector)) ]

st.header('Scraping Data')
st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df_selected_sector)

# Download S&P500 data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="crypto_idea.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# https://pypi.org/project/yfinance/

data = yf.download(
        tickers = list(df_selected_sector[:10].crypname),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )

# Plot Closing Price of Query Symbol
df2 = pd.read_csv('crypto.csv')
df2['Count'] = df2.desc.apply(lambda x: len(str(x).split(' ')))
df2['PostDate'] = pd.to_datetime(df2['stats'],unit='s')
df2['info']=df2['info'].replace(regex=['Long'],value=',Long')
df2['info']=df2['info'].replace(regex=['Short'],value=',Short')
df2['info']=df2['info'].replace(regex=['Education'],value=',Education')
#df2[['Assets', 'Timeframe','Position']] = df2['info'].str.split(',', expand=True)
df2['Position']=df2['Position'].replace(regex=['None'],value='Neutral')
df2.drop('title', axis=1, inplace=True)
df2.drop('info', axis=1, inplace=True)
df2.drop('author', axis=1, inplace=True)
df2.drop('stats', axis=1, inplace=True)
df2.drop('link', axis=1, inplace=True)
#df2.drop('social', axis=1, inplace=True)
#df2.to_csv('clean.csv', index=True)
def price_plot(symbol):
  df2 = pd.DataFrame(data[symbol].Close)
  df2['Date'] = df.index
  plt.fill_between(df2.Date, df2.Close, color='skyblue', alpha=0.3)
  plt.plot(df2.Date, df2.Close, color='skyblue', alpha=0.8)
  plt.xticks(rotation=90)
  plt.title(symbol, fontweight='bold')
  plt.xlabel('Date', fontweight='bold')
  plt.ylabel('Closing Price', fontweight='bold')
  return st.pyplot()

num_company = st.sidebar.slider('Number of Cryptocurrency', 1, 5)

if st.button('Sentiment'):
    from textblob import TextBlob
    import pandas as pd 
    df3 = pd.read_csv('clean.csv', encoding='utf8')
    polar = []
    subject = []
    #sentiment = []
    for item in df3['desc']:  
        sentence = TextBlob("slkdfskdjflsjf;lj;sdfj")
        polar.append(sentence.polarity)  # numerical score 0-1
        subject.append(sentence.subjectivity)  # 'POSITIVE' or 'NEGATIVE'
    df3['polarity'] = polar
    df3['subjectivity'] = subject
    sentiment = []
    for item in df3['polarity']:  
        if item > 0.3:
            sentiment.append("Positive")
        elif item > -0.3:
            sentiment.append("Nuetral")
        else:
            sentiment.append("Negative")
    df3['sentiment'] = sentiment
    df3.columns = ['id','desc','like','comment','Count','PostDate','Assets','Timeframe','Position','polarity','subjectivity','sentiment','aaa','bbb']
    df3.set_index('id')
    df3
    #df3.to_csv('sentiment.csv', index=True)

    
if st.button('Show Plots'):
    import streamlit as st
    import plost
    import pandas as pd 
    import datetime
    st.title('BTCUSD Price Prediction')
    st.write("From Tradingview Idea Opinion Mining")
    df = pd.read_csv('predict.csv')
    df['Date'] = pd.to_datetime(df['Date']).dt.date
    st.write (df)
    st.line_chart(df['Predict'])

if st.button('Price Prediction'):
    df = pd.read_csv('Idea26jany.csv')
    df.groupby(['postdate', 'sentiment'])['subjectivity'].describe()[['count', 'mean']]

    
