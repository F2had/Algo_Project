from flask import Flask, url_for, render_template, request
from geopy import distance
from gmplot import gmplot



app = Flask(__name__)
gm = gmplot


website = "https://google.com/"

d = distance


@app.route("/index.html")
def test():
    return render_template("index.html", website=website)


def cal(f, t):

    return round(d.distance(t, f).km)


@app.route("/index.html", methods=['POST', 'GET'])
def destains():
    if request.method == "POST":
        start = request.form['f1']
        start1 = request.form['f2']
        dest = request.form['t1']
        dest1 = request.form['t2']

        f = (start, start1)
        t = (dest, dest1)
        result = cal(f, t)
        print(result)

        return render_template("index.html", result=result, km='km')


if __name__ == '__main__':
    app.run(debug=True)