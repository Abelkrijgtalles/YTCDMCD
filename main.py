import os

from MorseCodePy import decode
from dotenv import load_dotenv
from googleapiclient.discovery import build

# init
load_dotenv()

print()
print("YT Countdown Morse Code Decipher")
print("https://github.com/Abelkrijgtalles/YTCDMCD")
print()
print("Made by Abelkrijgtalles")
print()

try:
    youtube = build("youtube", "v3", developerKey=os.getenv("KEY"))
except:
    print("Something went wrong with authenticating. Is your Youtube Data API v3 key in your .env-file as KEY=[key]?")
    print("Exiting.")
    exit()

request = youtube.search().list(
    part="snippet",
    channelId="UC7nm9Nzo12SDQzrxJS8xdVg",
    maxResults=50,
    order="date",
    publishedAfter="2024-04-17T18:30:15Z"
)
print("Requesting first 50 videos of countdown 2. ", end="")
response = request.execute()
print("[Done]")

items = response["items"]

# this system only works with the 100 videos

if int(response["items"][0]["snippet"]["title"]) < 50:
    extra_videos = 50 - int(response["items"][0]["snippet"]["title"])
    print("Requesting " + extra_videos + " more videos of countdown 2. ", end="")
    request = youtube.search().list(
        part="snippet",
        channelId="UC7nm9Nzo12SDQzrxJS8xdVg",
        maxResults=extra_videos,
        order="date",
        pageToken=response["nextPageToken"],
        publishedAfter="2024-04-17T18:30:15Z"
    )
    print("[Done]")
    items = items + response["items"]

print("Countdown 2 is currently at day " + items[0]["snippet"]["title"] + ".")

print("Converting all descriptions to IDs ", end="")
# ids is a list of IDs in order from 100 to the latest video.
ids = []
items.reverse()
for video in items:
    description = video["snippet"]["description"].replace(".", "")
    video_id = ""
    for i in description.split(" "):
        video_id = video_id + chr(int(i))
    ids.append(video_id)
print("[Done]")

print("Here are all the links: ")
for video_id in ids:
    print("https://youtu.be/" + video_id)

while True:
    answer = input("The following part of the script will use your YouTube API key alot. It will make a call for "
                   "every morse code video link. Do you want to continue? (y/n)")
    if answer == "y":
        break
    elif answer == "n":
        print("Exiting.")
        exit()

morse_code = ""

print("Getting morse code string. ", end="")
for video_id in ids:
    request = youtube.videos().list(
        part="snippet",
        id=video_id
    )

    response = request.execute()
    morse_code = morse_code + response["items"][0]["snippet"]["title"] + " "
print("[Done]")

print("Morse code: " + morse_code)
print("Current morse code message: " + decode(morse_code, language="english"))
