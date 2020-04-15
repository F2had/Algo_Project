# This file has helping functions for building the database

import googlemaps

__gmaps = googlemaps.Client(key='AIzaSyApye8aayb20yXZkHybB3XEvO1bvgfDy3w')



def get_latlon(point):
    result = __gmaps.geocode(point)
    if not result:
        # result not found
        return None

    return result[0]['geometry']['location'].values()
