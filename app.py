from flask import Flask, url_for, render_template, request
from geopy import distance
from gmplot import gmplot

app = Flask(__name__)
gm = gmplot

website = "https://google.com/"

d = distance


@app.route("/")
def load():
    return render_template("index.html", website=website)


@app.route("/", methods=['POST'])
def getPoints():
    start = request.form['start']
    end = request.form['end']

    return render_template("index.html", start=start, end=end)


if __name__ == '__main__':
    app.run(debug=True)
