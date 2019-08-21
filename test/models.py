# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 00:22:15 2019

@author: MOJO-JOJO
"""

from sqlalchemy import Column, Integer, String, Float

from .database import Base


class Places(Base):
    __tablename__ = "location_id"

    id = Column(Integer, primary_key=True, index=True)
    pincode = Column(String, unique=True, index=True)
    place_name = Column(String)
    admin_name = Column(String)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
    accuracy = Column(Integer)
    
class Geof(Base):
    __tablename__ = "geo_table"

    id = Column(Integer, primary_key=True, index=True)
    place_name = Column(String)
    latitude = Column(Float, index=True)
    longitude = Column(Float, index=True)
