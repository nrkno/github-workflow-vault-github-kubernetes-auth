#!/usr/bin/env python3

import traceback
from jinja2 import Template,Environment,FileSystemLoader,TemplateNotFound
import sys

objects = dict()

env = Environment(loader=FileSystemLoader(['./']))

class KlyTemplating():
    options = dict()
    def parse_options(self):
        for a in sys.argv[1:]:
            (x,y) = a.split("=",1)
            self.options[x] = y

    def generic(self):
        self.parse_options()
        body = ""
        try:
            template = env.from_string(sys.stdin.read(None))
            body = template.render(self.options)
        except TemplateNotFound as err:
            body = "Template not found\n"
        except Exception as err:
            body = ("Templating failed to render. Most likely due to an error in the template. Error transcript:\n\n%s\n----\n\n%s\n" % (err, traceback.format_exc()))
        print("%s" % body)


foo = KlyTemplating()
foo.generic()
