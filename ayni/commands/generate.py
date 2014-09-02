import os
from pecan.commands.base import BaseCommand
from pecan import conf

from ayni import models
from datetime import datetime

map_template = """# this is a generated file from an Ayni app - do not edit directly.
# file was last generated on {timestamp}

"""


def out(string):
    print "==> %s" % string


def timestamp():
    return datetime.isoformat(datetime.today())


class GenerateMapCommand(BaseCommand):
    """
    Generate the Nginx redirect map from projects
    in the current application
    """

    def run(self, args):
        super(GenerateMapCommand, self).run(args)
        out("LOADING ENVIRONMENT")
        self.load_app()
        models.init_model()
        try:
            out("STARTING A TRANSACTION...")
            models.start()
            models.Project('ceph', 'ceph.com'),
            models.Project('ceph-deploy', 'ceph.com'),
            models.Project('calamari', 'ceph.com'),
            models.commit()

            ceph = models.Project.get(1)
            cephdeploy = models.Project.get(2)
            calamari = models.Project.get(3)

            models.Doc(ceph, 'catchall', 'v0.80.5', '/docs/', prefix_regex=r'~/docs/(.*)', weight=99, redirect=True)
            models.Doc(ceph, 'firefly', 'v0.80.5', '/docs/', prefix_regex=r'~/docs/firefly$', weight=2, redirect=True)
            models.Doc(ceph, 'dumpling', 'v0.67.9', '/docs/', prefix_regex=r'~/docs/dumpling$', weight=2, redirect=True)
            models.Doc(ceph, 'stable', 'v0.80.5', '/docs/', prefix_regex=r'~/docs/(latest|stable)$', redirect=True)
            models.Doc(ceph, 'development', 'master', '/docs/', prefix_regex=r'~/docs/(dev|devel|development)$', redirect=True)
            models.Doc(cephdeploy, 'stable', 'latest', '~/ceph-deploy/docs', prefix_regex=r'~/docs/ceph-deploy($|\/$)', redirect=True)
            models.Doc(cephdeploy, 'development', 'master', '~/docs/ceph-deploy/', redirect=False)

            models.commit()
            template = map_template.format(timestamp=timestamp())
            for project in models.Project.query.all():
                template = template + '\n# redirects for %s\n' % project.name
                for doc in project.docs:
                    if doc.redirect:
                        line = "{prefix} {redirect};\n".format(
                            prefix=doc.prefix_regex or doc.url_prefix, redirect=doc.redirect_to
                        )
                        template = template + line
            #here = os.path.abspath(os.path.dirname(__file__))
            with open(conf.get('map_path', 'ayni.map'), 'w') as f:
                f.write(template)


        except:
            models.rollback()
            out("ROLLING BACK... ")
            raise
        else:
            out("COMMITING... ")
            models.commit()
