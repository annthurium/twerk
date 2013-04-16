from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from datetime import datetime

##### Global ... thingies #####
engine = create_engine("sqlite:///twerk.db", echo = False)
session = scoped_session(sessionmaker(bind=engine,
	autocommit = False, autoflush = False))

Base = declarative_base()
Base.query = session.query_property()

##### Class declarations #####
class Tweet(Base):
	__tablename__ = "tweets"

	id = Column(Integer, primary_key = True)
	from_user_id = Column(Integer)
	text = Column(String(150))
	to_user_id = Column(Integer, ForeignKey('users.id'), nullable = True)
	to_user_name = Column(String(64), nullable = True) # is this bad database design?
	in_reply_to_status_id = Column(Integer, nullable = True)
	time_stamp = Column(DateTime)
	
	user = relationship("User",
		backref=backref("tweets", order_by = id))

class User(Base):
	__tablename__ = "users"
	id = Column(Integer, primary_key = True)
	screen_name = Column(String(64))
	first_last_name = Column(String(256))
	profile_img_url = Column(String(500))


def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()