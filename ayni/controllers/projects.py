from pecan import expose



class DocController(object):

    def __init__(self, version):
        self.version = version

    @expose('json')
    def index(self):
        return dict(version=self.version)


class DocsController(object):

    @expose('json')
    def index(self):
        return dict()


    @expose('json')
    def _lookup(self, version, *remainder):
        return DocController(version), remainder


class ProjectController(object):

    def __init__(self, project_name):
        self.project_name = project_name

    @expose('json')
    def index(self):
        return dict(project_name=self.project_name)

    docs = DocsController()


class ProjectsController(object):

    @expose()
    def _lookup(self, project_name, *remainder):
        return ProjectController(project_name), remainder
