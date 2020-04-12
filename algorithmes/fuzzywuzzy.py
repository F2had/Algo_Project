from fuzzywuzzy import process



# FIXME
# change with the actual list of locations
test_data = ['panorama', 'um', 'pantai hill park', 'pantai panorama', 'KK12', 'UM Cerntral']
# take the user input for the query
user_query = 'Pantai hi'


def fuzzy(query, locations):
    return process.extractOne(query, locations)[0]
