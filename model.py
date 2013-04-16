from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from datetime import datetime

ENGINE = None
Session = None
Base = declarative_base()

class Tweet(Base):
	__tablename__ = "tweets"

	id = Column(Integer, primary_key = True)
	from_user_id = Column(Integer)
	text = Column(String(150))
	to_user_id = Column(Integer, nullable = True)
	to_user_name = Column(String(64), nullable = True)
	in_reply_to_status_id = Column(Integer, nullable = True)
	time_stamp = Column(DateTime)

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	screen_name = Column(String(64))
	first_last_name = Column(String(256))
	profile_img_url = Column(String(500))

def connect():
	global ENGINE
	global Session
	ENGINE = create_engine("sqlite:///twerk.db", echo = False)
	Session = sessionmaker(bind=ENGINE)

	return Session()