from ayni.models import projects


class TestProject(object):

    def test_create_an_object(self, session):
        project = projects.Project('foo', 'example.com')
        session.commit()
        assert project.id == 1

    def test_no_id_collitions(self, session):
        project = projects.Project('foobar', 'example.com')
        session.commit()
        assert project.id == 1
