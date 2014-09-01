from ayni.models import Project


class TestProjectsController(object):

    def test_get_index_no_projects(self, session):
        result = session.app.get('/projects/')
        assert result.status_int == 200
        assert result.json == {'projects': []}

    def test_list_a_project(self, session):
        Project('foobar', 'example.com')
        session.commit()

        result = session.app.get('/projects/')
        json = result.json['projects']
        assert result.status_int == 200
        assert len(json) == 1
        assert json[0]['fqdn'] == 'example.com'
        assert json[0]['name'] == 'foobar'

    def test_list_a_couple_of_projects(self, session):
        for p in range(20):
            Project('foo_%s' % p, 'example.com')
        session.commit()

        result = session.app.get('/projects/')
        json = result.json['projects']
        assert result.status_int == 200
        assert len(json) == 20


class TestProjectController(object):

    def test_get_index_single_project(self, session):
        Project('foobar', 'example.com')
        result = session.app.get('/projects/foobar/')
        assert result.status_int == 200

    def test_get_index_no_project(self, session):
        result = session.app.get('/projects/foobar/', expect_errors=True)
        assert result.status_int == 404

    def test_get_index_single_project_data(self, session):
        Project('foobar', 'example.com')
        result = session.app.get('/projects/foobar/')
        assert result.json == []
