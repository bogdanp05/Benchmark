import os
from contextlib import contextmanager

from sqlalchemy import Column, ForeignKey, Integer, String, exc, MetaData, Table
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker, scoped_session

"""
FMD level and location configuration
"""
FMD_LEVEL = int(os.environ["FMD_LEVEL"]) if "FMD_LEVEL" in os.environ else -1
LOCATION = os.path.abspath(os.path.dirname(__file__)) + '/'


"""
Declarative db configuration
"""
Base = declarative_base()


class PersonDeclarative(Base):
    __tablename__ = 'person'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)


class AddressDeclarative(Base):
    __tablename__ = 'address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    street_name = Column(String(250))
    street_number = Column(String(250))
    post_code = Column(String(250), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))
    person = relationship(PersonDeclarative)


# Create an engine that stores data in the local directory's
# declarative.db file.
engine_declarative = create_engine('sqlite:///declarative.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine_declarative)

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine_declarative

DBSession_declarative = sessionmaker(bind=engine_declarative)


@contextmanager
def session_scope_declarative():
    """
    When accessing the database, use the following syntax:
        with session_scope() as db_session:
            db_session.query(...)

    :return: the session for accessing the database
    """
    session_obj = scoped_session(DBSession_declarative)
    session = session_obj()
    try:
        yield session
        session.commit()
    except exc.OperationalError:
        session.rollback()
    finally:
        session.close()


"""
Imperative db configuration
"""
metadata = MetaData()

Person_imperative = Table('person', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('name', String(250), nullable=False))

Address_imperative = Table('address', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('street_name', String(250)),
                           Column('street_number', String(250)),
                           Column('post_code', String(250), nullable=False),
                           Column('person_id', Integer, ForeignKey('person.id')))

# Create an engine that stores data in the local directory's
# imperative.db file.
engine_imperative = create_engine('sqlite:///imperative.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
metadata.create_all(engine_imperative)


# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
metadata.bind = engine_imperative

DBSession_imperative = sessionmaker(bind=engine_declarative)


@contextmanager
def session_scope_imperative():
    """
    When accessing the database, use the following syntax:
        with session_scope() as db_session:
            db_session.query(...)

    :return: the session for accessing the database
    """
    session_obj = scoped_session(DBSession_imperative)
    session = session_obj()
    try:
        yield session
        session.commit()
    except exc.OperationalError:
        session.rollback()
    finally:
        session.close()
