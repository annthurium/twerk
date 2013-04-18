##### ORM stuff lives in this module.

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import sessionmaker, relationship, backref, scoped_session
from datetime import datetime

##### engine, session are thread local

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
	from_user_screen_name = Column(String(64))
	text = Column(String(150))
	to_user_id = Column(Integer, ForeignKey('users.id'), nullable = True)
	to_user_screen_name = Column(String(64), nullable = True) # This data also lives elsewhere. Is that bad database design?
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
    """This might come in handy someday"""
    pass

if __name__ == "__main__":
    app.run(debug=True)