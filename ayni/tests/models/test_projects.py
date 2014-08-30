from ayni.models import projects
from ayni import models
from ayni.tests import TestModel


class TestProject(TestModel):

    def test_create_an_object(self):
        project = projects.Project('foo', 'example.com')
        models.commit()
