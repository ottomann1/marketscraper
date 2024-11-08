from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ad(Base):
    __tablename__ = 'ads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    link = Column(String, unique=True, nullable=False)
    search_term = Column(String, nullable=False)

    def __init__(self, title, price, link, search_term):
        self.title = title
        self.price = price
        self.link = link
        self.search_term = search_term

    def __repr__(self):
        return f"<Ad(title={self.title}, price={self.price}, link={self.link}, search_term={self.search_term})>"

class SearchTerm(Base):
    __tablename__ = 'search_terms'

    id = Column(Integer, primary_key=True, autoincrement=True)
    search_term = Column(String, unique=True, nullable=False)

    def __init__(self, search_term):
        self.search_term = search_term

    def __repr__(self):
        return f"<SearchTerm(search_term={self.search_term})>"
