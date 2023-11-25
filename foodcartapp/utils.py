from star_burger.settings import YANDEX_API_KEY

import requests
from geopy import distance as dstnc


def fetch_coordinates(address, apikey=YANDEX_API_KEY):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json()['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


def get_distance(from_where, to_where):
    try:
        fetched_from_where = fetch_coordinates(from_where)
        fetched_to_where = fetch_coordinates(to_where)
    except requests.exceptions:
        return 0
    distance = dstnc.distance(fetched_from_where, fetched_to_where).km
    return round(distance)
