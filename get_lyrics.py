#!/usr/bin/env python3
# coding: utf-8
import json
import sys
import requests
from bs4 import BeautifulSoup

with open('config.json') as json_data_file:
    data = json.load(json_data_file)
a = data["token"]

base_url = "http://api.genius.com"
headers = {'Authorization': a}

SONG_TITLE = 0
ARTIST_NAME = 0


def check_args():
    global SONG_TITLE
    global ARTIST_NAME
    if len(sys.argv) != 3:
        print("Error: Missing arguments",
                file=sys.stderr)
        print(sys.argv[0], "song artist",
                file=sys.stderr)
        sys.exit(1)
    SONG_TITLE = sys.argv[1]
    ARTIST_NAME = sys.argv[2]


def get_song_id_from_name():
    search_url = base_url + "/search"
    data = {'q': SONG_TITLE + '+' + ARTIST_NAME}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()
    artist = ARTIST_NAME.upper()
    if response.status_code != 200:
        sys.exit("An error occured. (Is your token valid ?)")
    for res in json["response"]["hits"]:
        if res["result"]["primary_artist"]["name"].upper() == artist:
            return res["result"]["id"]
    return 0


def get_web_path_from_song_id(song_id):
    search_url = base_url + "/songs/" + str(song_id)
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        sys.exit("Combination Song/Artist not found")
    json = response.json()
    return json["response"]["song"]["path"]


def get_lyrics_from_path(path):
    url = "http://genius.com" + path
    response = requests.get(url)
    bs = BeautifulSoup(response.text, "html.parser")
    [h.extract() for h in bs('script')]
    lyrics = bs.find("lyrics").get_text()
    return lyrics


def main():
    check_args()
    song_id = get_song_id_from_name()
    web_path = get_web_path_from_song_id(song_id)
    lyrics = get_lyrics_from_path(web_path)
    print(lyrics)


if __name__ == "__main__":
    main()
