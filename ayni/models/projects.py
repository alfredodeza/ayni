from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from ayni.models import Base


class Project(Base):

    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True, index=True)
    fqdn = Column(String(256))

    docs = relationship('Doc',
                        backref=backref('project'),
                        cascade='all,delete',
                        lazy='dynamic',
                        order_by='Doc.doc_id',
                        )

    def __init__(self, name, fqdn):
        self.name = name
        self.fqdn = fqdn
