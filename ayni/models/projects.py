from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, backref
from ayni.models import Base
from ayni.models.docs import Doc


class Project(Base):

    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, unique=True, index=True)
    fqdn = Column(String(256))

    docs = relationship(
                'Doc',
                backref=backref('project'),
                cascade='all,delete',
                order_by='Doc.id',
           )

    def __init__(self, name, fqdn):
        self.name = name
        self.fqdn = fqdn

    def get_doc(self, version):
        for d in self.docs:
            if d.version == version:
                return d
