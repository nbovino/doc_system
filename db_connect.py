from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy import extract
from sqlalchemy import asc, desc
from sqlalchemy.orm import sessionmaker
from models import Base, Assets, AssetTypes, Solutions
import os
import psycopg2

try:
    # engine = create_engine('sqlite:///docutest.db', echo=True)
    # engine = create_engine(os.environ["postgres://wnwyjyjotgvutc:38ed87d2070dba581e0ec605e8412bdaf5b231fa3228fd0e89d486de8218fa1b@ec2-34-197-188-147.compute-1.amazonaws.com:5432/df01j5v2r27q0f"])
    engine = psycopg2.connect("postgres://wnwyjyjotgvutc:38ed87d2070dba581e0ec605e8412bdaf5b231fa3228fd0e89d486de8218fa1b@ec2-34-197-188-147.compute-1.amazonaws.com:5432/df01j5v2r27q0f", sslmode='require')
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
    except exc.SQLAlchemyError:
        print(exc.SQLAlchemyError.__name__)


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



def query_distinct_for_models(mv, av):
    session = create_session()
    q = session.query(Assets.model).filter(Assets.manufacturer == mv). \
                              filter(Assets.asset_type == av).distinct()
    session.close()
    return q


def query_latest_five(model):
    session = create_session()
    q = session.query(model).order_by(desc(model.date_revised)).limit(5).all()
    session.close()
    return q


def query_latest_five_better(model, column, v):
    session = create_session()
    q = session.query(model).filter(column == v).limit(5)
    session.close()
    return q


# This filters with .contains. Which searches if a value is in an ARRAY data type
def query_latest_five_by_asset_type(asset_type):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(Solutions).filter(Solutions.associated_asset_types.contains([asset_type])).order_by(desc(Solutions.date_revised)).limit(5)
    session.close()
    return q


def query_by_associated_solution(solution_id):
    session = create_session()
    q = session.query(Solutions).filter(Solutions.associated_solutions.contains([solution_id])).all()
    session.close()
    return q


def query_one_db(model, column, v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    q = session.query(model).filter(column == v).first()
    session.close()
    return q


def query_latest(model):
    session = create_session()
    q = session.query(model).order_by(model.id.desc()).first()
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
