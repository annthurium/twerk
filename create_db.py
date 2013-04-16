from model import *
engine = create_engine("sqlite:///twerk.db", echo=True)
Base.metadata.create_all(engine)