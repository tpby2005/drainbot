import lyricsgenius
import random
import csv
import tweepy
from keys import keys

def get_song():
    with open('spotify.csv') as file:
        reader = csv.reader(file)
        random_row = random.choice(list(reader))
        artist = random_row[3]
        song = random_row[1]
    return song, artist

def get_lyrics(song, artist):
    client_access_token = keys['client_access_token']
    genius = lyricsgenius.Genius(client_access_token)
    lyrics = genius.search_song(song, artist).lyrics
    song = song.upper()
    return lyrics

def clean_lyrics(lyrics):
    lines = lyrics.split('\n')
    for i in range(len(lines)):
        if lines[i] == '' or '[' in lines[i]:
            lines[i] = 'XXX'
    lines = [i for i in lines if i != 'XXX']

    random_num = random.randrange(0, len(lines)-1)
    tweet = lines[random_num] + '\n' + lines[random_num + 1] + '\n' + lines[random_num + 2]
    tweet = tweet.replace("\\", "")
    return tweet

#just a main function essentially, used for aws lambda
def handler(event, context):
    auth = tweepy.OAuthHandler(
        keys['CONSUMER_API_KEY'],
        keys['CONSUMER_API_SECRET_KEY']
    )
    auth.set_access_token(
        keys['ACCESS_TOKEN'],
        keys['ACCESS_TOKEN_SECRET']
    )
    api = tweepy.API(auth)
    song, artist = get_song()
    lyrics = get_lyrics(song, artist)
    tweet = clean_lyrics(lyrics)
    new_line = '\n'
    clean_tweet = f'{tweet}{new_line}{new_line}{song} by {artist} #draingang'

    print(clean_tweet)
    status = api.update_status(clean_tweet)

    return clean_tweet