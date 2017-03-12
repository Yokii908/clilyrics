#!/usr/bin/env python3
# coding: utf-8
import json
import sys
import requests
from bs4 import BeautifulSoup


def get_config(config_file='config.json'):
    """Docstring for get_config.

    :config_file: configuration file
    :returns: token

    """
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
    a = data.get("token")
    return a


BASE_URL = "http://api.genius.com"
HEADERS = {'Authorization': get_config()}
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
    search_url = BASE_URL + "/search"
    data = {'q': SONG_TITLE + '+' + ARTIST_NAME}
    response = requests.get(search_url, params=data, headers=HEADERS)
    json = response.json()
    artist = ARTIST_NAME.upper()
    if response.status_code != 200:
        sys.exit("An error occured. (Is your token valid ?)")
    for res in json["response"]["hits"]:
        if res["result"]["primary_artist"]["name"].upper() == artist:
            return res["result"]["id"]
    return 0


def get_web_path_from_song_id(song_id):
    search_url = BASE_URL + "/songs/" + str(song_id)
    response = requests.get(search_url, headers=HEADERS)
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
