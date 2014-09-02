from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from ayni.models import Base
from ayni.util import normalize_fqdn


class Project(Base):

    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True, index=True)
    fqdn = Column(String(256))

    docs = relationship(
                'Doc',
                backref=backref('project'),
                cascade='all,delete',
                order_by='asc(Doc.weight)',
           )

    def __init__(self, name, fqdn):
        self.name = name
        self.fqdn = normalize_fqdn(fqdn)

    def get_doc(self, name):
        for d in self.docs:
            if d.name == name:
                return d

    def __json__(self):
        return dict(
            name=self.name,
            fqdn=self.fqdn,
            docs=self.docs,
        )

