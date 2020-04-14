from datetime import datetime
import googlemaps
import polyline
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def getBounds(test_path):
    # test_path should be deleted later! GG
    test_path = [(3.10554, 101.66232), (3.10554, 101.66257), (3.10592, 101.66257), (3.10592, 101.66335),
                          (3.10591, 101.6654), (3.10591, 101.66608), (3.10631, 101.66609), (3.10694, 101.66609),
                          (3.10837, 101.66609), (3.10847, 101.66609), (3.10849, 101.66699), (3.10849, 101.66728),
                          (3.1085, 101.66769), (3.1085, 101.6681), (3.10867, 101.66811), (3.10892, 101.6681),
                          (3.10943, 101.66803), (3.10964, 101.66794), (3.1098, 101.66781), (3.10988, 101.66769),
                          (3.10994, 101.66757), (3.10998, 101.66746), (3.11, 101.66729), (3.11, 101.66678),
                          (3.10997, 101.66618), (3.11001, 101.66488), (3.11006, 101.66444), (3.11018, 101.66405),
                          (3.11029, 101.66384), (3.11043, 101.66362), (3.11094, 101.663), (3.11111, 101.66279),
                          (3.11127, 101.66263), (3.11158, 101.6624), (3.11169, 101.66234), (3.11201, 101.66223),
                          (3.11213, 101.66221), (3.11247, 101.66222), (3.11383, 101.66241), (3.11447, 101.66248),
                          (3.11491, 101.66249), (3.11557, 101.66245), (3.11592, 101.6624), (3.11615, 101.66241),
                          (3.11644, 101.66243), (3.11673, 101.6625), (3.117, 101.66263), (3.1172, 101.66277),
                          (3.11762, 101.6631), (3.11816, 101.66352), (3.11823, 101.66356), (3.11841, 101.66356),
                          (3.11858, 101.66353), (3.11865, 101.66354), (3.11868, 101.66357), (3.11869, 101.66346),
                          (3.11878, 101.66296), (3.11882, 101.6626), (3.11879, 101.66135), (3.11869, 101.6607),
                          (3.11865, 101.66058), (3.11834, 101.65987), (3.11823, 101.6596), (3.11819, 101.65932),
                          (3.11821, 101.65906), (3.11829, 101.65873), (3.11849, 101.65824), (3.11897, 101.65717),
                          (3.11903, 101.65696), (3.1192, 101.65492), (3.11923, 101.65479), (3.11926, 101.65472),
                          (3.11941, 101.65459), (3.1201, 101.65461)]

    bounds = {}
    north = -180
    west = 180
    east = -180
    south = 180

    for point in test_path:
        if point[0] > north:
            north = point[0]
        if point[0] < south:
            south = point[0]

        if point[1] > east:
            east = point[1]
        if point[1] < west:
            west = point[1]

    bounds = {'northeast': {'lat': north, 'lng': east}, 'southwest': {'lat': south, 'lng': west}}
    return bounds


def compute_path(start, end):
    gmaps = googlemaps.Client(key='AIzaSyBY-vvkInUrKKkdiCOZh36MggdgJRh1BbI')
    now = datetime.now()
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=now, region='MY')

    if len(directions_result) == 0:
        return {"error": "Could not find path"}

    distancetime_result = gmaps.distance_matrix(start, end, mode="transit", departure_time=now, region='MY')

    result = {}

    path = directions_result[0]['overview_polyline']['points']
    result['path'] = polyline.decode(path)

    result['bounds'] = directions_result[0]['bounds']

    row = distancetime_result['rows'][0]['elements'][0]
    distance = row['distance']['text']
    time = row['duration']['text']

    result['distance'] = distance
    result['time'] = time

    return result


@app.route("/", methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']

        if start and end:
            result = compute_path(start, end)
            return jsonify({'data': result})

        return jsonify({'error': 'Missing input!'})
    else:
        return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
