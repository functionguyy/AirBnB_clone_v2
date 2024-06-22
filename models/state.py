#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.city import City

class State(BaseModel, Base):
    """ State class """

    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref="state", cascade="all, delete")

    @property
    def cities(self):
        """getter for FileStorage"""
        from models import storage
        city_list = []
        all_cities = storage.all("City")
        for key in all_cities.keys():
            if all_cities[key].state_id == self.id:
                city_list.append(all_cities[key])
        return city_list
