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
    engine = create_engine(os.environ["DOC_SYSTEM"])
    print("Opened database successfully")

except Exception as e:
    print("Error during connection: ", str(e))


Base.metadata.create_all(engine)

Base.metadata.bind = engine


def create_session():
    DBSession = sessionmaker(bind=engine)
    return DBSession()


def insert_db(v):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.add(v)
        session.commit()
        session.close()
    except exc.IntegrityError:
        pass
    except:
        print('Exeption!')


def query_all(v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(v).all()
    session.close()
    return q


def query_filtered(model, model_column, v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(model).filter(model_column == v).all()
    session.close()
    return q


def query_latest_five(model):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(model).order_by(desc(model.date_revised)).limit(5).all()
    session.close()
    return q


def query_latest_five_by_asset_type(asset_type):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(Solutions).filter(Solutions.associated_asset_types.contains([asset_type])).order_by(desc(Solutions.date_revised)).limit(5)
    session.close()
    return q


def query_one_db(model, column, v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(model).filter(column == v).first()
    session.close()
    return q


def get_solution_asset_types(type_ids):
    type_names = []
    for i in type_ids:
        r = query_one_db(AssetTypes, AssetTypes.id, i)
        type_names.append(r)
    return type_names


def update_column(model, id, column, v):
    try:
        session = create_session()
        session.query(model).filter(model.id == id).update({column: v})
        session.commit()
        session.close()
    except exc.IntegrityError:
        print("Error")


def update_assoc_asset_types(sid, values):
    try:
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        session.query(Solutions).filter(Solutions.id == sid).update({Solutions.associated_asset_types: values})
        session.commit()
        session.close()
    except exc.IntegrityError:
        print("Integrity Error!!!!!!!!!!!!!!!!!!!!!!!!!!")
