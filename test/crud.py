# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 01:02:46 2019

@author: MOJO-JOJO
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from math import radians, cos, sin, asin, sqrt
from . import models, schemas

# function to initialize database
def initial(db):
    db.execute("""CREATE EXTENSION cube;
CREATE EXTENSION earthdistance;""")
    return 1

# function to get all
def get_all(db):
    return db.query(models.Places).all()
    
# function for finding place by latitude and longitude stored in database
def get_place_by_lat_n_lon(db: Session, lat: float, lon: float):
    return db.query(models.Places).filter(models.Places.latitude == lat, models.Places.longitude == lon).all()

# function for finding place by pincode in database
def get_place_by_pin(db: Session, pin: str):
     return db.query(models.Places).filter(models.Places.pincode == pin).all()

# function to find places in the database within certain 'lim' Kms radius of given latitude and longitude using postgres 'earthradius module'
# run query in postgres for extention cube, earthdistance before calling this function 
def get_place_using_postgres(db: Session, lat: float, lon: float, lim:int):
    db_list = db.query(models.Places).filter((func.earth_distance(func.ll_to_earth(models.Places.latitude, models.Places.longitude),func.ll_to_earth(lat, lon))/1000)<1).order_by(func.earth_distance(func.ll_to_earth(models.Places.latitude, models.Places.longitude),func.ll_to_earth(lat, lon))/1000).all()
    print(db_list)
    return db_list

# function to find places in the database within certain 'lim' Kms radius of given latitude and longitude using math functions
def get_place_using_self(db: Session, lat1: float, lon1: float, lim:int):
    db_temp = db.query(models.Places.id, models.Places.place_name, models.Places.latitude, models.Places.longitude).all()
    lat = []
    lon = []
    for i in range(len(db_temp)):
        x = db_temp[i][2]
        lat.append(x)
        y = db_temp[i][3]
        lon.append(y)
    lat = list(filter(lambda x: x!=None, lat))
    lon = list(filter(lambda x: x!=None, lon))
    lat_ = list(map(lambda i: radians(i), lat))
    lon_ = list(map(lambda i: radians(i), lon))
    lon1, lat1 = map(radians, [lon1, lat1])
    res = []
    for i in range(len(lat_)):
        xlon = lon1 - lon_[i]
        xlat = lat1 - lat_[i]
        p = sin(xlat / 2) ** 2 + cos(lat1) * cos(lat_[i]) * sin(xlon / 2) ** 2
        q = 2 * asin(sqrt(p))
        r = 6371.00
        s = q * r
        res.append(s)
    dl = []
    for i in res:
        if i <= lim:
            iy = 'In radius'
        else:
            iy = 'Outside radius'
        dl.append(iy)
    latitu = [lat for a, lat in zip(dl, lat) if a.startswith('In')]
    longitu = [lon for a, lon in zip(dl, lon) if a.startswith('In')]
    db_list = db.query(models.Places).filter(models.Places.latitude.in_(latitu), models.Places.longitude.in_(longitu)).all()
    return db_list

# function to validate if location is present in the database by latitude and longitude 
def loc_check(db: Session, lat: float, lon: float):
    llist = db.query(models.Places).filter((func.earth_distance(func.ll_to_earth(models.Places.latitude, models.Places.longitude),func.ll_to_earth(lat, lon))/1000)<1).all()
    if len(llist)>0:
        return 1
    
# function to validate if location is present in the database by pincode
def pin_check(db: Session, pin: str):
    return db.query(models.Places).filter(models.Places.pincode == pin).all()

# function to add place in database table "location_id"
def post_place(db: Session, place: schemas.post_Places):
    db_place = models.Places(latitude = place.latitude, longitude =  place.longitude, pincode =  place.pincode, place_name =  place.place_name,
                            admin_name =  place.admin_name)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

# function to add place in database table "geo_table"
def post_geof(db: Session, place: str,  lat: float, lon: float):
    db_place = models.Geof(place_name =  place, latitude = lat, longitude =  lon)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)

# function to get location area name stored in database table "geo_table" accurate upto 0.1 degree
def get_geof(db: Session, lat: float, lon: float):
    llist = db.query(models.Geof.id).filter((func.earth_distance(func.ll_to_earth(models.Geof.latitude, models.Geof.longitude),func.ll_to_earth(lat, lon))/1000)<1).order_by(func.earth_distance(func.ll_to_earth(models.Geof.latitude, models.Geof.longitude),func.ll_to_earth(lat, lon))/1000).all()
    print(llist)
    if len(llist)<1:
        return False
    else:
        return db.query(models.Geof.place_name).filter(models.Geof.id == llist[0][0]).all()