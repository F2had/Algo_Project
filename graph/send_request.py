import polyline
from jsonpath import jsonpath
import requests
import json
from lxml import etree

class get_points:

    def __init__(self):
        self.results=[]
        self.points_list = ['UM, Jalan Universiti, Kuala Lumpur, Federal Territory of Kuala Lumpur',
                       'Happy Mansion, Seksyen 17, Petaling Jaya, Selangor',
                       'KL Gateway Mall, Jalan Kerinchi, Pantai Dalam, Kuala Lumpur, Federal Territory of Kuala Lumpur']
        self.mode=['walking']

        self.base_url='https://maps.googleapis.com/maps/api/directions/json?'

        self.headers={
            'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        self.params={
            'key': 'AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI',
            'origin':self.points_list[0],
            'destination':self.points_list[0],
            'mode':self.mode[0]
        }


    def main(self):

        for x in self.points_list:
            self.params['origin']=x
            for y in self.points_list:
                if y not in x:
                    self.params['destination'] =y
                    response=self.send_request(self.base_url)
                    print(response.url)
                    self.parse_info(response)
        print(self.results)
        self.save_data()

    def send_request(self,url):
            response=requests.get(url,headers=self.headers,params=self.params)
            return response



    def parse_info(self,response):
        text=json.loads(response.content)
        info=jsonpath(text,'$..routes')[0]
        for i in info:
            result= {}
            result['from_point']=i['legs'][0]['start_address']
            result['start_lat'] = i['legs'][0]['start_location']['lat']
            result['start_lng'] = i['legs'][0]['start_location']['lng']
            result['to_point']=i['legs'][0]['end_address']
            result['end_lat'] = i['legs'][0]['end_location']['lat']
            result['end_lng'] = i['legs'][0]['end_location']['lng']
            result['path'] = polyline.decode(i['overview_polyline']['points'])
            result['distance'] = i['legs'][0]['distance']['value']
            result['time'] = i['legs'][0]['duration']['value']
            result['travel_mode']=i['legs'][0]['steps'][0]['travel_mode']
            result['bounds'] = i['bounds']

            self.results.append(result)

    def save_data(self):
        with open('result.json','w') as fp:
            json.dump(self.results,fp)


if __name__ == '__main__':
    points=get_points()
    points.main()
