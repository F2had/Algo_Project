from math import inf

# TODO: use cache for distance and time as well
import googlemaps

from data.database import points, MODE_WALKING

__client = googlemaps.Client(key='AIzaSyApye8aayb20yXZkHybB3XEvO1bvgfDy3w')


def getTime(from_p, to_p, method):
    result = __client.distance_matrix(from_p, to_p, mode='walking' if method == MODE_WALKING else 'transit',
                                      region='MY')

    time = result['rows'][0]['elements'][0]['duration']['value']
    return time


def findPath(start_name, end_name):
    # make sure the arguments are in the database
    assert start_name in points and end_name in points, "These points does not exist in our database"

    # initialize the values
    visited = []
    prev = {point_n: None for point_n in points.keys()}

    time = {point_n: inf for point_n in points.keys()}
    # TODO: use the distance or display it.
    distance = {point_n: inf for point_n in points.keys()}

    # the first point does not have previous and distance and time to itself is 0
    time[start_name] = distance[start_name] = 0
    prev[start_name] = None

    # go through all points in the database
    for _ in range(len(points)):
        # get the one with the lowest time and not yet visited
        min_time_n = min(filter(lambda x: not x[0] in visited, time.items()), key=lambda x: x[1])[0]
        current_point = points[min_time_n]

        visited.append(current_point.name)

        # TODO: use connections object instead of tuple
        for connection in current_point.connections:
            if not connection[0].name in visited:
                time_between = getTime((current_point.lat, current_point.lon),
                                       (connection[0].lat, connection[0].lon), connection[1])
                if time[current_point.name] + time_between <= time[connection[0].name]:
                    time[connection[0].name] = time[current_point.name] + time_between
                    prev[connection[0].name] = current_point.name

    if prev[end_name] == -1:
        # TODO: replace with actual working error handling
        raise Exception(f'No path found from {start_name} to {end_name}')
    path = []

    u = end_name
    path.append((points[u].lat, points[u].lon))

    while prev[u]:
        u = prev[u]
        path.insert(0, (points[u].lat, points[u].lon))

    # for now distance is -1, because if it was left as infinity it will make an error in JS
    return {'path': path, 'time': time[end_name], 'distance': -1}


if __name__ == '__main__':
    findPath('Masjid Al-Husna', 'Pantai Hill Park')
