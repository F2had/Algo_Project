# Use this to convert a point name to coordinates
####
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI')

search = 'KLCC'

print(gmaps.geocode(search))
print(gmaps.geocode(search)[0]['geometry']['location'])
