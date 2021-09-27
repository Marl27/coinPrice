import os
from sqlalchemy import create_engine

#DEFAULT_PATH = os.path.join(os.path.dirname(__file__), "sqlite:///foo.db")


def db_con():
    #engine = create_engine('sqlite:///Coin_price.db', echo=True)
    engine = create_engine('sqlite:////home/golu/Desktop/Github/coinPrice/Coin_price.db', echo=True)
    print("DB CREATED")
    return engine



