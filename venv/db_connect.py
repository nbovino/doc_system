from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy import extract
from sqlalchemy.orm import sessionmaker
from models import Base
import os

try:
    engine = create_engine('sqlite:///docutest.db', echo=True)
    # engine = create_engine(os.environ['LM_DB_ENGINE'])
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


def query_one_db(model, column, v):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session.query(model).filter(column == v).first()
