import polyline
from jsonpath import jsonpath
import requests
import json
from lxml import etree

class data:

    def __init__(self):

        self.connection_url='https://maps.googleapis.com/maps/api/directions/json?'
        self.point_url='https://maps.googleapis.com/maps/api/place/textsearch/json?'

        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        self.conection_params={
            'key': 'AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI',
            'origin':None,
            'destination':None,
            'mode':None
        }

        self.point_params={
            'query':None,
            'key': 'AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI',
        }

# send url request and return point or connection information
    def connection_points(self,origin,destination,mode):
        self.conection_params['origin']=origin
        self.conection_params['destination']=destination
        self.conection_params['mode']=mode
        response = requests.get(self.connection_url, headers=self.headers, params=self.conection_params)
        connection=self.parse_connection(response,origin,destination)
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
            #connection['from_point']=i['legs'][0]['start_address']
            #connection['to_point']=i['legs'][0]['end_address']
            'from_point':origin,
            'to_point':destination,
            'distance': i['legs'][0]['distance']['value'],
            'travel_mode':i['legs'][0]['steps'][0]['travel_mode']
            }
            return connection

    def parse_point(self,response,name):
        text = json.loads(response.content)
        info = jsonpath(text, '$..results')[0]
        for i in info:
            point={
                'name':name,
                'location':tuple((i['geometry']['location']['lat'],i['geometry']['location']['lng']))
            }
            return point


    def save_data(self,data):
        with open('data.json','w') as fp:
            json.dump(data,fp)



if __name__ == '__main__':
    g=data()
    r=g.point('university of malaya')
    c=g.connection_points('university of malaya','kl gateway','walking')
    print(r)
    print(c)