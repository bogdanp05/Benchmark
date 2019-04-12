import os
from contextlib import contextmanager

from sqlalchemy import Column, ForeignKey, Integer, String, exc
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

"""
FMD level and location configuration
"""
FMD_LEVEL = int(os.environ["FMD_LEVEL"]) if "FMD_LEVEL" in os.environ else -1
LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'
FMD_DB = os.environ["FMD_DB"] if "FMD_DB" in os.environ else None
BM_SPEED = os.environ["BM_SPEED"] if "BM_SPEED" in os.environ else "fast"

"""
Declarative db configuration
"""
Base = declarative_base()
Base2 = declarative_base()


class Person(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person)


class Person2(Base2):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class Address2(Base2):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(Person2)


# Create an engine that stores data in the local directory's
# micro.db file.
engine = create_engine('sqlite:///micro.db')
engine2 = create_engine('sqlite://')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
Base2.metadata.create_all(engine2)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine
Base2.metadata.bind = engine2

DBSession = sessionmaker(bind=engine)
DBSession2 = sessionmaker(bind=engine2)


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
    finally:
        session.close()


@contextmanager
def session_scope2():
    """
    When accessing the database, use the following syntax:
        with session_scope() as db_session:
            db_session.query(...)

    :return: the session for accessing the database
    """
    session_obj = scoped_session(DBSession2)
    session = session_obj()
    try:
        yield session
        session.commit()
    except exc.OperationalError:
        session.rollback()
    finally:
        session.close()
