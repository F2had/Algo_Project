from flask import Flask, render_template, request, jsonify

from algorithms.Djikstra import find_path
from data import database
from data.graph import MODE_WALKING, MODE_BUS, MODE_TRAIN

app = Flask(__name__)


def get_bounds(test_path):
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
    result = find_path(start, end)

    result['bounds'] = get_bounds(result['path'])

    return result


@app.route("/graphdata", methods=['GET'])
def graphdata():
    paths = []
    visited = []
    flat_path = []

    modes_names = {MODE_WALKING: "walking", MODE_BUS: "bus", MODE_TRAIN: "train"}

    def add_connections(point):
        if point.name in visited:
            return
        visited.append(point.name)
        for connection in point.connections:
            paths.append([connection.from_point, connection.to_point, connection.transit])
            add_connections(connection.to_point)

    for point_n, point in database.points.items():
        add_connections(point)

    for i in range(len(paths)):
        path = paths[i]
        path[0] = (path[0].lat, path[0].lon)
        path[1] = (path[1].lat, path[1].lon)
        flat_path.append(path[0])
        flat_path.append(path[1])
        path[2] = modes_names[path[2]]
        paths[i] = path
    return jsonify({"paths": paths, "bounds": get_bounds(flat_path)})


@app.route("/", methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']

        try:
            if start and end:
                result = compute_path(start, end)
                return jsonify({'data': result})

            return jsonify({'error': 'Missing input!'})

        except AssertionError as e:
            return jsonify({'error': str(e)})
    else:
        return render_template("index.html", locations=database.points_names)


if __name__ == '__main__':
    app.run(debug=True)
