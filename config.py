from pecan.hooks import TransactionHook, RequestViewerHook
from ayni.hooks.cors import CorsHook
from ayni import models


# Server Specific Configurations
server = {
    'port': '8000',
    'host': '0.0.0.0'
}

# Pecan Application Configurations
app = {
    'root': 'ayni.controllers.root.RootController',
    'modules': ['ayni'],
    'default_renderer': 'json',
    'hooks': [
        TransactionHook(
            models.start,
            models.start_read_only,
            models.commit,
            models.rollback,
            models.clear
        ),
        CorsHook(),
    ],
    'debug': False,
    #'errors': {
    #    404: '/error/404',
    #    '__force_dict__': True
    #}
}

logging = {
    'loggers': {
        'root': {'level': 'INFO', 'handlers': ['console']},
        'ayni': {'level': 'DEBUG', 'handlers': ['console']},
        'pecan.commands.serve': {'level': 'DEBUG', 'handlers': ['console']},
        'py.warnings': {'handlers': ['console']},
        '__force_dict__': True
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'color'
        }
    },
    'formatters': {
        'simple': {
            'format': ('%(asctime)s %(levelname)-5.5s [%(name)s]'
                       '[%(threadName)s] %(message)s')
        },
        'color': {
            '()': 'pecan.log.ColorFormatter',
            'format': ('%(asctime)s [%(padded_color_levelname)s] [%(name)s]'
                       '[%(threadName)s] %(message)s'),
        '__force_dict__': True
        }
    }
}

sqlalchemy = {
    'url': 'sqlite:///dev.db',
    #'url': 'postgresql+psycopg2://USER:PASSWORD@DB_HOST/DB_NAME',
    'echo':          True,
    'echo_pool':     True,
    'pool_recycle':  3600,
    'encoding':      'utf-8'
}


ayni_css_file = "http://ayni.ceph.com/public/css/ayni.css"

ayni_fqdn = "http://ayni.ceph.com/"

projects = [
    {
        'name': 'ceph',
        'fqdn': 'ceph.com',
        'docs': [
            {
                'name': 'latest',
                'version': 'v0.80.5',
                'url_prefix': '/docs/',
                'prefix_regex': '~/docs/(.*)',
                'weight': 99,
                'redirect': True,
            },
            {
                'name': 'firefly',
                'version': 'v0.80.5',
                'url_prefix': '/docs/',
                'prefix_regex': '~/docs/firefly$',
                'redirect': True,
            },
            {
                'name': 'dumpling',
                'version': 'v0.67.9',
                'url_prefix': '/docs/',
                'prefix_regex': '~/docs/dumpling$',
                'redirect': True,
            },
            {
                'name': 'development',
                'version': 'master',
                'url_prefix': '/docs/',
                'redirect': False,
            },

        ]
    },
    {
        'name': 'ceph-deploy',
        'fqdn': 'ceph.com',
        'docs': [
            {
                'name': 'latest',
                'version': 'v1.5.12',
                'url_prefix': '/ceph-deploy/docs/',
                'prefix_regex': '~/ceph-deploy/docs/(.*)',
                'weight': 99,
                'redirect': True,
            },
            {
                'name': 'development',
                'version': 'master',
                'url_prefix': '/ceph-deploy/docs/',
                'redirect': False,
            },

        ]
    },
]


extra_redirect_rules = [
    ('~^wiki$',                                   'http://ceph.com/docs/'),
    ('~^wiki/$',                                  'http://ceph.com/docs/'),
    ('~^wiki/(.*)$',                              'http://ceph.com/docs/'),
    ('~^/w/(.*)$',                                'http://ceph.com/docs/'),
    ('~/docs/master/cluster-ops',                 'http:/ceph.com/docs/master/rados/operations'),
    ('~/docs/master/cluster-ops/',                'http:/ceph.com/docs/master/rados/operations/'),
    ('~/docs/master/source',                      'http://ceph.com/docs/master/install'),
    ('~/docs/master/source/',                     'http://ceph.com/docs/master/install/'),
    ('~/docs/master/source/build-prerequisites/', 'http://ceph.com/docs/master/install/build-prerequisites/'),
    ('~/docs/master/source/get-tarballs/',        'http://ceph.com/docs/master/install/get-tarballs/'),
    ('~/docs/master/source/git/',                 'http://ceph.com/docs/master/install/git/'),
    ('~/docs/master/source/clone-source/',        'http://ceph.com/docs/master/install/clone-source/'),
    ('~/docs/master/source/building-ceph/',       'http://ceph.com/docs/master/install/building-ceph/'),
    ('~/docs/master/source/build-packages/',      'http://ceph.com/docs/master/install/build-packages/'),
]
