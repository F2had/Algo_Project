from os import path

from data.database_builder import get_time_distance

# FIXME: change to string might be better
MODE_TRAIN = 0
MODE_BUS = 1
MODE_WALKING = 2


class ConnectionCacheHolder:
    def __init__(self, filename):
        self.connections = {}
        self.filename = filename
        if path.isfile(filename):
            with open(filename, 'r') as cache_file:
                for line in cache_file:
                    connection = eval(line)
                    from_p, to_p, transit, time, distance = connection
                    if from_p not in self.connections:
                        self.connections[from_p] = []
                    self.connections[from_p].append([to_p, transit, time, distance])

    def get_time_distance(self, from_p, to_p, transit):
        if from_p not in self.connections:
            return None
        from_p_connections = self.connections[from_p]
        result = list(filter(lambda x: x[0] == to_p and x[1] == transit, from_p_connections))

        if result:
            assert len(result) == 1
            return result[0][-2:]
        else:
            return None

    def add_connection(self, from_p, to_p, transit, time, distance):
        if not self.get_time_distance(from_p, to_p, transit):
            if from_p not in self.connections:
                self.connections[from_p] = []
            self.connections[from_p].append([to_p, transit, time, distance])
            self.save_cache()

    def save_cache(self):
        with open(self.filename, 'w') as cache_file:
            for from_p_connections in self.connections.items():
                from_p, connections_details = from_p_connections
                for connection in connections_details:
                    print(f"{[from_p] + connection}", file=cache_file)


class GraphPointConnection:
    def __init__(self, from_point, to_point, transit, time=None, distance=None):
        self.from_point = from_point
        self.to_point = to_point
        self.transit = transit

        if time and distance:
            self.time = time
            self.distance = distance
        else:
            print(self.from_point.name, "....", self.to_point.name)
            self.time, self.distance = get_time_distance(self.from_point.position(), self.to_point.position(),
                                                         self.transit)
            print(f'time_distance: {from_point.name} => {to_point.name}')


class GraphPoint:
    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.connections = []

    def connect(self, other, transit, is_one_way=False, cache=None):
        # make sure that the mode is valid
        assert transit in [MODE_TRAIN, MODE_BUS, MODE_WALKING], "Please specify a valid mode of transit"

        connection = cache.get_time_distance(self.name, other.name, transit)

        if connection:
            connection = GraphPointConnection(self, other, transit, connection[0], connection[1])
        else:
            connection = GraphPointConnection(self, other, transit)
            cache.add_connection(self.name, other.name, transit, connection.time, connection.distance)

        self.connections.append(connection)

        if not is_one_way:
            other.connect(self, transit, is_one_way=True, cache=cache)

    def position(self):
        return self.lat, self.lon

    def __str__(self):
        return f"GraphPoint('{self.name}', {self.lat}, {self.lon})"

    def __repr__(self):
        return f"GraphPoint('{self.name}', {self.lat}, {self.lon})"


def connect_points(from_point, to_point, transit, cache, is_one_way=False):
    from_point.connect(to_point, transit, is_one_way, cache)
