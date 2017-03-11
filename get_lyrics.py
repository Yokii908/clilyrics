#!/usr/bin/env python3
# coding: utf-8
import sys
import requests
from bs4 import BeautifulSoup

base_url = "http://api.genius.com"
headers = {
        'Authorization': 'Bearer ggtZ3yMZlWxVXnwMZyRzDhtLLWpLX39bxMdrccRhrEfZLkRaCpcCdtxmGR1GnjN7'}

SONG_TITLE = 0
ARTIST_NAME = 0


def check_args():
    global SONG_TITLE
    global ARTIST_NAME
    if len(sys.argv) != 3:
        sys.exit(1)
    SONG_TITLE = sys.argv[1]
    ARTIST_NAME = sys.argv[2].upper()


def get_song_id_from_name():
    search_url = base_url + "/search"
    data = {'q': SONG_TITLE}
    response = requests.get(search_url, params=data, headers=headers)
    json = response.json()

    for res in json["response"]["hits"]:  # Caca
        if res["result"]["primary_artist"]["name"].upper() == ARTIST_NAME:
            return res["result"]["id"]
    return 0


def get_web_path_from_song_id(song_id):
    search_url = base_url + "/songs/" + str(song_id)
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        print("Combination Song/Artist not found")
        sys.exit(2)
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
    # Tres caca.
    print(
            get_lyrics_from_path(
                get_web_path_from_song_id(
                    get_song_id_from_name()
                    )
                )
            )


if __name__ == "__main__":
    main()
