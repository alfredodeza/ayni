from pecan import expose, abort, request
from ayni.models import projects


class DocController(object):

    def __init__(self, name):
        self.name = name
        project_id = request.context['project_id']
        self.project = projects.Project.get(project_id)

    @expose('json')
    def index(self):
        doc = self.project.get_doc(self.name)
        if not doc:
            abort(404)
        return doc


class DocsController(object):

    @expose('json')
    def index(self):
        _id = request.context['project_id']
        project = projects.Project.get(_id)
        return project.docs

    @expose('json')
    def _lookup(self, name, *remainder):
        return DocController(name), remainder


class ProjectController(object):

    def __init__(self, project_name):
        self.project_name = project_name
        self.project = projects.Project.query.filter_by(name=project_name).first()
        if not self.project:
            abort(404)
        request.context['project_id'] = self.project.id

    @expose('json')
    def index(self):
        return self.project.docs

    docs = DocsController()


class ProjectsController(object):

    @expose('json')
    def index(self):
        project_list = projects.Project.query.all()
        return dict(projects=project_list)

    @expose()
    def _lookup(self, project_name, *remainder):
        return ProjectController(project_name), remainder
