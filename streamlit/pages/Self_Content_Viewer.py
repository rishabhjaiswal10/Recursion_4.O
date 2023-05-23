import pyphen
import requests
from PIL import Image
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
# from pyecharts.charts import Bar
# from pyecharts import options as opts
import base64
from pytube import YouTube
from pytube import Channel
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from googleapiclient.discovery import build
# # import plotly.graph_objects as go
# st.set_page_config(page_title="WEb Name", layout="wide")
# def load_lottiefile(filepath: str):
#     with open(filepath, "r") as f:
#         return json.load(f)
#
# api_key = 'AIzaSyBbpbkQwK4lcXjqw3vOZqSGRhdB0_Gf73k'
# def load_lottieurl(url: str):
#     r = requests.get(url)
#     if r.status_code != 200:
#         return None
#     return r.json()
# lottie_hello = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_A6VCTi95cd.json")
#
# channel_ids=[]
#
# lc,rc = st.columns(2)
# with st.container():
#     with rc:
#         st_lottie(
#             lottie_hello,
#             # speed=1,
#             # reverse=False,
#             # loop=True,
#             # quality="low", # medium ; high
#             # renderer="svg", # canvas
#             height=500,
#             #
#             width=600,
#             # key=None,
#         )
# with lc:
#     st.header("Title")
#     st.write("Description")
#     video = st.text_input("Enter the video url=")
#     x=YouTube(video)
#     Cid=x.channel_id
#     Curl=x.channel_url
#     c=Channel(Curl)
#     Cname=c.channel_name
#     channel_ids.append(Cid)
#
# youtube = build('youtube', 'v3', developerKey=api_key)
#
#
# def get_channel_stats(youtube, channel_ids):
#     all_data = []
#     request = youtube.channels().list(
#         part='snippet,contentDetails,statistics',
#         id=','.join(channel_ids))
#     response = request.execute()
#
#     for i in range(len(response['items'])):
#         data = dict(Channel_name=response['items'][i]['snippet']['title'],
#                     Subscribers=response['items'][i]['statistics']['subscriberCount'],
#                     Views=response['items'][i]['statistics']['viewCount'],
#                     Total_videos=response['items'][i]['statistics']['videoCount'],
#                     playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
#         all_data.append(data)
#
#     return all_data
#
# channel_statistics = get_channel_stats(youtube, channel_ids)
#
# channel_data = pd.DataFrame(channel_statistics)
#
# channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
# channel_data['Views'] = pd.to_numeric(channel_data['Views'])
# channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])
#
# def get_video_ids(youtube, playlist_id):
#     request = youtube.playlistItems().list(
#         part='contentDetails',
#         playlistId=playlist_id,
#         maxResults=50)
#     response = request.execute()
#
#     video_ids = []
#
#     for i in range(len(response['items'])):
#         video_ids.append(response['items'][i]['contentDetails']['videoId'])
#
#     next_page_token = response.get('nextPageToken')
#     more_pages = True
#
#     while more_pages:
#         if next_page_token is None:
#             more_pages = False
#         else:
#             request = youtube.playlistItems().list(
#                 part='contentDetails',
#                 playlistId=playlist_id,
#                 maxResults=50,
#                 pageToken=next_page_token)
#             response = request.execute()
#
#             for i in range(len(response['items'])):
#                 video_ids.append(response['items'][i]['contentDetails']['videoId'])
#
#             next_page_token = response.get('nextPageToken')
#
#     return video_ids
#
# playlist_id = channel_data.loc[channel_data['Channel_name']==Cname, 'playlist_id'].iloc[0]
# video_ids = get_video_ids(youtube, playlist_id)
#
#
# def get_video_details(youtube, video_ids):
#     all_video_stats = []
#
#     for i in range(0, len(video_ids), 50):
#         request = youtube.videos().list(
#             part='snippet,statistics',
#             id=','.join(video_ids[i:i + 50]))
#         response = request.execute()
#
#         for video in response['items']:
#             video_stats = dict(Title=video['snippet']['title'],
#                                Views=video['statistics']['viewCount'],
#                                # Comments=video['statistics']['commentCount'],
#                                Likes=video['statistics']['likeCount']
#                                )
#             all_video_stats.append(video_stats)
#
#     return all_video_stats
#
# video_details = get_video_details(youtube, video_ids)
#
# video_data = pd.DataFrame(video_details)
#
# #SEO
#
# import nltk
# nltk.download('punkt')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('vader_lexicon')
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize, sent_tokenize
# from nltk.stem import WordNetLemmatizer, PorterStemmer
#
#
# def get_seo_data(youtube, video_id):
#     request = youtube.videos().list(
#         part="snippet",
#         id=video_id
#     )
#     response = request.execute()
#     all_seo_data = []
#     for data in response['items']:
#         seodata = dict(Desc=data['snippet']['description'],
#                        Tags=data['snippet']['tags'],
#                        Titles=data['snippet']['title']
#                        )
#         all_seo_data.append(seodata)
#
#     return all_seo_data
#
# seo_details = get_seo_data(youtube, 'XWetgrNas-k')
#
#
#
# def syllable_count(word):
#     dic = pyphen.Pyphen(lang='en_US')
#     return len(dic.inserted(word).split("-"))
#
# print(syllable_count("computer"))
#
# description = seo_details[0]['Desc']
# # Tokenize the text into sentences
# sentences = sent_tokenize(description)
# # Tokenize the sentences into words
# words = word_tokenize(description)
# # Remove stop words
# stop_words = set(stopwords.words('english'))
# filtered_words = [word for word in words if word.casefold() not in stop_words]
# # Stemming
# stemmer = PorterStemmer()
# stemmed_words = [stemmer.stem(word) for word in filtered_words]
# # Lemmatization
# lemmatizer = WordNetLemmatizer()
# lemmatized_words = [lemmatizer.lemmatize(word) for word in filtered_words]
# # Extract top 5 most frequent words
# freq_dist = nltk.FreqDist(lemmatized_words)
# top_words = freq_dist.most_common(5)
# print("Top 5 most frequent words:", top_words)
#
# # Measure the readability of the text using the Flesch-Kincaid Grade Level formula
# num_sentences = len(sentences)
# num_words = len(words)
# num_syllables = sum([syllable_count(word) for word in words])
# seo_description_score = 0.39 * (num_words/num_sentences) + 11.8 * (num_syllables/num_words) - 15.59
#
# # import plotly.graph_objects as go
# sns.set(rc={'figure.figsize':(10,8)})
# f, ax = plt.subplots(figsize=(17, 5))
# ax = sns.barplot(x='Channel_name', y='Subscribers', data=seo_description_score)
# # fig = go.Figure(go.Indicator(
# #     mode = "gauge+number+delta",
# #     value = seo_description_score,
# #     domain = {'x': [0, 1], 'y': [0, 1]},
# #     title = {'text': " Description score"},
# #     delta = {'reference': 60},
# #     gauge = {'axis': {'range': [None, 100]},
# #              'steps' : [
# #                  {'range': [0, 50], 'color': "lightgray"},
# #                  {'range': [50, 100], 'color': "gray"}],
# #              'threshold' : {'line': {'color': "red", 'width': 4}, 'thickness': 1, 'value': 90}}))
#
# st.pyplot(ax)

image = Image.open('description.jpeg')
st.image(image)

image1 = Image.open('Tag.jpeg')
st.image(image1)

image2 = Image.open('Title.jpeg')
st.image(image2)