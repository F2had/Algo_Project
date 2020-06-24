# This file has helping functions for building the database

import googlemaps
import geopy

MODE_TRAIN = 0
MODE_BUS = 1
MODE_WALKING = 2

__gmaps = googlemaps.Client(key='AIzaSyApye8aayb20yXZkHybB3XEvO1bvgfDy3w')
nominatim = geopy.Nominatim(user_agent="my-application")


def get_latlon(point):
    # result_ = __gmaps.geocode(point, region='MY')

    print(point)
    result = nominatim.geocode(point, country_codes=['MY'])

    if not result:
        # result not found
        return None

    print('geocode api used')

    return (result.latitude, result.longitude)


def get_time_distance(from_p, to_p, method):
    mode = ""
    if method in [MODE_TRAIN, MODE_BUS]:
        mode = "transit"
    elif method == MODE_WALKING:
        mode = "walking"
    else:
        mode = "driving"
    # FIXME: method 2 is walking, we can't import MODE_WALKING, because it would result in circular import
    result = __gmaps.distance_matrix(from_p, to_p, mode=mode, region='MY')

    element = result['rows'][0]['elements'][0]
    time = element['duration']['value']
    distance = element['distance']['value']

    print('distance_matrix api used')

    return time, distance
