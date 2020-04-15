from .database_builder import get_latlon
from .graph import GraphPoint, connect_points, MODE_BUS, MODE_WALKING, MODE_TRAIN
from os import path

points_names = [
    'Sunway Pyramid',
    'UM CENTRAL',
    'Mid Valley Megamall',
    'KL Sentral',
    'National Mosque of Malaysia',
    'Kuala Lumpur City Centre',
    'Menara Kuala Lumpur',
    'Kuala Lumpur International Airport',

    'Masjid Al-Husna',
    'LRT Asia Jaya',
    'Ppum Federal',
    'KL 1102 Masjid Ar-Rahman UM',
    'Lrt Station Universiti',
    'LRT Kerinchi',
    'Pantai Hill Park',
    'LRT Abdullah Hukum',
    'Kuala Lumpur Station',

]

points = {}

# load cache
if path.isfile('cache_points'):
    with open('cache_points', 'r') as cache_file:
        for line in cache_file:
            point = eval(line)
            if point.name in points_names:
                points[point.name] = point

# build the real points data collection
# only build points that are not present in the cache
with open('cache_points', 'w') as cache_file:
    for point_n in points_names:
        if not point_n in points:
            latlon = list(get_latlon(point_n))
            points[point_n] = GraphPoint(point_n, latlon[0], latlon[1])
            print(f'geocode: {point_n}')
        print(points[point_n], file=cache_file)

# Connections building

# walking

connect_points(points['Sunway Pyramid'], points['Masjid Al-Husna'], MODE_WALKING)
connect_points(points['KL 1102 Masjid Ar-Rahman UM'], points['UM CENTRAL'], MODE_WALKING)

connect_points(points['KL 1102 Masjid Ar-Rahman UM'], points['Lrt Station Universiti'], MODE_WALKING)
connect_points(points['Lrt Station Universiti'], points['LRT Kerinchi'], MODE_WALKING)
connect_points(points['LRT Abdullah Hukum'], points['Mid Valley Megamall'], MODE_WALKING)
connect_points(points['Kuala Lumpur Station'], points['National Mosque of Malaysia'], MODE_WALKING)
connect_points(points['National Mosque of Malaysia'], points['Kuala Lumpur City Centre'], MODE_WALKING)

# bus
connect_points(points['Masjid Al-Husna'], points['LRT Asia Jaya'], MODE_BUS)
connect_points(points['LRT Asia Jaya'], points['Ppum Federal'], MODE_BUS)
connect_points(points['Ppum Federal'], points['KL 1102 Masjid Ar-Rahman UM'], MODE_BUS)

connect_points(points['UM CENTRAL'], points['Lrt Station Universiti'], MODE_BUS)
connect_points(points['Lrt Station Universiti'], points['Mid Valley Megamall'], MODE_BUS)
connect_points(points['UM CENTRAL'], points['Pantai Hill Park'], MODE_BUS)
connect_points(points['Pantai Hill Park'], points['LRT Abdullah Hukum'], MODE_BUS)

connect_points(points['Ppum Federal'], points['Mid Valley Megamall'], MODE_BUS)
connect_points(points['Mid Valley Megamall'], points['KL Sentral'], MODE_BUS)
connect_points(points['KL Sentral'], points['Kuala Lumpur Station'], MODE_BUS)
connect_points(points['Kuala Lumpur City Centre'], points['Menara Kuala Lumpur'], MODE_BUS)

# LRT train
connect_points(points['LRT Asia Jaya'], points['Lrt Station Universiti'], MODE_TRAIN)
connect_points(points['Lrt Station Universiti'], points['LRT Kerinchi'], MODE_TRAIN)
connect_points(points['LRT Kerinchi'], points['LRT Abdullah Hukum'], MODE_TRAIN)
connect_points(points['LRT Abdullah Hukum'], points['KL Sentral'], MODE_TRAIN)
connect_points(points['KL Sentral'], points['Kuala Lumpur City Centre'], MODE_TRAIN)
connect_points(points['KL Sentral'], points['Kuala Lumpur International Airport'], MODE_TRAIN)
