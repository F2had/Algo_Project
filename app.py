from flask import Flask, url_for, render_template, request, jsonify
from geopy import distance
from gmplot import gmplot
import polyline

app = Flask(__name__)
gm = gmplot


def compute_path(start, end):
    gmaps = googlemaps.Client(key='AIzaSyBqxu4tCWwSfaKcN7cQcReXzsZDY0HeG1k')
    now = datetime.now()
    directions_result = gmaps.directions(start, end, mode="transit", departure_time=now)
    x = []
    for i in directions_result:
        x.append(j['overview_polyline']['points'])
    test_data = polyline.decode(str(x))
    return test_data


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
