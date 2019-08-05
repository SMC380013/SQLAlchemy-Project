import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

# database setup
engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

# List all routes that are available.

@app.route('/')
def index():
    return (
        f"Available Routes:<br />"
        f"Precipitate info by date use: /api/v1.0/precipitation<br />"
        f"For list of stations use: /api/v1.0/stations<br />"
        f"Temperature Observations (tobs) for the previous year use: /api/v1.0/tobs<br />"
        f"JSON list of the min temp, avg temp, and max temp for start date (Use yyyy-mm-dd format): /api/v1.0/[start]<br />"
        f"JSON list of the min temp, avg temp, and max temp for start-end range (Use yyyy-mm-dd format and separate start and end dates using backslash and no spaces in between): /api/v1.0/[start]/[end]<br />"
    )


# Convert the query results to a Dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.

@app.route('/api/v1.0/precipitation')
def prcp_api():

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()

    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)
    
    return jsonify(all_prcp)


# Return a JSON list of stations from the dataset.

@app.route('/api/v1.0/stations')
def station_api():

    session = Session(engine)
    results = session.query(Station.station).all()

    # results= session.query(Measurement.station).group_by(Measurement.station).all()
    # return jsonify(results)
    all_stations = []
    for station in results:
        station_dict = {}
        station_dict['station'] = "".join(station)
        all_stations.append(station_dict)
    
    return jsonify(all_stations)


# query for the dates and temperature observations from a year from the last data point.
# Return a JSON list of Temperature Observations (tobs) for the previous year.

@app.route('/api/v1.0/tobs')
def tobs_api():

    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date > '2016-08-23').all()

    year_tobs = []
    for date, tobs in results:
        tobs_dict = {}
        tobs_dict['date'] = date
        tobs_dict['tobs'] = tobs
        year_tobs.append(tobs_dict)
           
    return jsonify(year_tobs)

# Return a JSON list of the minimum temperature, the average temperature, and the max 
# temperature for a given start.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater 
# than and equal to the start date.

@app.route('/api/v1.0/<start>')
def startonly_api(start):

    session = Session(engine)
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).all()
     
    return jsonify(results)


# Return a JSON list of the minimum temperature, the average temperature, and the max 
# temperature for a given start-end range.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` 
# for dates between the start and end date inclusive.

@app.route('/api/v1.0/<start>/<end>')
def startend_api(start, end):

    session = Session(engine)
    results1 = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
     
    return jsonify(results1)

if __name__ == "__main__":
    app.run(debug=True)
