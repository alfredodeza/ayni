from pecan import expose
from ayni.controllers.projects import ProjectsController


class RootController(object):

    @expose('json')
    def index(self):
        return dict()

    projects = ProjectsController()
