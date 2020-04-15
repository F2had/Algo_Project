
# modes
MODE_TRAIN = 0
MODE_BUS = 1
MODE_WALKING = 2


class GraphPointConnection:
    def __init__(self, from_point, to_point, transit):
        self.from_point = from_point
        self.to_point = to_point
        self.transit = transit
        self.calculate_distance_time()

    def calculate_distance_time(self):
        # TODO: implement time and distance calculation routine
        self.distance = 1
        self.travel_time = 1
        pass


class GraphPoint:

    def __init__(self, name, lat, lon):
        self.name = name
        self.lat = lat
        self.lon = lon
        self.connections = []

    def connect(self, other, transit, is_one_way=False):
        # make sure that the mode is valid
        assert transit in [MODE_TRAIN, MODE_BUS, MODE_WALKING], "Please specify a valid mode of transit"

        self.connections.append((other, transit))

        if not is_one_way:
            other.connections.append((self, transit))

    def __str__(self):
        return f"GraphPoint('{self.name}', {self.lat}, {self.lon})"

    def __repr__(self):
        return f"GraphPoint('{self.name}', {self.lat}, {self.lon})"



def connect_points(from_point, to_point, transit, is_one_way=False):

    from_point.connect(to_point, transit, is_one_way)
    from_point
