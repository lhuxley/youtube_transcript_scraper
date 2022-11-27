import sys
import os
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi


def remove(string):
    string = string.replace("?", "")
    string = string.replace("|", "")
    return string.replace(" ", "")

youtube = build('youtube', 'v3', developerKey='Enter Dev Key Here')

channel = youtube.channels().list(part = 'contentDetails', id='Enter Channel Id Here').execute()

playlist_ID = channel['items'][0]['contentDetails']['relatedPlaylists']['uploads']


videos = []
next = None


while 1:
    res = youtube.playlistItems().list(playlistId=playlist_ID, part='snippet', pageToken = next, maxResults=50).execute()
    videos += res['items']
    next = res.get('nextPageToken')

    if next is None:
        break

path = os.path.join(os.getcwd(), "video_transcripts_" + remove(videos[0]['snippet']['channelTitle']))

if not os.path.exists(path):
    os.mkdir(path, 777)

os.chdir(path)

for video in videos:

    file = open(remove(video['snippet']['title']) + ".txt", 'w', encoding='utf-8')
    file.write("URL: https://www.youtube.com/watch?v=" + video['snippet']['resourceId']['videoId'] + "\n\n")
    
    try:
        print(video['snippet']['title'])
        dictlist = YouTubeTranscriptApi.get_transcript(video['snippet']['resourceId']['videoId'], languages=['en'])
        if dictlist:
            for dict in dictlist:
                file.write(str(dict["start"]) + " " + dict["text"] + "\n")
    except:
        print('FAILED: ' + video['snippet']['title'] + '. This most often occurs because transcripts are disabled by the channel owner, or the video does not have transcripts.') 

    file.close()



