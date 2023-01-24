import requests
import pandas as pd
import bs4
from bs4 import BeautifulSoup
page = 1
title_list=[]
info_list=[]
author_list=[]
stats_list=[]
desc_list=[]
social_list=[]
like_list=[]
comment_list=[]
while page <= 500:
    #data = requests.get('https://th.tradingview.com/ideas/page-' + str(page))
    data = requests.get('https://www.tradingview.com/symbols/BTCUSDT/ideas/page-' + str(page))
    soup = bs4.BeautifulSoup(data.text)
    for c in soup.find_all('div',{'class' : 'tv-widget-idea js-userlink-popup-anchor'}):
        title_list.append(c.find('div',{'class':'tv-widget-idea__title-row'}).text.strip().replace('\n', ''))
        info_list.append(c.find('div',{'class':'tv-widget-idea__info-row'}).text.strip().replace('\n', ''))
        author_list.append(c.find('div',{'class':'tv-widget-idea__author-row'}).text.strip().replace('\n', ''))
        stats_list.append(c.find("span", class_="tv-card-stats__time js-time-upd")["data-timestamp"])
        desc_list.append(c.find('p',{'class':'tv-widget-idea__description-row tv-widget-idea__description-row--clamped js-widget-idea__popup'}).text.strip().replace('\n', ''))
        social_list.append(c.find('div',{'class':'tv-social-row tv-widget-idea__social-row'}).text.strip().replace('\n', ''))
        like_list.append(c.find('div',{'class':'tv-social-row__start'}).text.strip().replace('\n', ''))
        comment_list.append(c.find('div',{'class':'tv-social-row__end'}).text.strip().replace('\n', ''))       
    page += 1
    print('Complete page number: ' , page)
        
table = pd.DataFrame([title_list,info_list,author_list,stats_list,desc_list,social_list,like_list,comment_list]).transpose()
table.columns = ['title','info','author','stats','desc','social','like','comment_list']
table.set_index('title')

import datetime
df = pd.read_csv('Idea.csv')
df['Count'] = df.desc.apply(lambda x: len(str(x).split(' ')))
df['PostDate'] = pd.to_datetime(df['stats'], infer_datetime_format=True, unit="ms")
df['PostDate'] = df['PostDate']+datetime.timedelta(days=19361)
df['PostDate'] = df['PostDate'].dt.strftime('%Y-%m-%d')
df['info']=df['info'].replace(regex=['Long'],value=',Long')
df['info']=df['info'].replace(regex=['Short'],value=',Short')
df['info']=df['info'].replace(regex=['Education'],value=',Education')
table = df
table.columns = ['title','info','author','stats','desc','social','like','comment_list','Count','PostDate']
table.set_index('title')
#df


df[['Assets', 'Timeframe','Position']] = df['info'].str.split(',', expand=True)
df['Position']=df['Position'].replace(regex=['None'],value='Neutral')
df.drop('title', axis=1, inplace=True)
df.drop('info', axis=1, inplace=True)
df.drop('author', axis=1, inplace=True)
df.drop('stats', axis=1, inplace=True)
df.drop('social', axis=1, inplace=True)
#df

from textblob import TextBlob
polar = []
subject = []
#sentiment = []
for item in df['desc']:  
    sentence = TextBlob(item)
    polar.append(sentence.polarity)  # numerical score 0-1
    subject.append(sentence.subjectivity)  # 'POSITIVE' or 'NEGATIVE'
    
# add probability and sentiment predictions to tweets dataframe
df['polarity'] = polar
df['subjectivity'] = subject
#df['sentiments'] = sentiment
#df

#Textblob sentiment analyzer returns two properties for a given input sentence: 

#Polarity is a float that lies between [-1,1], -1 indicates negative sentiment and +1 indicates positive sentiments. 
#Subjectivity is also a float which lies in the range of [0,1]. Subjective sentences generally refer to personal opinion, emotion, or judgment. 
sentiment = []
for item in df['polarity']:  
    if item > 0.3:
        sentiment.append("Positive")
    elif item > -0.3:
        sentiment.append("Nuetral")
    else:
        sentiment.append("Negative")
    
df['sentiment'] = sentiment
#df

table.columns = ['desc','like','comment_list','Count','PostDate','Assets','Timeframe','Position','polarity','subjectivity','sentiment']
table.set_index('desc')
#table
table.to_csv('Idea01.csv', index=True)

import streamlit as st
import plost
import pandas as pd 
st.title('BTCUSD Price Prediction')
st.write("From Tradingview Idea Opinion Mining")
df = pd.read_csv('/workspace/webapp/Idea01.csv')

st.write (df)
st.line_chart(df['polarity'])

df.groupby(['PostDate', 'sentiment'])['subjectivity'].describe()[['count', 'mean']]
#df
