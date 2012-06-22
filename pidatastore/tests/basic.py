from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

from pidatastore import Photo, Tag

engine = None

def connect():
    return create_engine('sqlite:///:memory:', echo=True)

def setUp():
    global engine

    if engine == None:
        engine = connect()
        Base.metadata.create_all(engine)

def testCreation():
    assert engine is not None
