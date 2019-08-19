# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 01:15:09 2019

@author: MOJO-JOJO
"""

from typing import List
import geojson, json, os
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, exc
from starlette.requests import Request
from starlette.responses import Response, PlainTextResponse, HTMLResponse
from fastapi.exceptions import RequestValidationError
from . import crud, models, schemas
from .database import SessionLocal, engine
from starlette.middleware.cors import CORSMiddleware


models.Base.metadata.create_all(bind=engine)

app = FastAPI()
exceptions = exc.sa_exc

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


# Dependency
def get_db(request: Request):
    return request.state.db

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return PlainTextResponse(str(exc), status_code=400)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Hi</title>
    </head>
    <body>
        <h1>Testing 123</h1>
    </body>
</html>
"""
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

subtest = FastAPI(openapi_prefix="/subtest")

@app.get("/")
async def get():
    return HTMLResponse(html)

@subtest.get("/first_timer/{flag}")
def first_timer(flag:int,  db: Session = Depends(get_db)):
    if flag == 1:
        db_place = crud.initial(db)
        if db_place != 1:
            HTMLResponse(content = "database initialized successfully", status_code=200)
    return HTMLResponse(status_code=200, detail="wrong flag or selected 0. try again later after create_geof if something wrong there")

@app.post("/post_location/", response_model=schemas.get_Places)
def post_location(place: schemas.post_Places, db: Session = Depends(get_db)):
    try: 
        db_place = crud.loc_check(db, lat =  place.latitude, lon = place.longitude)
        if db_place:
            raise HTTPException(status_code=418, detail="Location already registered by latitude and longitude")
        db_place = crud.pin_check(db, pin = place.pincode)
        if db_place:
            raise HTTPException(status_code=418, detail="Location already registered by pincode")
        return crud.post_place(db=db, place=place)
    except TypeError:
        return crud.post_place(db=db, place=place)
    
@app.get("/get_location/", response_model=List[schemas.get_Places])
def get_location(lat: float, lon: float, db: Session = Depends(get_db)):
    db_place = crud.get_place_by_lat_n_lon(db, lat, lon)
    if len(db_place)<1:
        raise HTTPException(status_code=420, detail="Location not found")
    return db_place

@app.get("/get_using_postgres/", response_model=List[schemas.get_Places])
def get_using_postgres(lat: float, lon: float, lim: int, db: Session = Depends(get_db)):
    db_list = crud.get_place_using_postgres(db, lat, lon, lim)
    if len(db_list)<1:
        HTMLResponse(content = "Cities in database are not within the limit. Change location or limit.", status_code=201)
    return db_list

@app.get("/get_using_self/", response_model=List[schemas.get_Places])
def get_using_self(lat: float, lon: float, lim: int, db: Session = Depends(get_db)):
    db_list = crud.get_place_using_self(db, lat, lon, lim)
    return db_list

@subtest.post("/find_place/post_files/")
def create_geof(db: Session = Depends(get_db)):
   # with open('map.geojson.txt') as json_file:
   with open(os.path.join(__location__, "map_geojson.txt")) as f:
       for lines in f:
           data = json.loads(lines)
   for i in range(len(data['features'])):
       placename = data['features'][i]['properties']['name']
       coor = list(geojson.utils.coords(data['features'][i]['geometry']))
       for j in coor:
           crud.post_geof(db, placename, j[0], j[1])
   return HTMLResponse(content = "database posted successfully", status_code=200)

@app.get("/detect/", response_model=List)
def get_geof(lat: float, lon: float, db: Session = Depends(get_db)):
    db_place = crud.get_geof(db, lat, lon)
    if db_place is False:
        raise HTTPException(status_code=404, detail="Location not found")
    return db_place


@subtest.get("/find_place")
async def main():
    content = """
<body>
<form action="/find_place/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file">
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
app.mount("/subtest", subtest)