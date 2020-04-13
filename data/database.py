
from .graph import *

database = {
    'UM CENTRAL': GraphPoint('UM CENTRAL', 3.1210462, 101.6536228),
    'KLCC': GraphPoint('KLCC', 44.0509338, -123.0946959),
    'Mid Valley': GraphPoint('Mid Valley', 3.1183878, 101.6783698),
    'KL Sentral': GraphPoint('KL Sentral', 3.1343385, 101.6863371),

    'KL Gateway': GraphPoint('KL Gateway', 3.113827, 101.6630249),
    'Lrt Station Universiti': GraphPoint('Lrt Station Universiti', 3.1146872, 101.6616935),
    'LRT Kerinchi': GraphPoint('LRT Kerinchi', 3.115546, 101.668395),
    'LRT Abdullah Hukum': GraphPoint('LRT Abdullah Hukum', 3.119093, 101.672967),
    'Pantai Panorama Condominium': GraphPoint('Pantai Panorama Condominium', 3.1095448, 101.6627078),

}


#
connect_points(database['UM CENTRAL'], database['KL Gateway'], MODE_BUS)
connect_points(database['UM CENTRAL'], database['KL Gateway'], MODE_WALKING)
connect_points(database['KL Gateway'], database['Lrt Station Universiti'], MODE_WALKING)
connect_points(database['KL Gateway'], database['Pantai Panorama Condominium'], MODE_WALKING)
connect_points(database['LRT Kerinchi'], database['Pantai Panorama Condominium'], MODE_WALKING)
connect_points(database['LRT Abdullah Hukum'], database['Mid Valley'], MODE_WALKING)

# LRT train
connect_points(database['Lrt Station Universiti'], database['LRT Kerinchi'], MODE_TRAIN)
connect_points(database['LRT Kerinchi'], database['LRT Abdullah Hukum'], MODE_TRAIN)
connect_points(database['LRT Abdullah Hukum'], database['KL Sentral'], MODE_TRAIN)
connect_points(database['KL Sentral'], database['KLCC'], MODE_TRAIN)
