import os, argparse
from jinja2 import Environment, FileSystemLoader, select_autoescape

class emailRender():

    def __init__(self, template):
        self.template_loader = Environment(
            loader=FileSystemLoader('emailcreator/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = self.template_loader.get_template(template)

    def render(self):
        print(self.template.render())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, help="name of the template to be rendered")
    args = parser.parse_args()
    emailRender(args.template + ".jinja").render()

