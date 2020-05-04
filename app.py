from flask import Flask, render_template, request, send_file
import pandas as pd
from geopy.geocoders import Nominatim
import datetime
from geopy.extra.rate_limiter import RateLimiter


app= Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html", btn = 'submit')


@app.route('/success-table', methods=['POST'])
def success_table():
    global filename
    if request.method=="POST":
        file=request.files['file']
    try:
        df= pd.read_csv(file)
        geo = Nominatim(user_agent="the geolocator")
        geocode = RateLimiter(geo.geocode, min_delay_seconds=2)
        df["coordinates"]=df["Address"].apply(geocode)
        df['Latitude'] = df['coordinates'].apply(lambda loc: loc.latitude if loc else None)
        df['Longitude'] = df['coordinates'].apply(lambda loc: loc.longitude if loc else None)
        df=df.drop("coordinates",1)
        filename=datetime.datetime.now().strftime("uploads/%Y-%m-%d-%H-%M-%S-%f"+".csv")
        df.to_csv(filename,index=None)
        return render_template("index.html", text = df.to_html(), btn='download.html')
    except Exception as e:
        return render_template("index.html", text = str(e))


@app.route("/download-file/")
def download():
    return send_file(filename, attachment_filename='youraddress.csv', as_attachment=True)


if __name__=="__main__":
    app.run(debug=True)
