################
#Import dependencies
################

from matplotlib import figure, style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import calendar
from scipy import stats, mean

#Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, asc , desc, and_

#Flask modules
from flask import Flask, jsonify

#Local modules
import helpers


################
#Database Setup
################

#SQL Use Tool
engine = create_engine("sqlite:///data/hawaii.sqlite")

#Reflect database into new model
Base = automap_base()

#Reflect the tables and pass in the engine
Base.prepare(engine, reflect=True)

#Label tables from classes
Station = Base.classes.station
Measurement = Base.classes.measurement

#Create a session and bind it to the engine
session = Session(engine)

#App.py prcp: Find the most recent date
recent = (session
          .query(Measurement.date)
          .order_by(Measurement.date.desc()).first())
    
#App.py prcp: Make most recent date a variable
date_parts = [int(date_part) for date_part in recent[0].split("-")]

#App.py prcp: Find the date from 1 year/12 months/365 days ago
year = datetime.date(*date_parts) - datetime.timedelta(days=365)

#Stop query session
session.close()


################
#Flask Setup
################

#Create an app for Flask setup
app = Flask(__name__)


################
#Flask Routes
################

#List all available api routes
@app.route("/")
def welcome():
    print("Server received request for 'Welcome' page...")
    return (
        f"Welcome to the Vacation to Honolulu, Hawaii Trip Planner!<p>"
        f"Filter for your trip:<br/>"
        f"/api/v1.0/precitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br>"
        f"/api/v1.0/temp/[start]<br>"
        f"/api/v1.0/temp/[start]/[end]")    


#API Route for Precipitation Data
@app.route("/api/v1.0/precitation")
def precipitation():
    print("""Return one year date from most recent in data as json""")
    
    #Create a session and bind it to the engine
    session = Session(engine)
    
    #App.py: Find all dates and prcp within last 12 months
    results_query = (session
                     .query(Measurement.date,func.avg(Measurement.prcp))
                     .filter(Measurement.date >= year, Measurement.prcp != None)
                     .group_by(Measurement.date)
                     .all())
    
    #Stop query session
    session.close()
    
    #Create a dictonary comprehension to store year prcp data in json
    results_precitation = {date: prcp for date, prcp in results_query}
    return jsonify(results_precitation)


#API Route for Station Data
@app.route("/api/v1.0/stations")
def stations():
    print("""Return station data as json""")
    
    #Create a session and bind it to the engine
    session = Session(engine)
    
   #List of station ids in station
    locations_list = session.query(Station.station).all()
    
    #Stop query session
    session.close()
    
    #Unravel results from id array to list
    id_list = np.ravel(locations_list, order='K')  
    
    return jsonify(list(id_list))

   
#API Route for tobs Data
@app.route("/api/v1.0/tobs")
def temp_monthly():
    print("""Return tobs data as json""")
    
    #Create a session and bind it to the engine
    session = Session(engine)
    
    
    #App.py tobs: Find the most active station based on frequency in dataset
    most = (session
        .query(Measurement.station,func.count(Measurement.station))
        .group_by(Measurement.station)
        .order_by(func.count(Measurement.station).desc()).first())  

    #App.py tobs: Grab most active station id
    most_station = most[0]
    
    #Results for trip dates
    prcp_stations = helpers.prcp_total('2016-08-28', '2016-09-03', session, Measurement, Station)
    
    #Find and return total prcp/rainfall by station for trip dates
    results = [result._asdict() for result in prcp_stations]
    
    #Stop query session
    session.close()
    
    #Unravel results from id array to list
    #prcpstations_list = list(np.ravel(prcp_stations, order='K'))  
    return jsonify(results)


#API Route for trip dates Data
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    
    #Create a session and bind it to the engine
    session = Session(engine)
    
    if end is not None:

        #Results for trip dates
        prcp_stations = helpers.trip_total(start, end, session, Measurement, Station)

        #Unravel results from id array to list
        selected_list = [result._asdict() for result in prcp_stations]
    
    else:
        
        #Results for trip dates
        prcp_stations = helpers.trip_total(start, datetime.date(*date_parts), session, Measurement, Station)

        #Unravel results from id array to list
        selected_list = [result._asdict() for result in prcp_stations]
    
    #Stop query session
    session.close()
    
    return jsonify(selected_list)
    

#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)