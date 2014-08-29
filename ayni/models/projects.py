from sqlalchemy import Column, Integer
from ayni.models import Base


class Project(Base):

    __tablename__ = 'jobs'
    id = Column(Integer, primary_key=True)
