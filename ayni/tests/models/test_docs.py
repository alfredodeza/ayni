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
        Doc(p, 'stable', 'latest', '/docs/')
        session.commit()
        result = session.app.get('/projects/foobar/docs/')
        assert result.status_int == 200
        assert len(result.json) == 1

    def test_project_has_multiple_docs(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', 'latest', '/docs/stable/')
        Doc(p, 'development', 'dev', '/docs/development/')

        session.commit()
        result = session.app.get('/projects/foobar/docs/')
        assert result.status_int == 200
        assert len(result.json) == 2


class TestDocController(object):

    def test_single_doc_version(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', 'latest', '/docs/')
        Doc(p, 'development', 'dev', '/docs/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/latest/')
        assert result.status_int == 200
        assert result.json['fqdn'] == 'http://example.com'
        assert result.json['version'] == 'latest'
        assert result.json['url_prefix'] == '/docs/'

    def test_cannot_find_doc_version(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'development', 'dev', '/docs/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/stable/', expect_errors=True)
        assert result.status_int == 404

    def test_get_full_url(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', 'latest', '/docs/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/latest/')
        assert result.status_int == 200
        assert result.json['full_url'] == 'http://example.com/docs/latest/'

    def test_get_fallback_redirect_to(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', 'latest', '/docs/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/latest/')
        assert result.json['redirect_to'] == 'http://example.com/docs/latest/'

    def test_get_end_url(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', 'latest', '/docs/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/latest/')
        assert result.status_int == 200
        assert result.json['end_url'] == '/docs/latest/'

    def test_get_redirect_to_override(self, session):
        p = Project('foobar', 'example.com')
        Doc(p, 'stable', 'latest', '/docs/', redirect_to='http://ceph.com/docs/')
        session.commit()

        result = session.app.get('/projects/foobar/docs/latest/')
        assert result.json['redirect_to'] == 'http://ceph.com/docs/'
