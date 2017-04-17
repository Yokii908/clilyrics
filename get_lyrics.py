#!/usr/bin/env python3
# coding: utf-8
'''
get_lyrics.py

CLI utility allowing you to get a song's lyrics
based on the Artist's name and the Song's name

Uses the Genius API
'''
import argparse
import json
import sys
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup


def get_config(config_file='config.json'):
    """Docstring for get_config.

    :config_file: configuration file
    :returns: token

    """
    with open(config_file) as json_data_file:
        data = json.load(json_data_file)
    return data.get("token")


BASE_URL = "http://api.genius.com"
HEADERS = {'Authorization': get_config()}


def check_args():
    '''Collects arguments (Song name, Artist name)'''
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--song",
        type=str,
        required=True)
    parser.add_argument(
        "-a",
        "--artist",
        type=str,
        required=True)
    args = parser.parse_args()
    return args.song, args.artist


def get_song_id_from_name(song_name, artist_name):
    '''Does a GET request to the API and returns the artist's ID'''
    search_url = BASE_URL + "/search"
    data = {'q': song_name + '+' + artist_name}
    try:
        response = requests.get(search_url, params=data, headers=HEADERS)
    except RequestException:
        sys.exit(1)
    resp = response.json()
    artist = artist_name.upper()
    if response.status_code != 200:
        sys.exit("An error occured. (Is your token valid ?)")
    for res in resp["response"]["hits"]:
        if res["result"]["primary_artist"]["name"].upper() == artist:
            return res["result"]["id"]


def get_web_path_from_song_id(song_id):
    '''GET request to get the path based on the song ID'''
    search_url = BASE_URL + "/songs/" + str(song_id)
    response = requests.get(search_url, headers=HEADERS)
    if response.status_code != 200:
        sys.exit("Combination Song/Artist not found")
    resp = response.json()
    try:
        return resp["response"]["song"]["path"]
    except KeyError:
        return


def get_lyrics_from_path(path):
    '''GET request to Genius API, then parses lyrics'''
    url = "http://genius.com" + path
    response = requests.get(url)
    bs_parsed = BeautifulSoup(response.text, "html.parser")
    lyrics = bs_parsed.find("lyrics").get_text()
    return lyrics


def main():
    '''Main Function'''
    song_name, artist_name = check_args()
    song_id = get_song_id_from_name(song_name, artist_name)
    web_path = get_web_path_from_song_id(song_id)
    lyrics = get_lyrics_from_path(web_path)
    print(lyrics)


if __name__ == "__main__":
    main()
