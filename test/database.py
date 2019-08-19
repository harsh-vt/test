# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 20:25:26 2019

@author: MOJO-JOJO
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgres://wsqprfypwgeksc:906144aad5862c6733154d92c04c1a861f6fb17237f46be225e8128da428204c@ec2-23-21-91-183.compute-1.amazonaws.com:5432/d1ev6uehp66juh"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()