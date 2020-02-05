from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Numeric, UnicodeText, TEXT, Boolean, JSON, ARRAY
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin

Base = declarative_base()


# class ItemTypes(Base):
# #     __tablename__ = "item_types"
# #     id = Column(Integer, primary_key=True)
# #     item_type = Column(String, unique=True)

class Assets(Base):
    __tablename__ = 'Assets'#Tells what table using
    id = Column(Integer, primary_key=True)
    asset_type = Column(Integer)
    name = Column(String)
    description = Column(TEXT)
    solutions = Column(ARRAY(Integer, dimensions=1))
    ip_address = Column(String)


class AssetTypes(Base):
    __tablename__ = 'AssetTypes'#Tells what table using
    id = Column(Integer, primary_key=True)
    asset_type = Column(String, unique=True)


class Software(Base):
    __tablename__ = 'Software'
    id = Column(Integer, primary_key=True)
    software_name = Column(String, unique=True)
    software_version = Column(String)


class Solutions(Base):
    __tablename__ = 'Solutions'#Tells what table using
    id = Column(Integer, primary_key=True)
    solution_title = Column(String)
    steps = Column(JSON)
    date_added = Column(Date)
    date_revised = Column(Date)
    user = Column(Integer)
    associated_solutions = Column(ARRAY(Integer, dimensions=1))
    associated_assets = Column(ARRAY(Integer, dimensions=1))
    associated_asset_types = Column(ARRAY(Integer, dimensions=1))
    associated_software = Column(ARRAY(Integer, dimensions=1))
