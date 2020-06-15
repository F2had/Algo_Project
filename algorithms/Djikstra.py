from math import inf

from data.database import points


def find_all_paths(start_name, end_name, limit=None):
    assert start_name in points and end_name in points, "These points does not exist in our database"

    point_from = points[start_name]
    point_to = points[end_name]

    visited = []
    path = [(point_from, 0, 0)]
    paths = []

    def inner(point_from):
        # Mark the current node as visited
        visited.append(point_from.name)

        if point_from.name == point_to.name:
            paths.append(list(path))
        else:
            # If current vertex is not destination
            # Recur for all the vertices adjacent to this vertex
            for connection in point_from.connections:
                if connection.to_point.name not in visited:
                    path.append((connection.to_point, connection.time, connection.distance))
                    inner(connection.to_point)

        # back tracking
        path.pop()
        visited.remove(point_from.name)

    inner(point_from)

    # cleaning
    paths = [list(zip(*x)) for x in paths]
    paths = [{'path': [y.position() for y in x[0]], 'time': sum(x[1]), 'distance': sum(x[2])} for x in paths]

    # sort using time first
    paths.sort(key=lambda x: (x['time'], x['distance']))

    limit = len(paths) if None or type(limit) != int or limit > len(paths) else limit

    return paths[:limit]


def find_path(start_name, end_name):
    # make sure the arguments are in the database
    assert start_name in points and end_name in points, "These points does not exist in our database"

    # initialize the values
    visited = []
    prev = {point_n: None for point_n in points.keys()}

    time = {point_n: inf for point_n in points.keys()}
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

        for connection in current_point.connections:
            if connection.to_point.name not in visited:
                time_between = connection.time
                if time[current_point.name] + time_between <= time[connection.to_point.name]:
                    time[connection.to_point.name] = time[current_point.name] + time_between
                    distance[connection.to_point.name] = distance[current_point.name] + connection.distance
                    prev[connection.to_point.name] = current_point.name

    if prev[end_name] == -1:
        # TODO: replace with actual working error handling
        raise Exception(f'No path found from {start_name} to {end_name}')
    path = []
    points_on_way = []

    u = end_name
    path.append((points[u].lat, points[u].lon))
    points_on_way.append(u)


    while prev[u]:
        u = prev[u]
        path.insert(0, (points[u].lat, points[u].lon))
        points_on_way.insert(0, u)

    # for now distance is -1, because if it was left as infinity it will make an error in JS
    return {'path': path, 'directions': points_on_way, 'time': time[end_name], 'distance': distance[end_name]}


if __name__ == '__main__':
    # for testing
    print(find_path('Masjid Al-Husna', 'Pantai Hill Park'))
    print(find_all_paths('Masjid Al-Husna', 'Pantai Hill Park'))
