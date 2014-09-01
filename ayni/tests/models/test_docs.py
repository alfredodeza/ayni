from ayni.models import Project, Doc


class TestDocsController(object):

    def test_project_has_no_docs(self, session):
        Project('foobar', 'example.com')
        session.commit()
        result = session.app.get('/projects/foobar/docs/')
        assert result.status_int == 200
        assert result.json == []

    def test_wrong_project(self, session):
        Project('foobar', 'example.com')
        session.commit()
        result = session.app.get('/projects/baz/docs/', expect_errors=True)
        assert result.status_int == 404

    def test_project_has_single_docs(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', '/docs/')
        session.commit()
        result = session.app.get('/projects/foobar/docs/')
        assert result.status_int == 200
        assert len(result.json) == 1

    def test_project_has_multiple_docs(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', '/docs/stable/')
        Doc(p, 'development', '/docs/development/')

        session.commit()
        result = session.app.get('/projects/foobar/docs/')
        assert result.status_int == 200
        assert len(result.json) == 2


class TestDocController(object):

    def test_single_doc_version(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', '/docs/stable/')
        Doc(p, 'development', '/docs/development/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/stable/')
        assert result.status_int == 200
        assert result.json['fqdn'] == 'example.com'
        assert result.json['version'] == 'stable'
        assert result.json['url_prefix'] == '/docs/stable/'

    def test_cannot_find_doc_version(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'development', '/docs/development/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/stable/', expect_errors=True)
        assert result.status_int == 404
