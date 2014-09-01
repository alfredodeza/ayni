import os
from pecan.testing import load_test_app

import subprocess

from copy import deepcopy
from pecan import conf
from pecan import configuration
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from ayni import models as _db
import pytest


DBNAME = 'aynitest'
BIND = 'postgresql+psycopg2://localhost'


def config_file():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'config.py')


@pytest.fixture(scope='session')
def app(request):
    config = configuration.conf_from_file(config_file()).to_dict()

    # Add the appropriate connection string to the app config.
    config['sqlalchemy'] = {
        'url': '%s/%s' % (BIND, DBNAME),
        'encoding': 'utf-8',
        'poolclass': NullPool
    }

    # Set up a fake app
    app = load_test_app(config)
    return app


@pytest.fixture(scope='session')
def connection(app, request):
    """Session-wide test database."""
    # Connect and create the temporary database
    print "=" * 80
    print "CREATING TEMPORARY DATABASE FOR TESTS"
    print "=" * 80
    subprocess.call(['dropdb', DBNAME])
    subprocess.call(['createdb', DBNAME])

    # Bind and create the database tables
    _db.clear()
    engine_url = '%s/%s' % (BIND, DBNAME)

    db_engine = create_engine(
        engine_url,
        encoding='utf-8',
        poolclass=NullPool)

    # AKA models.start()
    _db.Session.bind = db_engine
    _db.metadata.bind = _db.Session.bind

    _db.Base.metadata.create_all(db_engine)
    _db.commit()
    _db.clear()

    #connection = db_engine.connect()

    def teardown():
        _db.Base.metadata.drop_all(db_engine)

    request.addfinalizer(teardown)
    return _db


@pytest.fixture(scope='function')
def session(connection, request):
    """Creates a new database session for a test."""
    _config = configuration.conf_from_file(config_file()).to_dict()
    config = deepcopy(_config)

    # Add the appropriate connection string to the app config.
    config['sqlalchemy'] = {
        'url': '%s/%s' % (BIND, DBNAME),
        'encoding': 'utf-8',
        'poolclass': NullPool
    }

    connection.start()

    def teardown():
        from sqlalchemy.engine import reflection

        # Tear down and dispose the DB binding
        connection.clear()

        # start a transaction
        engine = conf.sqlalchemy.engine
        conn = engine.connect()
        trans = conn.begin()

        inspector = reflection.Inspector.from_engine(engine)

        # gather all data first before dropping anything.
        # some DBs lock after things have been dropped in
        # a transaction.
        conn.execute("TRUNCATE TABLE %s RESTART IDENTITY CASCADE" % (
            ', '.join(inspector.get_table_names())
        ))

        trans.commit()
        conn.close()

    request.addfinalizer(teardown)
    return connection
