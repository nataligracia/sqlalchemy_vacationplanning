#Import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#Database setup
engine = create_engine("sqlite:///data/hawaii.sqlite")

#Reflect database into new model of tables
Base = automap_base()

#Reflect data in tables
Base.prepare(engine, reflect=True)

#Find classes that automap found with Base.classes
Base.classes.keys()

#Label tables from classes
Station = Base.classes.station
Measurement = Base.classes.measurement

#Create a session and bind it to the engine
Session = Session(engine)

#Create an app for Flask setup
app = Flask(__name__)

#Define user experience for index ISSUE MULTILINE
@app.route("/")
def welcome():
    print("Server received request for 'Welcome' page...")
    return "Welcome to my page! This is awesome!"

#Define user experience for precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    print("Server received request for 'About' page...")
    return "This is our precipitation data for Honolulu, Hawaii!"

#Define main behavior
if __name__ == "__main__":
    app.run(debug=True)


# define a precipitation() function that returns jsonified precipitation data from the database
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database

    # Query for the date and precipitation for the last year

    # Create a dictionary to store the date: prcp pairs. 
    # Hint: check out a dictionary comprehension, which is similar to a list comprehension but allows you to create dictionaries
    
    # Return the jsonify() representation of the dictionary
    
# Set the app.route() decorator for the "/api/v1.0/stations" route
# define a stations() function that returns jsonified station data from the database
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Query for the list of stations

    # Unravel results into a 1D array and convert to a list
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    
    # Return the jsonify() representation of the list


# Set the app.route() decorator for the "/api/v1.0/tobs" route
# define a temp_monthly() function that returns jsonified temperature observations (tobs) data from the database
# In the function (logic should be the same from the starter_climate_analysis.ipynb notebook):
    # Calculate the date 1 year ago from last date in database

    # Query the primary station for all tobs from the last year
    
    # Unravel results into a 1D array and convert to a list
    # Hint: checkout the np.ravel() function to make it easier to convert to a list
    
    # Return the jsonify() representation of the list


# Set the app.route() decorator for the "/api/v1.0/temp/<start>" route and "/api/v1.0/temp/<start>/<end>" route
# define a stats() function that takes a start and end argument, and returns jsonified TMIN, TAVG, TMAX data from the database
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    # If the end argument is None:
        # calculate TMIN, TAVG, TMAX for dates greater than start
        
        # Unravel results into a 1D array and convert to a list
        # Hint: checkout the np.ravel() function to make it easier to convert to a list
    
        # Return the jsonify() representation of the list

    # Else:
        # calculate TMIN, TAVG, TMAX with both start and stop
        
        # Unravel results into a 1D array and convert to a list
        # Hint: checkout the np.ravel() function to make it easier to convert to a list
    
        # Return the jsonify() representation of the list


if __name__ == '__main__':
    app.run()
