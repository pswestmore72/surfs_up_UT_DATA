from flask import Flask, json, jsonify, render_template
import re
import os
import datetime as dt
from flask.scaffold import _matching_loader_thinks_module_is_package
import numpy as np
import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

app = Flask(__name__)

# SQLite
dir_path = os.path.dirname(__file__)
engine = create_engine(f"sqlite:///{dir_path}/hawaii.sqlite")
Base = automap_base()
Base.prepare(engine, reflect=True)
session = Session(engine)

# Classes for each SQL table in BASE
Measurement = Base.classes.measurement
Station = Base.classes.station

# 404 errors
def not_found(err):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
app.register_error_handler(404, not_found)

@app.route('/', methods=['GET'])
def index():
    routes = ['/api/v1.0/precipitation', '/api/v1.0/stations', '/api/v1.0/tobs', '/api/v1.0/temp/start/end']
    routes = [ re.findall(r'/api/v\d+\.\d/(.*)', route) for route in routes ]
    print("Server received request for 'Home' page")
    return render_template('home.html', data=routes)

@app.route("/api/v1.0/precipitation", methods=['GET'])
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

@app.route("/api/v1.0/stations", methods=['GET'])
def stations():
    stations_init = session.query(Station.station).all()
    stations = list(np.ravel(stations_init))
    return jsonify(stations=stations)

@app.route("/api/v1.0/tobs", methods=['GET'])
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results_monthly = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).\
        all()
    temps_monthly = list(np.ravel(results_monthly))
    return jsonify(temps=temps_monthly)

@app.route("/api/v1.0/temp/<start>/<end>", methods=['GET'])
def temp(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    if not end:
        results_temp = session.query(*sel).\
            filter(Measurement.date >= start).\
            all()
        temps = list(np.ravel(results_temp))
        return jsonify(temps)

    results_temp = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).\
        all()
    temps = list(np.ravel(results_temp))
    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True, port=3000)