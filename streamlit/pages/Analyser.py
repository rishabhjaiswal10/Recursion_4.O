import requests
import streamlit as st
from streamlit_lottie import st_lottie
import pandas as pd
import base64
from pytube import YouTube
from pytube import Channel
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from googleapiclient.discovery import build

st.set_page_config(page_title="YTanalyser", layout="wide")
def load_lottiefile(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
lottie_hello = load_lottieurl("https://assets1.lottiefiles.com/packages/lf20_A6VCTi95cd.json")

channel_ids=[]

lc,rc = st.columns(2)
with st.container():
    with rc:
        st_lottie(
            lottie_hello,
            # speed=1,
            # reverse=False,
            # loop=True,
            # quality="low", # medium ; high
            # renderer="svg", # canvas
            height=500,
            #
            width=600,
            # key=None,
        )
with lc:
    st.header("Title")
    st.write("A tool which compares,analyses youtube data for the user")
    video = st.text_input("Enter channel 1 url=")
    video1 = st.text_input("Enter channel 2 url=")
    x=YouTube(video)
    Cid=x.channel_id
    Curl=x.channel_url
    c=Channel(Curl)
    Cname=c.channel_name
    channel_ids.append(Cid)

    x1=YouTube(video1)
    Cid1=x1.channel_id
    Curl1=x1.channel_url
    c1=Channel(Curl1)
    Cname1=c1.channel_name
    channel_ids.append(Cid1)
# print("Channel ID=",Cid)
api_key = 'AIzaSyBbpbkQwK4lcXjqw3vOZqSGRhdB0_Gf73k'
#channel_id = 'UCnz-ZXXER4jOvuED5trXfEA'
# channel_ids = ['UCnz-ZXXER4jOvuED5trXfEA', # techTFQ
#                'UCLLw7jmFsvfIVaUFsLs8mlQ', # Luke Barousse
#                'UCiT9RITQ9PW6BhXK0y2jaeg', # Ken Jee
#                'UC7cs8q-gJRlGwj4A8OmCmXg', # Alex the analyst
#                'UC2UXDak6o7rBm23k3Vv5dww' # Tina Huang
#               ]
# Cname
# Cname1
youtube = build('youtube', 'v3', developerKey=api_key)


def get_channel_stats(youtube, channel_ids):
    all_data = []
    request = youtube.channels().list(
        part='snippet,contentDetails,statistics',
        id=','.join(channel_ids))
    response = request.execute()

    for i in range(len(response['items'])):
        data = dict(Channel_name=response['items'][i]['snippet']['title'],
                    Subscribers=response['items'][i]['statistics']['subscriberCount'],
                    Views=response['items'][i]['statistics']['viewCount'],
                    Total_videos=response['items'][i]['statistics']['videoCount'],
                    playlist_id=response['items'][i]['contentDetails']['relatedPlaylists']['uploads'])
        all_data.append(data)

    return all_data

channel_statistics = get_channel_stats(youtube, channel_ids)

channel_data = pd.DataFrame(channel_statistics)

channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Total_videos'] = pd.to_numeric(channel_data['Total_videos'])

sns.set(rc={'figure.figsize':(10,8)})
f, ax = plt.subplots(figsize=(17, 5))
ax = sns.barplot(x='Channel_name', y='Subscribers', data=channel_data)

st.pyplot(f)
c, bx = plt.subplots(figsize=(17, 5))
bx = sns.barplot(x='Channel_name', y='Views', data=channel_data)
st.pyplot(c)

d, cx = plt.subplots(figsize=(17, 5))
cx = sns.barplot(x='Channel_name', y='Total_videos', data=channel_data)
st.pyplot(d)

playlist_id = channel_data.loc[channel_data['Channel_name']==Cname, 'playlist_id'].iloc[0]
# playlist_id


def get_video_ids(youtube, playlist_id):
    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids

video_ids = get_video_ids(youtube, playlist_id)


def get_video_details(youtube, video_ids):
    all_video_stats = []

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics',
            id=','.join(video_ids[i:i + 50]))
        response = request.execute()

        for video in response['items']:
            video_stats = dict(Title=video['snippet']['title'],
                               Views=video['statistics']['viewCount'],
                               # Comments=video['statistics']['commentCount'],
                               Likes=video['statistics']['likeCount']
                               )
            all_video_stats.append(video_stats)

    return all_video_stats

video_details = get_video_details(youtube, video_ids)

video_data = pd.DataFrame(video_details)

# video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
# video_data['Comments'] = pd.to_numeric(video_data['Comments'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
# video_data['Dislikes'] = pd.to_numeric(video_data['Dislikes'])
# video_data['Views'] = pd.to_numeric(video_data['Views'])

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)
d, ax1 = plt.subplots(figsize=(7, 5))
ax1 = sns.barplot(x='Views', y='Title', data=top10_videos)
st.pyplot(d)

