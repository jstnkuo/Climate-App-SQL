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

#flask set up
app = Flask(__name__)

#flash route
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/stations<br/>"
    )

@app.route("/api/v1.0/precipitation")
def prcp():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

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

    # Input result into a dictionary
    precip = {date: prcp for date, prcp in measurement_year}
    return jsonify(precip)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # Query to select all the stations from dataset
    stations = engine.execute('select station from station').fetchall()
    session.close()

    # Convert to normal list
    all_stations= list(np.ravel(stations))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    #Query the dates and temperature observations of the most-active station 
    #for the previous year of data
    one_year = dt.date(2017,8,23) - dt.timedelta(days=365)
    tobs_result = session.query(Measurement.tobs).filter(Measurement.date>=one_year).filter(Measurement.station == 'USC00519281').all()
    session.close()

    # Input result into a dictionary
    tobs_year = list(np.ravel(tobs_result))
    return jsonify(tobs_year)


#run flask
if __name__ == '__main__':
    app.run()
