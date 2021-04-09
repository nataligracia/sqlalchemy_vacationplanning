#Import dependencies
from sqlalchemy import func, asc, desc

#App.py tobs: Find and return temp for most recent year with station information
def trip_tobs (trip_start, trip_end, session, Measurement, Station):
    return (session
            .query(Measurement.station,
                   Station.name,
                   Station.latitude,
                   Station.longitude,
                   Station.elevation,
                   func.min(Measurement.date).label("start_date"),
                   func.max(Measurement.date).label("end_date"),
                   func.min(Measurement.tobs).label("min_temp"),
                   func.avg(Measurement.tobs).label("avg_temp"),
                   func.max(Measurement.tobs).label("max_temp"),
                   func.count(Measurement.station).label("data_count"))
            .filter(Measurement.station == Station.station)        
            .filter(Measurement.date >= trip_start)
            .filter(Measurement.date <= trip_end)
            .group_by(Measurement.station,
                      Station.name,
                      Station.latitude,
                      Station.longitude,
                      Station.elevation)
            .order_by(func.count(Measurement.station).desc())
            .first())

#App.py temp: Find and return temp for trip dates with station information
def trip_total (trip_start, trip_end, session, Measurement, Station):
    return (session
            .query(Measurement.station,
                   Station.name,
                   Station.latitude,
                   Station.longitude,
                   Station.elevation,
                   func.min(Measurement.date).label("start_date"),
                   func.max(Measurement.date).label("end_date"),
                   func.min(Measurement.tobs).label("tmin_temp"),
                   func.avg(Measurement.tobs).label("tavg_temp"),
                   func.max(Measurement.tobs).label("tmax_temp"),
                   func.count(Measurement.station).label("data_count"))
            .filter(Measurement.station == Station.station)        
            .filter(Measurement.date >= trip_start)
            .filter(Measurement.date <= trip_end)
            .group_by(Measurement.station,
                      Station.name,
                      Station.latitude,
                      Station.longitude,
                      Station.elevation)
            .order_by(func.count(Measurement.station).desc())
            .all())
