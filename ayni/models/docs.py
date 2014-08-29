from sqlalchemy import Column, Integer, String, ForeignKey
from ayni.models import Base


class Doc(Base):

    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)
    version = Column(String(256), nullable=False, unique=True, index=True)
    project_id = Column(Integer, ForeignKey('project.id'))
    url_prefix = Column(String(256))
    fqdn = Column(String(256))

    def __init__(self, project, version, url_prefix, fqdn=None):
        self.project = project
        self.version = version
        self.url_prefix = url_prefix
        self.fqdn = fqdn or project.fqdn

    @property
    def url(self):
        return "/%s/%s/" % (self.url_prefix, self.version)

