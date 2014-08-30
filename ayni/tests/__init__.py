import os
from unittest import TestCase
from pecan import set_config
from pecan.testing import load_test_app

__all__ = ['FunctionalTest']

from copy import deepcopy
import os
import subprocess

from pecan import conf
from pecan import configuration
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool

from ayni import models as amodel

__bind__ = 'postgresql+psycopg2://localhost'

def config_file():
    here = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(here, 'config.py')

class TestModel(object):

    config = configuration.conf_from_file(config_file()).to_dict()

    __db__ = None

    @classmethod
    def setup_class(cls):
        if TestModel.__db__ is None:
            TestModel.__db__ = 'pixoristtest'
            # Connect and create the temporary database
            print "=" * 80
            print "CREATING TEMPORARY DATABASE FOR TESTS"
            print "=" * 80
            #subprocess.call(['dropdb', TestModel.__db__])
            subprocess.call(['createdb', TestModel.__db__])

            # Bind and create the database tables
            amodel.clear()
            engine_url = '%s/%s' % (__bind__, TestModel.__db__)

            db_engine = create_engine(
                    engine_url,
                    encoding='utf-8',
                    poolclass=NullPool)

            # AKA models.start()
            amodel.Session.bind = db_engine
            amodel.metadata.bind = amodel.Session.bind

            amodel.Base.metadata.create_all(db_engine)
            amodel.commit()
            amodel.clear()

    def setup(self):
        config = deepcopy(self.config)

        # Add the appropriate connection string to the app config.
        config['sqlalchemy'] = {
            'url': '%s/%s' % (__bind__, TestModel.__db__),
            'encoding': 'utf-8',
            'poolclass': NullPool
        }

        # Set up a fake app
        self.app = self.load_test_app(config)
        amodel.start()
        # Not sure why petrello needed to clear here as this removes the
        # binding
        #amodel.clear()

    def load_test_app(self, config):
        return load_test_app(config)

    def teardown(self):
        from sqlalchemy.engine import reflection

        # Tear down and dispose the DB binding
        amodel.clear()

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


class FunctionalTest(TestCase):
    """
    Used for functional tests where you need to test your
    literal application and its integration with the framework.
    """

    def setUp(self):
        self.app = load_test_app(os.path.join(
            os.path.dirname(__file__),
            'config.py'
        ))

    def tearDown(self):
        set_config({}, overwrite=True)
