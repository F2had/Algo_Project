from datetime import datetime

import googlemaps
import polyline
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


def compute_path(start, end):
    gmaps = googlemaps.Client(key='AIzaSyBqxu4tCWwSfaKcN7cQcReXzsZDY0HeG1k')
    now = datetime.now()
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=now)

    if len(directions_result) == 0:
        return {"error": "Could not find path"}

    distancetime_result = gmaps.distance_matrix(start, end, mode="transit", departure_time=now)

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
