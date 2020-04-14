from .database_builder import get_latlon
from .graph import GraphPoint, connect_points, MODE_BUS, MODE_WALKING, MODE_TRAIN

points_names = [
    'UM CENTRAL',
    'Kuala Lumpur City Centre',
    'Mid Valley Megamall',
    'KL Sentral',

    'KL Gateway',
    'Lrt Station Universiti',
    'LRT Kerinchi',
    'Abdullah Hukum',
    'Pantai Panorama Condominium',
]

points = {}

# build the real points data collection
for point_n in points_names:
    latlon = get_latlon(point_n)
    points[point_n] = GraphPoint(point_n, latlon[0], latlon[1])

# Connections building
connect_points(points['UM CENTRAL'], points['KL Gateway'], MODE_BUS)
connect_points(points['UM CENTRAL'], points['KL Gateway'], MODE_WALKING)
connect_points(points['KL Gateway'], points['Lrt Station Universiti'], MODE_WALKING)
connect_points(points['KL Gateway'], points['Pantai Panorama Condominium'], MODE_WALKING)
connect_points(points['LRT Kerinchi'], points['Pantai Panorama Condominium'], MODE_WALKING)
connect_points(points['LRT Abdullah Hukum'], points['Mid Valley'], MODE_WALKING)

# LRT train
connect_points(points['Lrt Station Universiti'], points['LRT Kerinchi'], MODE_TRAIN)
connect_points(points['LRT Kerinchi'], points['LRT Abdullah Hukum'], MODE_TRAIN)
connect_points(points['LRT Abdullah Hukum'], points['KL Sentral'], MODE_TRAIN)
connect_points(points['KL Sentral'], points['KLCC'], MODE_TRAIN)
