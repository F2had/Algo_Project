# This file has helping functions for building the database

import googlemaps

__gmaps = googlemaps.Client(key='AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI')


def get_latlon(point):
    result = __gmaps.geocode(point)
    if not result:
        # result not found
        return None

    return result[0]['geometry']['location'].values()
