# -*- coding: utf-8 -*-
"""
Created on Wed Jul 31 20:25:26 2019

@author: MOJO-JOJO
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
#import os
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:1234@localhost:5432/location_db"
#SQLALCHEMY_DATABASE_URL = "postgres+psycopg2://$(whoami)"
SQLALCHEMY_DATABASE_URL = "postgres://exqokjsiwrkslh:e55831391dde495b7d33e4c2b37de96fa7c9ad50f44484aea80a89fcfb4ddda8@ec2-54-225-72-238.compute-1.amazonaws.com:5432/d9mgc66is0glh9"


#DATABASE_URL = os.environ['DATABASE_URL']

#conn = psycopg2.connect(DATABASE_URL, sslmode='require')


engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()