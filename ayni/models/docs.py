import os
from sqlalchemy import Column, Integer, String, ForeignKey
from ayni.models import Base
from ayni.util import normalize_fqdn


class Doc(Base):

    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)
    version = Column(String(256), nullable=False, unique=True, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    url_prefix = Column(String(256))
    fqdn = Column(String(256))

    def __init__(self, project, version, url_prefix, fqdn=None):
        self.project = project
        self.version = version
        self.url_prefix = url_prefix
        self.fqdn = normalize_fqdn(fqdn) or project.fqdn

    @property
    def full_url(self):
        url = "%s%s" % (self.fqdn, self.end_url)
        return url

    @property
    def end_url(self):
        url = os.path.join(self.url_prefix, self.version)
        if not url.endswith('/'):
            return url + '/'
        return url

    def __json__(self):
        return dict(
            version=self.version,
            url_prefix=self.url_prefix,
            fqdn=self.fqdn,
            end_url=self.end_url,
            full_url=self.full_url
        )
