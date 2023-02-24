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
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/start_date/end_date<br/>"
        f"start_date and end_date must be in date format YYYY-MM-DD"
        f"example of route: /api/v1.0/2015-08-18/2015-10-01"
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
    tobs_result = session.query(Measurement.tobs)\
                         .filter(Measurement.date>=one_year)\
                         .filter(Measurement.station == 'USC00519281')\
                         .all()
    session.close()

    # Convert to normal list
    tobs_year = list(np.ravel(tobs_result))
    return jsonify(tobs_year)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp(start=None, end=None):
    # Create our session (link) from Python to the DB
    session = Session(bind=engine)

    # if no end date is input
    if not end:

        # Query min, avg, max temp with start date as a dynamic variable
        min_temp = session.query(func.min(Measurement.tobs))\
                          .filter(Measurement.date>=dt.datetime.strptime(start,"%Y-%m-%d"))\
                          .filter(Measurement.station == 'USC00519281')\
                          .all()
        avg_temp = session.query(func.avg(Measurement.tobs))\
                          .filter(Measurement.date>=dt.datetime.strptime(start,"%Y-%m-%d"))\
                          .filter(Measurement.station == 'USC00519281')\
                          .all()
        max_temp = session.query(func.max(Measurement.tobs))\
                          .filter(Measurement.date>=dt.datetime.strptime(start,"%Y-%m-%d"))\
                          .filter(Measurement.station == 'USC00519281')\
                          .all()
        
        # Put the results into a list
        temp_list=[]
        temp_list.append(min_temp)
        temp_list.append(avg_temp)
        temp_list.append(max_temp)

        # Convert to normal list 
        all_temps= list(np.ravel(temp_list))

        return jsonify(all_temps)

    # if end date is provided
    else:

        # Query min, avg, max temp with start date and end date as a dynamic variables
        min_temp = session.query(func.min(Measurement.tobs))\
                          .filter(Measurement.date>=dt.datetime.strptime(start,"%Y-%m-%d"))\
                          .filter(Measurement.date<=dt.datetime.strptime(end,"%Y-%m-%d"))\
                          .filter(Measurement.station == 'USC00519281')\
                          .all()
        avg_temp = session.query(func.avg(Measurement.tobs))\
                          .filter(Measurement.date>=dt.datetime.strptime(start,"%Y-%m-%d"))\
                          .filter(Measurement.date>=dt.datetime.strptime(end,"%Y-%m-%d"))\
                          .filter(Measurement.station == 'USC00519281')\
                          .all()
        max_temp = session.query(func.max(Measurement.tobs))\
                          .filter(Measurement.date>=dt.datetime.strptime(start,"%Y-%m-%d"))\
                          .filter(Measurement.date>=dt.datetime.strptime(end,"%Y-%m-%d"))\
                          .filter(Measurement.station == 'USC00519281')\
                          .all()


        # Put the results into a list
        temp_list=[]
        temp_list.append(min_temp)
        temp_list.append(avg_temp)
        temp_list.append(max_temp)

        #Convert to normal list
        all_temps= list(np.ravel(temp_list))

        return jsonify(all_temps)
        
    session.close()
    
#run flask
if __name__ == '__main__':
    app.run()
