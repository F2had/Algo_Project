# Use this to convert a point name to coordinates
####
import googlemaps

gmaps = googlemaps.Client(key='AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI')

search = "KL Sentral "

print(gmaps.geocode(search))
print(gmaps.geocode(search)[0]['geometry']['location'])
