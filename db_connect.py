from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy import extract
from sqlalchemy import asc, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Assets, AssetTypes, Solutions
import os

try:
    # engine = create_engine('sqlite:///docutest.db', echo=True)
    engine = create_engine('postgresql://postgres:unitedFries28@localhost/doc_system')
    print("Opened database successfully")

except Exception as e:
    print("Error during connection: ", str(e))


Base.metadata.create_all(engine)

Base.metadata.bind = engine


def insert_db(v):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(v)
        session.commit()
    except exc.IntegrityError:
        pass
    except:
        print('Exeption!')


def query_all(v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(v).all()


def query_filtered(model, model_column, v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(model).filter(model_column == v).all()


def query_latest_five(model):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(model).order_by(desc(model.date_revised)).limit(5).all()


def query_latest_five_by_asset_type(asset_type):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(Solutions).filter(Solutions.associated_asset_types.contains([asset_type])).order_by(desc(Solutions.date_revised)).limit(5)


def query_one_db(model, column, v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(model).filter(column == v).first()


def get_solution_asset_types(type_ids):
    type_names = []
    for i in type_ids:
        r = query_one_db(AssetTypes, AssetTypes.id, i)
        type_names.append(r)
    return type_names
