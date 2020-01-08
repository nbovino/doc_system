from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Numeric, UnicodeText, TEXT, Boolean
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


# class ItemTypes(Base):
# #     __tablename__ = "item_types"
# #     id = Column(Integer, primary_key=True)
# #     item_type = Column(String, unique=True)