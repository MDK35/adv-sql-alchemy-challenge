# Import the dependencies.
import datetime as dt
import numpy as np

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import session
from aqlalchemy import create_engine, func

from flask import Flask, jsonify


engine = create_engine("sqlite:///Resoruces/hawaii.sqlite")


#################################################
# Database Setup
#################################################


# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine)

# reflect the tables
Measurement = Base.classes.measurement

# Save references to each table
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def welcome():
    return(
        f"Welcome to the Hawaii Climate Analysis API<br/>"
        f"Available Routes: <br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start<br/>"
        f"/api/v1.0/temp/end<br/>"
        f"<p> 'start' and 'end' date should be in the format MMDDYYYY.</p>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    pre_year = dt.date(2017, 8 , 23) - dt.timedelta(days=365)

    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= pre_year).all()

    session.close()

    precipitation2= {date: prcp for date, prcp in precipitation}

    return jsonify(precipitation2)


@app.route("/api/v1.0/stations")
def stations():
    results = session.query(Station.station).all()

    session.close()

    stations = list(np.ravel(results))

    return jsonify(stations=stations)


@app.route("/api/v1.0/tobs")
def temp_monthly(): 
    pre_year = dt.date(2017,8,23) - dt.timedelta(days=365)

    results = session.query(Measurement).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= pre_year).all()

    session.close()

    print()

    temps = list(np.ravel(results))

    return jsonify (temps=temps)


@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None , end=None):

    sel =[func.min(Measurement.tobs), func.max(Measuremnt.tobs), func.avg]


    if not end:
        start = dt.datetime.strptime(start, "%m%d%y")
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()


        session.close

        temps = list(np.ravel(results))
        return jsonify(temps)

    start =  dt.datetime.strptime(start, "%m%d%y")
    end =  dt.datetime.strptime(end, "%m%d%y")

    results = session.query(*sel).\
            filter(Measurement.date >= start).\
            filter(Measurement.date <= start).all()
print(start)
print(end)
print(results)

    session.close()

    temps = list(np.ravel(results))

    return jsonify(temps=temps)

    if __name__ == "__main__":
        app.run(debug=True)