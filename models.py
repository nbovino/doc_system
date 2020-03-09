from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Numeric, UnicodeText, TEXT, Boolean, JSON, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
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
    manufacturer = Column(Integer)
    model = Column(String)
    serial_no = Column(String)
    dia_asset_tag = Column(String)
    name = Column(String)
    description = Column(TEXT)
    ip_address = Column(String)
    solutions = Column(ARRAY(Integer, dimensions=1))
    department = Column(Integer)
    date_added = Column(Date)
    date_revised = Column(DateTime)


class Departments(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True)
    department = Column(String)


class ItemModels(Base):
    __tablename__ = "item_models"
    id = Column(Integer, primary_key=True)
    item_model = Column(String, unique=True)
    manufacturer = Column(Integer, ForeignKey("manufacturers.id"))
    item_desc = Column(TEXT)


class Manufacturers(Base):
    __tablename__ = 'manufacturers'
    id = Column(Integer, primary_key=True)
    manufacturer = Column(String, unique=True)


class AssetTypes(Base):
    __tablename__ = 'AssetTypes'#Tells what table using
    id = Column(Integer, primary_key=True)
    asset_type = Column(String, unique=True)


class Software(Base):
    __tablename__ = 'Software'
    id = Column(Integer, primary_key=True)
    software_name = Column(String, unique=True)
    software_version = Column(String)


#TODO: Make another column for primary asset type. Mainly to show when searching to associate solutions
class Solutions(Base):
    __tablename__ = 'Solutions'  #Tells what table using
    id = Column(Integer, primary_key=True)
    solution_title = Column(String)
    steps = Column(JSON)
    date_added = Column(Date)
    date_revised = Column(DateTime)
    user = Column(Integer)
    associated_solutions = Column(ARRAY(Integer, dimensions=1))
    associated_assets = Column(ARRAY(Integer, dimensions=1))
    primary_asset_type = Column(Integer)
    associated_asset_types = Column(ARRAY(Integer, dimensions=1))
    associated_software = Column(ARRAY(Integer, dimensions=1))
