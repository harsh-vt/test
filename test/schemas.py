# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 00:49:50 2019

@author: MOJO-JOJO
"""

from pydantic import BaseModel
    
class post_Places(BaseModel):
    pincode: str
    place_name: str
    admin_name1: str
    latitude: float = None
    longitude: float = None
    accuracy: int = None
    class Config:
        orm_mode = True
class get_Places(post_Places):
    id: int
    class Config:
        orm_mode = True
class find_Places(BaseModel):
    id: int
    place_name: str
    latitude: float
    longitude: float
    class Config:
        orm_mode = True

