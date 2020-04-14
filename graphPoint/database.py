from jsonpath import jsonpath
import requests
import json


"this class aim to get point detail and connection detail such as latitude and longitude and distance information from website use google API"
class request_data:
    def __init__(self):
        self.connection_url='https://maps.googleapis.com/maps/api/directions/json?'
        self.point_url='https://maps.googleapis.com/maps/api/place/textsearch/json?'

        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        self.conection_params={
            'key': 'AIzaSyApye8aayb20yXZkHybB3XEvO1bvgfDy3w',
            'origin':None,
            'destination':None,
            'mode':None
        }

        self.point_params={
            'query':None,
            'key': 'AIzaSyApye8aayb20yXZkHybB3XEvO1bvgfDy3w',
        }

# send url request and return point or connection information
    # enter point name
    def connect_points_name(self,origin,destination,mode):
        self.conection_params['origin']=origin
        self.conection_params['destination']=destination
        self.conection_params['mode']=mode
        response = requests.get(self.connection_url, headers=self.headers, params=self.conection_params)

        connection=self.parse_connection(response,origin,destination)
        return connection

    # enter whole point
    def connect_points(self,from_point,to_point,mode):

        from_point = from_point.replace("\'", "\"")
        to_point=to_point.replace("\'", "\"")

        origin=json.loads(from_point)
        destination=json.loads(to_point)

        self.conection_params['origin'] = origin['name']
        self.conection_params['destination'] = destination['name']
        self.conection_params['mode'] = mode
        response = requests.get(self.connection_url, headers=self.headers, params=self.conection_params)

        connection = self.parse_connection(response, origin, destination)
        return connection



    def point(self,name):
        self.point_params['query']=name
        response = requests.get(self.point_url, headers=self.headers, params=self.point_params)
        point=self.parse_point(response,name)
        return point


# parse detail point or connection information from response
    def parse_connection(self,response,origin,destination):
        text=json.loads(response.content)
        info=jsonpath(text,'$..routes')[0]
        for i in info:
            connection= {
            "from_point":origin,
            "to_point":destination,
            "distance": i['legs'][0]['distance']['value'],
            "travel_mode":i['legs'][0]['steps'][0]['travel_mode']
            }
            return connection

    def parse_point(self,response,name):
        text = json.loads(response.content)
        info = jsonpath(text, '$..results')[0]
        for i in info:
            point={
                "name":name,
                "location":"(%s,%s)"%(i['geometry']['location']['lat'],i['geometry']['location']['lng'])
            }
            return str(point)


    def save_data(self,data):
        with open('data.json','w') as fp:
            json.dump(data,fp)



"this class save points_data and connections_data which are defined by user"
class database:

    d=request_data()
    point_database = {
        'UM CENTRAL': d.point('UM CENTRAL'),
        'Kuala Lumpur City Centre': d.point('Kuala Lumpur City Centre'),
        'Mid Valley Megamall': d.point('Mid Valley Megamall'),
        'KL Sentral': d.point('KL Sentral'),

        'KL Gateway': d.point('KL Gateway'),
        'Lrt Station Universiti': d.point('Lrt Station Universiti'),
        'LRT Kerinchi': d.point('LRT Kerinchi'),
        'Abdullah Hukum': d.point('Abdullah Hukum'),
        'Pantai Panorama Condominium': d.point('Pantai Panorama Condominium')
    }

    connections= {
        point_database['UM CENTRAL']:  {point_database['KL Gateway']: ('driving', 'walking')},
        point_database['KL Gateway']:  {point_database['Lrt Station Universiti']: 'walking', point_database['Pantai Panorama Condominium']: 'walking'},
        point_database['LRT Kerinchi']: {point_database['Pantai Panorama Condominium']: 'walking', point_database['Abdullah Hukum']: 'driving'},
        point_database['Abdullah Hukum']: {point_database['Mid Valley Megamall']: 'driving', point_database['KL Sentral']: 'driving'},
        point_database['Lrt Station Universiti']: {point_database['LRT Kerinchi']: 'driving'},
        point_database['KL Sentral']: {point_database['Kuala Lumpur City Centre']: 'driving'}
    }


    connection_database=[]

    # parse connection data which enter from_point ,to_point ,mode and save in a array finially
    # get from_point name
    for from_key in connections.keys():
        # pass the to_point name
        for to_key in connections[from_key].keys():
            # get the point_mode

            if type(connections[from_key][to_key]) == tuple:
                for i in range(len(connections[from_key][to_key])):
                    connection=d.connect_points(from_key, to_key, connections[from_key][to_key][i])
                    connection_database.append(connection)
            else:
                connection=d.connect_points(from_key, to_key, connections[from_key][to_key])
                connection_database.append(connection)



