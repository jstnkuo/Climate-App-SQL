import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#database set up 
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(bind=engine)

#flask set up
app = Flask(__name__)

#flash route
@app.route("/")
def home():
    return("hello")

@app.route("/api/v1.0/precipitation")
def prcp():
    # Design a query to retrieve the last 12 months of precipitation data and plot the results. 
    # Starting from the most recent data point in the database. 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate the date one year from the last date in data set.
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)


    # Perform a query to retrieve the data and precipitation scores
    sel = [Measurement.date, Measurement.prcp]

    measurement_year = session.query(*sel)\
                              .filter(Measurement.date>=one_year)\
                              .all()
    session.close()
    precip = {date: prcp for date, prcp in measurement_year}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    stations = session.query(Station.station).all()    
    return jsonify(stations)

#run flask
if __name__ == '__main__':
    app.run()
