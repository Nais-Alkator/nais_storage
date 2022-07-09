from geopy.distance import distance
from django.conf import settings
from nais_storage.models import BoxOrder, SeasonOrder
import requests


YANDEX_GEOCODER_API_TOKEN = settings.YANDEX_GEOCODER_API_TOKEN


def get_storages_context(storages, profile):
    client_address = profile.address
    client_coordinates = fetch_coordinates(YANDEX_GEOCODER_API_TOKEN, client_address)
    storages_context = []
    for storage in storages:
        distance_to_client = distance(client_coordinates, (storage.longitude, storage.latitude))
        distance_to_client = round(distance_to_client.km)
        storage_context = {"name": storage.name, "address": storage.address, "distance_to_client": distance_to_client}
        storages_context.append(storage_context)
    return storages_context


def get_box_orders(profile):
    orders_raw = BoxOrder.objects.filter(client=profile).prefetch_related("storage").prefetch_related("box")
    box_orders_raw = (order for order in orders_raw)
    box_orders = []
    for box_order in box_orders_raw:
        order = {"box_size": box_order.box.size,
                 "storage": box_order.storage,
                 "date_from": box_order.date_from,
                 "date_to": box_order.date_to,
                 "price": box_order.box.price,
                 }
        box_orders.append(order)
    return box_orders

def get_season_orders(profile):
    orders_raw = SeasonOrder.objects.filter(client=profile).prefetch_related("item").prefetch_related("storage")
    season_orders_raw = (order for order in orders_raw)
    season_orders = []
    for season_order in season_orders_raw:
        order = {
            "item": season_order.item.name,
            "item_category": season_order.item.category,
            "storage": season_order.storage,
            "date_from": season_order.date_from,
            "date_to": season_order.date_to,
            "quantity": season_order.quantity,
            "price": season_order.price
        }
        season_orders.append(order)
    return season_orders


def fetch_coordinates(apikey, address):
    base_url = "https://geocode-maps.yandex.ru/1.x"
    response = requests.get(base_url, params={
        "geocode": address,
        "apikey": apikey,
        "format": "json",
    })
    response.raise_for_status()
    found_places = response.json(
    )['response']['GeoObjectCollection']['featureMember']

    if not found_places:
        return None

    most_relevant = found_places[0]
    lon, lat = most_relevant['GeoObject']['Point']['pos'].split(" ")
    return lon, lat


