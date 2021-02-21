import json
from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim
import folium
from pprint import pprint


def twitter_api(tweet_tag: str) -> dict:
    """
    Get json from twitter.
    """
    base_url = "https://api.twitter.com/"

    bearer_token = "AAAAAAAAAAAAAAAAAAAAAIKvMwEAAAAAGfXtAizYuenmkYuQLZ4qCDL%2F3n8%3D0Bqy4HA6TVWqzcYq7Nk9UK0slRiRyVZvlEBtpyowkdXOupLBNf"

    search_url = '{}1.1/friends/list.json'.format(base_url)

    search_headers = {
        'Authorization': 'Bearer {}'.format(bearer_token)
    }

    search_params = {
        'screen_name': f'@{tweet_tag}',
        'count': 15
    }

    response = requests.get(
        search_url, headers=search_headers, params=search_params)
    return response.json()['users']


def get_coordinates(friends: dict) -> list:
    """
    Get coordinates and usernames from json.
    """
    geolocator = Nominatim(user_agent="twitter_users")
    data_list = []
    for friend in friends:
        if friend['location'] != '':
            try:
                location = geolocator.geocode(friend['location'])
                coords = (location.latitude, location.longitude)
                friend_tuple = [coords, friend['screen_name']]
                data_list.append(friend_tuple)

            except (AttributeError, OSError):
                continue

    return data_list


def generate_map(data: list):
    """
    Generate HTML map with location markers.
    """

    mp = folium.Map(location=(data[0][0]), zoom_start=10)

    for info in data:
        mp.add_child(folium.Marker(
            location=[info[0][0], info[0][1]],
            popup=info[1],
            icon=folium.Icon(color='green',
                             icon_color='white',
                             icon='cloud')))

    mp.save('twitter.html')

# app = Flask(__name__)


if __name__ == "__main__":
    pprint(generate_map(get_coordinates(twitter_api("BarackObama"))))
    # app.run()
