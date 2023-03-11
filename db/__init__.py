from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from db import models

Base = models.Base

database = os.getenv("DATABASE_NAME", default="reddit_ed")
folder_path = os.getenv("DATABASE_FOLDER", default="./")
version = os.getenv("DATABASE_VERSION", default="0.1.0")
sqlite_path = f"{os.path.join(folder_path,f'{database}_{version}')}.sqlite3"
engine = create_engine(
    f"sqlite:///{sqlite_path}",
    connect_args={"check_same_thread":False},
)

def create_db():
    """Initialize db with an engine"""
    if folder_path != "" and not os.path.exists(folder_path):
        os.makedirs(folder_path)

    Base.metadata.create_all(engine)

create_db()

def get_session():
    """Returns a new session object the current engine
    :return: sqlalchemy Session
    :rtype: session
    """
    Session = sessionmaker(bind=engine)
    return Session()

def drop_all():
    """Drop all tables in db
    :return: True if success
    :rtype: bool
    """
    Base.metadata.drop_all(engine)
    return True

def delete_db():
    """Delete db construct (sqlite file)
    :return: True if success
    :rtype: bool
    """
    os.remove(sqlite_path)
    return True

def wipe():
    """Drop all tables and delete file"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)