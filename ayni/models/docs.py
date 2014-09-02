import os
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from ayni.models import Base
from ayni.util import normalize_fqdn


class Doc(Base):

    __tablename__ = 'docs'
    id = Column(Integer, primary_key=True)
    name = Column(String(256), nullable=False, index=True)
    version = Column(String(256), nullable=False, index=True)
    project_id = Column(Integer, ForeignKey('projects.id'))
    redirect = Column(Boolean(), nullable=False, default=False)
    redirect_to = Column(String(256))
    url_prefix = Column(String(256))
    prefix_regex = Column(String(256))
    fqdn = Column(String(256))
    weight = Column(Integer)

    def __init__(self, project, name, version, url_prefix,
            redirect_to=None, fqdn=None,
            redirect=False, prefix_regex=None, weight=1):
        self.project = project
        self.name = name
        self.version = version
        self.url_prefix = url_prefix
        self.prefix_regex = prefix_regex
        self.fqdn = normalize_fqdn(fqdn) or project.fqdn
        self.redirect_to = redirect_to or self.full_url
        self.redirect = redirect
        self.weight = weight

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
            name=self.name,
            prefix_regex=self.prefix_regex,
            version=self.version,
            url_prefix=self.url_prefix,
            end_url=self.end_url,
            redirect_to=self.redirect_to,
        )
