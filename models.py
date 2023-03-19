from sqlalchemy import Column, Integer, String, DateTime, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:r3l0ATprogef3w_+@127.0.0.1:5432/flask_project')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class Advert(Base):
    __tablename__ = 'advertisements'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    user_name = Column(String, nullable=False)


Base.metadata.create_all(engine)
