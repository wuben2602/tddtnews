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
        time = str(datetime.strptime(time,'%H:%M').strftime('%I:%M %p'))
        return month + " " + day + ", " + time

    def __get_events(self, days=60):
        minTime = datetime.now(timezone.utc).astimezone()
        maxTime = minTime + timedelta(days=days)
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
            if summary.lower() == "team practice" or summary.lower() == "tddt practice":
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
                
            ### get people
            people = 0
            for person in event["attendees"]:
                if person["responseStatus"] == "accepted":
                    people += 1
                    
            ### get status
            if "description" in event and ("Confirmed" in event["description"] or "CONFIRMED" in event["description"]):
                status = True
            elif people >= 5:
                status = True
            else:
                status = False

            event_list.append(
                {"summary" : summary,
                 "date" : date,
                 "people" : people,
                 "status" : status, 
                 "link" : event["htmlLink"]
                 })
            
        return event_list

def test():
    event_list = calendarParser().parse_events()
    for event in event_list:
        print(event)