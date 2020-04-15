from .database_builder import get_latlon
from .graph import GraphPoint, connect_points, MODE_BUS, MODE_WALKING, MODE_TRAIN

points_names =[
    'Sunway Pyramid',
    'UM CENTRAL',
    'Mid Valley Megamall',
    'KL Sentral',
    'National Mosque of Malaysia',
    'Kuala Lumpur City Centre',
    #'Dataran Merdeka',
    #'Menara Kuala Lumpur',
    #'Kuala Lumpur International Airport',


    'Masjid Al-Husna',
    'Ppum Federal',
    'Lrt Station Universiti',
    'KL Gateway',
    'Pantai Panorama Condominium',
    'LRT Kerinchi',
    'LRT Abdullah Hukum',
    'Kuala Lumpur Station',

]

points = {}

# build the real points data collection
for point_n in points_names:
    latlon =list(get_latlon(point_n))
    points[point_n] = GraphPoint(point_n, latlon[0], latlon[1])


# Connections building


#walking
connect_points(points['Sunway Pyramid'],points['Masjid Al-Husna'],MODE_WALKING)
connect_points(points['Ppum Federal'],points['UM CENTRAL'],MODE_WALKING)

connect_points(points['UM CENTRAL'],points['Ppum Federal'],MODE_WALKING)
connect_points(points['Ppum Federal'],points['KL Gateway'],MODE_WALKING)

connect_points(points['KL Gateway'], points['Pantai Panorama Condominium'], MODE_WALKING)
connect_points(points['KL Gateway'], points['LRT Kerinchi'], MODE_WALKING)
connect_points(points['Pantai Panorama Condominium'], points['Lrt Station Universiti'], MODE_WALKING)
connect_points(points['Lrt Station Universiti'],points['LRT Kerinchi'],MODE_WALKING)
connect_points(points['LRT Abdullah Hukum'], points['Mid Valley Megamall'], MODE_WALKING)
connect_points(points['Kuala Lumpur Station'],points['National Mosque of Malaysia'],MODE_WALKING)
connect_points(points['National Mosque of Malaysia'],points['Kuala Lumpur City Centre'],MODE_WALKING)
connect_points(points['Kuala Lumpur Station'],points['Kuala Lumpur City Centre'],MODE_WALKING)

# bus
connect_points(points['Masjid Al-Husna'],points['Ppum Federal'],MODE_BUS)
connect_points(points['Ppum Federal'],points['Mid Valley Megamall'],MODE_BUS)
connect_points(points['Mid Valley Megamall'],points['KL Sentral'],MODE_BUS)

connect_points(points['UM CENTRAL'], points['KL Gateway'], MODE_BUS)
connect_points(points['KL Gateway'],points['Mid Valley Megamall'],MODE_BUS)
connect_points(points['Lrt Station Universiti'],points['LRT Kerinchi'],MODE_BUS)

# LRT train
connect_points(points['Lrt Station Universiti'], points['LRT Kerinchi'], MODE_TRAIN)
connect_points(points['LRT Kerinchi'], points['LRT Abdullah Hukum'], MODE_TRAIN)
connect_points(points['LRT Abdullah Hukum'], points['KL Sentral'], MODE_TRAIN)
connect_points(points['KL Sentral'],points['Kuala Lumpur Station'],MODE_TRAIN)
connect_points(points['KL Sentral'], points['Kuala Lumpur City Centre'], MODE_TRAIN)


