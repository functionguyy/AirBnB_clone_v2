#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Integer, Float, Table
from sqlalchemy.orm import relationship



place_amenity = Table("place_amenity", Base.metadata,
        Column("place_id", String(60), ForeignKey("place.id"),
            primary_key=True),
        Column("amenity_id", String(60), ForeignKey("amenities.id"),
            primary_key=True)
        )


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", cascade="all, delete", backref="place")
    amenities = relationship("Amenity", secondary=place_amenity,
                              viewonly=False)


    @property
    def reviews(self):
        """getter for FileStorage"""
        from models import storage
        review_list = []
        all_reviews = storage.all("Review")
        for key in all_reveiws.keys():
            if all_reviews[key].place_id == self.id:
                review_list.append(all_reviews[key])
        return review_list

    @property
    def amenities(self):

    if getenv("HBNB_TYPE_STORAGE") != "db":
        reviews = self.reviews()
