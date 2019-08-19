# Location Handler (test)

glacial-hollows-86710.herokuapp.com/docs
Backend for location handler with functions to store and find location by pincode, latitude, longitude and place name. Some additional functions to get nearest locations by two ways and additional function added to get location in a geojson file. Powered by FastAPI and hosted on Heroku.

# Requirements

 1. Python 3.7.2
 2. FastAPI
 3. Postgresql
 
 Rest requirements are described in requirements.txt
 
# Initializing
Run glacial-hollows-86710.herokuapp.com/subtest/docs before running app for first time that contains following APIs,

## 1. /get_all
**Get all locations**,
For testing purpose. Returns all locations in 'location_id' table.

## 2. /first_timer/{flag}
**Initialize Earthdistance functions**,
For initial purpose. Initialize database with extensions cube and earthdistance for '/detect/'. Set flag to 1 for initializing.

## 3. /post_place
**Add geojson file**,
For initial purpose. Initialize 'geo_table' by adding map_geojson.txt file to database.
             

# List of APIs

## 1. /post_location

**Add new location in database**,
Insert new location with distinct pincode and location parameters. Check for close enough latitude and longitude. Returns id for new location and location data.
             

## 2. /get_location

**Get data from location database**,
Finds location by location parameters in 'location_id' table. 'lat' = Latitude. 'lon' = longitude. Both are of float data type.
             
## 3. /get_using_postgres

**Find nearby location using postgresql earthdistance**,
Get all locations in databse nerby given parameters within a range. Uses postgresql ll_to_earth and earth_distance function. 'lat' = Latitude. 'lon' = longitude. Both are of float data type. 'lim' = limit or boundary (integer type).
             

## 4. /get_using_self

**Find nearby location using user defined functions**,
Get all locations in databse nerby given parameters within a range. Uses python math functions. 'lat' = Latitude. 'lon' = longitude. Both are of float data type. 'lim' = limit or boundary (integer type).
             

## 5. /detect

**Get area name from Geojson**,
Get area name form boundaries defined in geojson file. 'lat' = Latitude. 'lon' = longitude. Both are of float data type.
             


# Testing

Install Pytest first to run tests,

    pip install pytest

Then simply run pytest command in test directory.

    /test> pytest


