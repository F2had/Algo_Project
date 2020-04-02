from flask import Flask, url_for, render_template, request, jsonify
from geopy import distance
from gmplot import gmplot

app = Flask(__name__)
gm = gmplot

d = distance


@app.route("/", methods=['POST', 'GET'])
def root():
    if request.method == 'POST':
        start = request.form['start']
        end = request.form['end']

        if start and end:
            return jsonify({'start': start})

        return jsonify({'error': 'Missing input!'})
    else:
        return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
