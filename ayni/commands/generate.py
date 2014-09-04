from pecan.commands.base import BaseCommand
from pecan import conf

from ayni import models
from ayni import templates
from datetime import datetime
import os
from string import Template

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

            template = map_template.format(timestamp=timestamp())
            for project in conf.projects:
                p = models.Project.query.filter_by(name=project['name']).first()
                if not p:
                    p = models.Project(name=project['name'], fqdn=project['fqdn'])
                template = template + '\n# redirects for %s\n' % p.name
                for doc in project.get('docs', []):
                    d = p.get_doc(doc['name'])
                    if not d:
                        d = models.Doc(p, **doc)

                    if doc.get('redirect'):
                        line = "{prefix} {redirect};\n".format(
                            prefix=d.prefix_regex or d.url_prefix, redirect=d.redirect_to
                        )
                        template = template + line

                # Create the JS
                here = os.path.abspath(os.path.dirname(__file__))
                top_path = os.path.abspath(os.path.dirname(os.path.dirname(here)))
                public_path = os.path.join(top_path, 'public')
                js_path = os.path.join(public_path, 'js')
                project_js = os.path.join(js_path, "%s.js" % project['name'])
                with open(project_js, 'w') as js_file:
                    project_url_part = "/projects/%s/" % project['name']
                    project_url = "%s%s" % (conf.ayni_fqdn.strip('/'), project_url_part)
                    t = Template(templates.js)
                    contents = t.substitute({
                        'ayni_css_file': conf.ayni_css_file,
                        'project_url': project_url,
                        })
                    js_file.write(contents)

            models.commit()

            with open(conf.get('map_path', 'ayni.map'), 'w') as f:
                f.write(template)

        except:
            models.rollback()
            out("ROLLING BACK... ")
            raise
        else:
            out("COMMITING... ")
            models.commit()
