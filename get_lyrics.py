#!/usr/bin/env python3
# coding: utf-8
import argparse
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


def check_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("song")
    parser.add_argument("artist")
    args = parser.parse_args()
    return args.song, args.artist


def get_song_id_from_name(song_name, artist_name):
    search_url = BASE_URL + "/search"
    data = {'q': song_name + '+' + artist_name}
    response = requests.get(search_url, params=data, headers=HEADERS)
    json = response.json()
    artist = artist_name.upper()
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
    song_name, artist_name = check_args()
    song_id = get_song_id_from_name(song_name, artist_name)
    web_path = get_web_path_from_song_id(song_id)
    lyrics = get_lyrics_from_path(web_path)
    print(lyrics)


if __name__ == "__main__":
    main()
