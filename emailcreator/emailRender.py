import os, argparse, json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from calendarparser.calendarParser import calendarParser, Event

class emailRender():

    def __init__(self, template):
        self.template_loader = Environment(
            loader=FileSystemLoader('emailcreator/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = self.template_loader.get_template(template)

    def render(self):
        date = datetime.today().strftime("%B %d, %Y")
        volume = self.__getinfo("volume")
        number = self.__getinfo("number")
        events = calendarParser().parse_events()
        render = self.template.render(
            volume = volume,
            number = number,
            date = date,
            events_list = events
        )
        with open("test.html", "w") as f:
            f.write(render)
            
    def __getinfo(self, key):
        with open("assets\info.json", "r") as info:
            try:
                return json.load(info)[key]
            except KeyError:
                return None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, help="name of the template to be rendered")
    args = parser.parse_args()
    emailRender(args.template + ".jinja").render()
    
