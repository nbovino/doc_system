from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Numeric, UnicodeText, TEXT, Boolean, JSON, DateTime
from sqlalchemy.dialects import postgresql
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import PasswordType

passlib = None
try:
    import passlib
    from passlib.context import LazyCryptContext
except ImportError:
    pass

from flask_login import UserMixin

Base = declarative_base()


# class ItemTypes(Base):
# #     __tablename__ = "item_types"
# #     id = Column(Integer, primary_key=True)
# #     item_type = Column(String, unique=True)
class Users(Base):
    __tablename__ = 'Users'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    username = Column(String, unique=True)
    password = Column(PasswordType(schemes=['pbkdf2_sha512']))


class Assets(Base):
    __tablename__ = 'Assets'#Tells what table using
    id = Column(Integer, primary_key=True)
    asset_type = Column(Integer)
    manufacturer = Column(Integer)
    model = Column(String)
    serial_no = Column(String)
    dia_asset_tag = Column(String, unique=True)
    name = Column(String)
    description = Column(TEXT)
    ip_address = Column(String)
    solutions = Column(ARRAY(Integer, dimensions=1))
    department = Column(Integer)
    date_added = Column(Date)
    date_revised = Column(DateTime)
    checked_out = Column(Boolean)
    location = Column(String)
    deployed = Column(Boolean)
    decommissioned = Column(DateTime)


class EquipmentSignOut(Base):
    __tablename__ = 'EquipmentSignOut'
    id = Column(Integer, primary_key=True)
    asset_id = Column(Integer, ForeignKey('Assets.id'))
    check_out_date = Column(Date)
    check_in_date = Column(Date)
    user = Column(Integer, ForeignKey('Users.id'))


class Departments(Base):
    __tablename__ = "Departments"
    id = Column(Integer, primary_key=True)
    department = Column(String)


class ItemModels(Base):
    __tablename__ = "ItemModels"
    id = Column(Integer, primary_key=True)
    item_model = Column(String)
    manufacturer = Column(Integer, ForeignKey("Manufacturers.id"))
    item_desc = Column(TEXT)


class Manufacturers(Base):
    __tablename__ = 'Manufacturers'
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
    public = Column(Boolean, default=False)
