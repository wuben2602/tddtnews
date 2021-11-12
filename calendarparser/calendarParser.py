from googleapiclient.discovery import build
from tddtnews.googleAuth import googleAuth

from datetime import datetime, timezone, timedelta

import calendar
from dataclasses import dataclass

class calendarParser():

    def __init__(self):
        
        auth = googleAuth()
        
        #Resource for interacting with API
        self.service = build('calendar', 'v3', credentials=auth.get_creds()) 

    def __convertDate(self, date):
        month = str(calendar.month_name[date.month])
        day = str(date.day)
        time = str(date.hour) + ":" + str(date.minute)
        time = str(datetime.strptime('18:30','%H:%M').strftime('%I:%M %p'))
        return month + " " + day + ", " + time

    def __get_events(self):
        minTime = datetime.now(timezone.utc).astimezone()
        maxTime = minTime + timedelta(days=30)
        return self.service.events().list(
            calendarId = "primary",
            orderBy = "startTime",
            timeMin = minTime.isoformat(),
            timeMax = maxTime.isoformat(),
            singleEvents = True
            ).execute()   
        
    def parse_events(self):
        event_list = list()
        events = self.__get_events()
        for event in events["items"]:
        
            ### get summary
            summary = event["summary"]
            if summary[:2] == "!!":
                continue
            if summary.lower() == "team practice":
                continue
            
            ### get date
            date = ''
            try:
                raw_time = event["start"]["dateTime"][:-6]
                t = datetime.strptime(raw_time, '%Y-%m-%dT%H:%M:%S')
                date = self.__convertDate(t)
            except KeyError: # all day event
                raw_time = event["start"]["date"]
                t = datetime.strptime(raw_time, "%Y-%m-%d")
                date = str(calendar.month_name[t.month]) + " " + str(t.day) + ", " + "All Day"

            ### get status
            status = 0
            for person in event["attendees"]:
                if person["responseStatus"] == "accepted":
                    status += 1
            
            #event_list.append(Event(summary, date, status)) #for debugging purposes
            event_list.append({"summary" : summary, "date" : date, "status" : status})
        return event_list
        
@dataclass
class Event(): # dataclass for pretty print debugging
    
    summary : str
    date : str
    status : int

    def __str__(self):
        retstr = ""
        retstr += self.summary + "\n"
        retstr += self.date + "\n"
        retstr += "Acceptances: " + str(self.status)
        return retstr

def main(): # tests CalendarParser
    # event_dict = dict()
    # event_list = calendarParser().parse_events()
    # for event in event_list:
    #     event_dict[event.summary[:10]] = event.__dict__
    # print(event_dict)
    
    event_list = calendarParser().parse_events()
    for event in event_list:
        print(event)
        