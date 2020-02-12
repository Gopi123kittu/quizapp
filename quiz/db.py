from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from models import *

engine = create_engine('sqlite:///myexam.db', echo = True)
Session = sessionmaker(bind=engine)

session = Session()




