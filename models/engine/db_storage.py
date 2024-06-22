#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from sqlalchemy import sessionmaker
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review


Session = sessiomaker()

class DBStorage:
    """engine for database storage of models"""
    __engine = None
    __session = None

    classes = {
               'User': User, 'State': State, 'Amenity': Amenity,
               'Place': Place, 'Review': Review
            }


    def __init__(self):
        """Initialization of the class instance"""
        USER = getenv('HBNB_MYSQL_USER')
        PASS = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        db_url = f"mysql+mysqldb://{USER}:{PASS}@localhost/{DB}"
        DBStorage.__engine = create_engine(db_url, pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all()

    def all(self, cls=None):
        Session.configure(bind=DBStorage.__engine)
        DBStorage.__session = Session()

        query_list = []
        obj_dict = {}

        if cls:
            query_list.extend(DBStorage.__session.query(cls).all())
        else:
            for cls in DBStorage.classes.values():
                query_list.extend(DBStorage.__session.query(cls).all())

        for obj in query_list:
            obj_dict[obj.__class__.__name__ + '.' + obj.id] = obj

        return obj_dict
