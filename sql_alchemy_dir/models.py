import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, Table, DateTime
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from .db_connect import db_con


engine = db_con()

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()


class CoinList(Base):
    __tablename__ = "coin_list"
    coin_list_id = Column(Integer)
    symbol = Column(String(10), primary_key=True)


class Coin_data(Base):
    __tablename__ = "coin_data"
    coin_data_id = Column(Integer)
    coin_list_id = Column(Integer, primary_key=True)
    symbol = Column(String(10))  # TEXT [pk, not null, unique]
    interval_id = Column(String(10), primary_key=True)  # int [pk, not null]
    open_time = Column(DateTime, primary_key=True)  # TEXT [pk, not null]
    open = Column(String(20))  # NUMERIC(18,9)
    high = Column(String(20))  # NUMERIC(18,9)
    low = Column(String(20))  # NUMERIC(18,9)
    close = Column(String(20))  # NUMERIC(18,9)
    volume = Column(String(20))  # TEXT
    close_time = Column(DateTime)  # TEXT
    created_at = Column(DateTime, default=datetime.now) #().strftime("%Y-%m-%d %H:%M:%S"))
    updated_at = Column(DateTime)
#
# class Coin_data_ta_lib(Base):
#     __tablename__ = "coin_data_ta_lib"
#     coin_data_id = Column(Integer)
#     coin_list_id = Column(Integer, primary_key=True)
#     symbol = Column(String(10))  # TEXT [pk, not null, unique]
#     interval_id = Column(String(10), primary_key=True)  # int [pk, not null]
#     open_time = Column(String(20), primary_key=True)  # TEXT [pk, not null]
#     open = Column(String(20))  # NUMERIC(18,9)
#     high = Column(String(20))  # NUMERIC(18,9)
#     low = Column(String(20))  # NUMERIC(18,9)
#     close = Column(String(20))  # NUMERIC(18,9)
#     volume = Column(String(20))  # TEXT
#     close_time = Column(String(20))  # TEXT

Base.metadata.create_all(engine)
