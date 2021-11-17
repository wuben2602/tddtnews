import os, argparse, json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

from calendarparser.calendarParser import calendarParser

class emailRender():

    def __init__(self, template):
        self.template_loader = Environment(
            loader=FileSystemLoader('emailcreator/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.volume = self.__getinfo("volume")
        self.number = self.__getinfo("number")
        self.template = self.template_loader.get_template(template)

    def render(self):
        images = json.load(open("assets\images.json", "r"))
        date = datetime.today().strftime("%B %d, %Y")
        events = calendarParser().parse_events()
        render = self.template.render(
            images = images,
            date = date,
            volume = self.volume,
            number = self.number,
            events_list = events
        )
        return render
            
    def __getinfo(self, key):
        with open("assets\info.json", "r") as info:
            try:
                return json.load(info)[key]
            except KeyError:
                return None

def test():
    parser = argparse.ArgumentParser()
    parser.add_argument('template', type=str, help="name of the template to be rendered")
    args = parser.parse_args()
    with open("test.html", "w") as f:
        html = emailRender(args.template + ".jinja").render()
        f.write(html)
    
