"""
    Creates the database.
    For information about how to access the database via a session-variable, see: session_scope()
"""
import datetime
import random
import time
from contextlib import contextmanager

from sqlalchemy import Column, Integer, String, DateTime, create_engine, Float, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from caller import LOCATION

# TODO: change to user configurable
DB_NAME = 'sqlite:///' + LOCATION + '../benchmark_data.db'


Base = declarative_base()


class Run(Base):
    """ Table storing the response time of endpoints. """
    __tablename__ = 'Run'
    id = Column(Integer, primary_key=True)
    endpoint_name = Column(String(250), nullable=False)
    parameter = Column(Float, nullable=False)
    response_time = Column(Float, nullable=False)
    # -1 no FMD, 0-3 correspond to FMD monitor levels
    fmd_level = Column(Integer, nullable=False)
    # TODO: get this value somehow
    fmd_version = Column(String(100))
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# TODO: add a TestGroup table


# define the database
engine = create_engine(DB_NAME)
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)


@contextmanager
def session_scope():
    """
    When accessing the database, use the following syntax:
        with session_scope() as db_session:
            db_session.query(...)

    :return: the session for accessing the database
    """
    session_obj = scoped_session(DBSession)
    session = session_obj()
    try:
        yield session
        session.commit()
    except exc.OperationalError:
        session.rollback()
        time.sleep(0.5 + random.random())
        session.commit()
    except Exception as e:
        session.rollback()
        print('No commit has been made, due to the following error: {}'.format(e))
    finally:
        session.close()
