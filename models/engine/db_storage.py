#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""
from sqlalchemy import create_engine
from os import getenv
from models.base_model import Base
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review



class DBStorage:
    """engine for database storage of models"""
    __engine = None
    __session = None

    classes = {
               'User': User, 'State': State, 'Amenity': Amenity,
               'Place': Place, 'Review': Review, 'City': City
            }


    def __init__(self):
        """Initialization of the class instance"""
        USER = getenv('HBNB_MYSQL_USER')
        PASS = getenv('HBNB_MYSQL_PWD')
        HOST = getenv('HBNB_MYSQL_HOST')
        DB = getenv('HBNB_MYSQL_DB')
        db_url = f"mysql+mysqldb://{USER}:{PASS}@{HOST}/{DB}"
        self.__engine = create_engine(db_url, pool_pre_ping=True,
                echo=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ query on the current database session all objects depending on the
        class name"""
        query_list = []
        obj_dict = {}

        if cls is not None:
            if isinstance(cls, str):
                cls = self.classes.get(cls)
            query_list.extend(self.__session.query(cls).all())
        else:
            for cls in self.classes.values():
                try:
                    query_list.extend(self.__session.query(cls).all())
                except:
                    continue

        for obj in query_list:
            obj_dict[obj.__class__.__name__ + '.' + obj.id] = obj

        return obj_dict


    def new(self, obj):
        """add the object to current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """ delete from the current database session"""

        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ create all tables in the database"""
        Base.metadata.create_all(self.__engine)
        sess = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess)
        self.__session = Session()
