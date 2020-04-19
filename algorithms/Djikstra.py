from math import inf


from data.database import points

def findPath(start_name, end_name):
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
            if not connection.to_point.name in visited:
                time_between = connection.time
                if time[current_point.name] + time_between <= time[connection.to_point.name]:
                    time[connection.to_point.name] = time[current_point.name] + time_between
                    distance[connection.to_point.name] = distance[current_point.name] + connection.distance
                    prev[connection.to_point.name] = current_point.name

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
    return {'path': path, 'time': time[end_name], 'distance': distance[end_name]}


if __name__ == '__main__':
    # for testing
    findPath('Masjid Al-Husna', 'Pantai Hill Park')
