from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Table

Base = declarative_base()


class Url(Base):
    __tablename__ = "urls"
    long_url = Column(String)
    short_url = Column(String, primary_key=True)
    views = Column(Integer)
