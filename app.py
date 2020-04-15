from datetime import datetime
import googlemaps
import polyline
from flask import Flask, render_template, request, jsonify

from data import database

app = Flask(__name__)


def getBounds(test_path):
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
    gmaps = googlemaps.Client(key='AIzaSyApye8aayb20yXZkHybB3XEvO1bvgfDy3w')
    now = datetime.now()
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=now, region='MY')

    if len(directions_result) == 0:
        return {"error": "Could not find path"}

    distancetime_result = gmaps.distance_matrix(start, end, mode="transit", departure_time=now, region='MY')

    result = {}

    path = directions_result[0]['overview_polyline']['points']
    result['path'] = polyline.decode(path)

    result['bounds'] = getBounds(result['path'])

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
        return render_template("index.html", locations=database.points_names)


if __name__ == '__main__':
    app.run(debug=True)
