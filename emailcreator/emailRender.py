import os, argparse, json
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dataclasses import dataclass

from calendarparser.calendarParser import calendarParser

class emailRender():
    
    def __init__(self, template : str):
        self.template_loader = Environment(
            loader=FileSystemLoader('emailcreator/templates/'),
            autoescape=select_autoescape(['html', 'xml'])
        )
        self.template = self.template_loader.get_template(template)
        self.news = list()
        self.update()

    def render(self):
        render = self.template.render(
            images = self.images,
            date = self.date,
            volume = self.volume,
            number = self.number,
            events_list = self.events,
            news_list = self.news
        )
        return render
    
    def add_news(self, news : str) -> bool:
        if isinstance(news, dict) and "title" in news and "content" in news:
            self.news.append(news)
            return True
        else:
            return False
    
    def remove_news(self, title : str) -> bool:
        for item in self.news:
            if item["title"] == title:
                self.news.remove(item)
                return True
        return False
    
    def update(self):
        self.events = calendarParser().parse_events()
        self.images = json.load(open("assets\images.json", "r"))
        self.date = datetime.today().strftime("%B %d, %Y")
        self.volume = self.__getinfo("volume")
        self.number = self.__getinfo("number")
        
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