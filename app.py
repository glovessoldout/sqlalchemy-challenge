#!/usr/bin/env python
# coding: utf-8

import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import date,timedelta
from flask import Flask, jsonify
app = Flask(__name__)

#db query setup
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
base = automap_base()
base.prepare(engine, reflect=True)
Measurement = base.classes.measurement
Station = base.classes.station

stations_list = [
    {"station":"USC00519397", "name":"WAIKIKI 717.2, HI US"},
    {"station":"USC00519281", "name":"WAIHEE 837.5, HI US"},
    {"station":"USC00516128", "name":"MANOA LYON ARBO 785.2, HI US"},
    {"station":"USC00513117", "name":"KANEOHE 838.1, HI US"},
    {"station":"USC00519523", "name":"WAIMANALO EXPERIMENTAL FARM, HI US"},
    {"station":"USC00514830", "name":"KUALOA RANCH HEADQUARTERS 886.9, HI US"},
    {"station":"USC00517948", "name":"PEARL CITY, HI US"}]

#flask
@app.route("/")
def home():
    print("Server received request for 'Home' page...")
    return (
        "Homework 10 Flask App API<br/>"
        "Available Routes:<br/>"
        "<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start-date<br/>"
        "/api/v1.0/start-date/end-date<br/>"
           )

@app.route("/api/v1.0/precipitation")
def about():
    session = Session(engine)
    Measurements = session.query(Measurement.date,Measurement.prcp).all()
    session.close()
    #Measurements_df = pd.DataFrame(Measurements)
    print("jsonify precipitation")
    return jsonify(Measurements)

@app.route("/api/v1.0/stations")
def welcome():
    print("Stations operational")
    return (jsonify(stations_list))

@app.route("/api/v1.0/tobs")
def temperatures():
    session = Session(engine)
    last_date = date.fromisoformat(session.query(func.max(Measurement.date)).all()[0][0])
    year = timedelta(days=365)
    first_date = last_date - year
    top_station = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
    filter(Measurement.date <= last_date, Measurement.date >= first_date, Measurement.station == "USC00519397").all()
    session.close()
    print("jsonify temperatures")
    return jsonify(top_station)

#    temperatures = [{"TMIN":f"{min_temp}"},{"TMAX":F"{max_temp}"},{"TAVG":f"{avg_temp}"}]

@app.route("/api/v1.0/<start>")
def start_date(start):
    session = Session(engine)
    
    max_temp = session.query(Measurement.date, func.max(Measurement.tobs), Measurement.station).\
    filter(Measurement.date >= start, Measurement.station == "USC00519397").all()
    min_temp = session.query(Measurement.date, func.min(Measurement.tobs), Measurement.station).\
    filter(Measurement.date >= start, Measurement.station == "USC00519397").all()
    avg_temp = session.query(Measurement.date, func.avg(Measurement.tobs), Measurement.station).\
    filter(Measurement.date >= start, Measurement.station == "USC00519397").all()
    session.close()
    temperatures = [{"TMIN":f"{min_temp}"},{"TMAX":F"{max_temp}"},{"TAVG":f"{avg_temp}"}]
    print("start works")
    return jsonify(temperatures)

@app.route("/api/v1.0/<start>/<end>")
def start_end_date(start,end):
    session = Session(engine)
    
    max_temp = session.query(Measurement.date, func.max(Measurement.tobs), Measurement.station).\
    filter(Measurement.date <= end, Measurement.date >= start, Measurement.station == "USC00519397").all()
    min_temp = session.query(Measurement.date, func.min(Measurement.tobs), Measurement.station).\
    filter(Measurement.date <= end, Measurement.date >= start, Measurement.station == "USC00519397").all()
    avg_temp = session.query(Measurement.date, func.avg(Measurement.tobs), Measurement.station).\
    filter(Measurement.date <= end, Measurement.date >= start, Measurement.station == "USC00519397").all()
    session.close()
    temperatures = [{"TMIN":f"{min_temp}"},{"TMAX":F"{max_temp}"},{"TAVG":f"{avg_temp}"}]
    print("start and end works")
    return jsonify(temperatures)




if __name__ == "__main__":
    app.run(debug=True)