# top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)
# d, ax1 = plt.subplots(figsize=(7, 5))
# ax1 = sns.barplot(x='Comments', y='Title', data=top10_videos)
# st.pyplot(d)

top10_videos = video_data.sort_values(by='Views', ascending=False).head(10)
d, ax1 = plt.subplots(figsize=(7, 5))
ax1 = sns.barplot(x='Likes', y='Title', data=top10_videos)
st.pyplot(d)
# playlist_id1
# def get_video_ids(youtube, playlist_id1):
#     request = youtube.playlistItems().list(
#         part='contentDetails',
#         playlistId=playlist_id1,
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

playlist_id1 = channel_data.loc[channel_data['Channel_name']==Cname1, 'playlist_id'].iloc[0]
video_ids = get_video_ids(youtube, playlist_id1)


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
#                                Published_date=video['snippet']['publishedAt'],
#                                Views=video['statistics']['viewCount'],
#                                # Likes=video['statistics']['likeCount'],
#                                # Comments=video['statistics']['commentCount']
#                                )
#             all_video_stats.append(video_stats)
#
#     return all_video_stats

video_details = get_video_details(youtube, video_ids)

video_data = pd.DataFrame(video_details)

# video_data['Published_date'] = pd.to_datetime(video_data['Published_date']).dt.date
video_data['Views'] = pd.to_numeric(video_data['Views'])
video_data['Likes'] = pd.to_numeric(video_data['Likes'])
# video_data['Comments'] = pd.to_numeric(video_data['Comments'])
# video_data['Dislikes'] = pd.to_numeric(video_data['Dislikes'])
# video_data['Views'] = pd.to_numeric(video_data['Views'])

top10_videos1 = video_data.sort_values(by='Views', ascending=False).head(10)
d, ax1 = plt.subplots(figsize=(7, 5))
ax1 = sns.barplot(x='Views', y='Title', data=top10_videos1)
st.pyplot(d)


top10_videos1 = video_data.sort_values(by='Views', ascending=False).head(10)
d, ax1 = plt.subplots(figsize=(7, 5))
ax1 = sns.barplot(x='Likes', y='Title', data=top10_videos1)
st.pyplot(d)


# top10_videos1 = video_data.sort_values(by='Views', ascending=False).head(10)
# c, ax2 = plt.subplots(figsize=(7, 5))
# ax2 = sns.barplot(x='Comments', y='Title', data=top10_videos1)
# st.pyplot(c)









# st.sidebar.header('User Input Features')
# selected_year = st.sidebar.selectbox('Year', list(reversed(range(1990,2020))))

# Web scraping of NFL player stats
# https://www.pro-football-reference.com/years/2019/rushing.htm
# @st.cache
# def load_data(year):
#     url = "https://www.pro-football-reference.com/years/" + str(year) + "/rushing.htm"
#     html = pd.read_html(url, header = 1)
#     df = html[0]
#     raw = df.drop(df[df.Age == 'Age'].index) # Deletes repeating headers in content
#     raw = raw.fillna(0)
#     playerstats = raw.drop(['Rk'], axis=1)
#     return playerstats
# playerstats = load_data(selected_year)

# Sidebar - Team selection
# sorted_unique_team = sorted(playerstats.Tm.unique())
# selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)

# Sidebar - Position selection
# unique_pos = ['RB','QB','WR','FB','TE']
# selected_pos = st.sidebar.multiselect('Position', unique_pos, unique_pos)

# Filtering data
# df_selected_team = playerstats[(playerstats.Tm.isin(selected_team)) & (playerstats.Pos.isin(selected_pos))]

# st.header('Display Player Stats of Selected Team(s)')
# st.write('Data Dimension: ' + str(df_selected_team.shape[0]) + ' rows and ' + str(df_selected_team.shape[1]) + ' columns.')
# st.dataframe(df_selected_team)

# Download NBA player stats data
# https://discuss.streamlit.io/t/how-to-download-file-in-streamlit/1806
# def filedownload(df):
#     csv = df.to_csv(index=False)
#     b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
#     href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
#     return href
#
# st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# # Heatmap
# if st.button('Intercorrelation Heatmap'):
#     st.header('Intercorrelation Matrix Heatmap')
#     df_selected_team.to_csv('output.csv',index=False)
#     df = pd.read_csv('output.csv')
#
#     corr = df.corr()
#     mask = np.zeros_like(corr)
#     mask[np.triu_indices_from(mask)] = True
#     with sns.axes_style("white"):
#         f, ax = plt.subplots(figsize=(7, 5))
#         ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
#     st.pyplot(f)
