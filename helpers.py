#Import dependencies
from sqlalchemy import func, asc, desc


#App.py tobs: Find the most active station based on frequency in dataset
most = (session
    .query(Measurement.station,
           func.count(Measurement.station))
    .group_by(Measurement.station)
    .order_by(func.count(Measurement.station).desc())
    .first())  

#App.py tobs: Grab most active station id
most_station = most[0]
    
#App.py tobs: Find and return total prcp/rainfall by station for trip dates with station name, latitude, longitude, and elevation
def prcp_total (trip_start, trip_end, session, Measurement, Station):
    return (session
            .query(Measurement.station,
                   Station.name,
                   Station.latitude,
                   Station.longitude,
                   Station.elevation,
                   func.min(Measurement.date).label("start_date"),
                   func.max(Measurement.date).label("end_date"),
                   func.sum(Measurement.prcp).label("sum_rainfall"),
                   func.min(Measurement.prcp).label("min_rainfall"),
                   func.avg(Measurement.prcp).label("avg_rainfall"),
                   func.max(Measurement.prcp).label("max_rainfall"))
            .filter(Measurement.station == most_station)        
            .filter(Measurement.date >= trip_start)
            .filter(Measurement.date <= trip_end)
            .group_by(Measurement.station,
                      Station.name,
                      Station.latitude,
                      Station.longitude,
                      Station.elevation)
            .order_by(func.sum(Measurement.prcp).desc())
            .all())



#App.py trip dates: Find and return total prcp/rainfall by station for trip dates with station name, latitude, longitude, and elevation
def trip_total (trip_start, trip_end, session, Measurement, Station):
    return (session
            .query(Measurement.station,
                   Station.name,
                   Station.latitude,
                   Station.longitude,
                   Station.elevation,
                   func.min(Measurement.date).label("start_date"),
                   func.max(Measurement.date).label("end_date"),
                   func.sum(Measurement.prcp).label("sum_rainfall"),
                   func.min(Measurement.prcp).label("tmin_rainfall"),
                   func.avg(Measurement.prcp).label("tavg_rainfall"),
                   func.max(Measurement.prcp).label("tmax_rainfall"))
            .filter(Measurement.station == Station.station)        
            .filter(Measurement.date >= trip_start)
            .filter(Measurement.date <= trip_end)
            .group_by(Measurement.station,
                      Station.name,
                      Station.latitude,
                      Station.longitude,
                      Station.elevation)
            .order_by(func.sum(Measurement.prcp).desc())
            .all())