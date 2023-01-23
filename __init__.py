from mycroft import MycroftSkill, intent_file_handler
from mycroft.util.parse import extract_datetime
from mycroft.util.time import default_timezone
from datetime import datetime as new_date
import caldav
import datetime
from ics import Calendar


class SiCalendarYekta(MycroftSkill):

    def log_in(self):
        
        # this is my deployement path not used currently but possible
        root = "/opt/mycroft/skills/SI-Calendar/userFiles/"
        
        """        
        # for some reason the attributes are not read from the settings file therefore i provided default values here
        self.username = self.settings.get('username', 'yk020@hdm-stuttgart.de')
        if not self.username:
           self.log.info('Failed to retrieve username')
        self.password = self.settings.get('password', 'SIPasswortyk020')
        if not self.password:
           self.log.info('Failed to retrieve password')
       """    
           
        """
        With this part you could read local files which have the username and password safed
        """
        # this file stores my nextcloud username information
        userName_file = open("/opt/mycroft/skills/SI-Calendar/userFiles/userNameFile.txt", "r")
        # this file stores my nextcloud password information as plaintext !!!
        passw_file = open("/opt/mycroft/skills/SI-Calendar/userFiles/passwFile.txt", "r")
        # extract username  and password from files (full line)
        username = userName_file.readlines()[0].rstrip("\n")
        password = passw_file.readlines()[0].rstrip("\n")
        # close both files
        userName_file.close()
        passw_file.close()

        
        
         # Create nextcloud url string
        url = "https://" + username + ":" + password + \
              "@nextcloud.humanoidlab.hdm-stuttgart.de/remote.php/dav"
        
        
        """
        # Create nextcloud url string
        url = "https://" + self.username + ":" + self.password + \
              "@nextcloud.humanoidlab.hdm-stuttgart.de/remote.php/dav"
        """      

        # open connection to calendar
        principal = caldav.DAVClient(url).principal()
        # get all available calendars (for this user)
        calendars = principal.calendars()
        # Main calender to be worked with
        main_calendar = calendars[0]
        return main_calendar

    def sort_events(self):
        # Retrieve current time
        t = datetime.datetime.now()

        # Get all events from calendar
        events_sorted = []
        for event in self.calendar.events():
            c = Calendar(event.data)
            for e in c.events:
                events_sorted.append(e)

        # Sort the events
        events_sorted.sort()
        # Extract future and todays events
        results_future = []
        results_today = []
        for event in events_sorted:
            if event.begin.date() > t.date():
                results_future.append(event)
            if event.begin.date() == t.date():
                results_today.append(event)

        return results_today, results_future

    @intent_file_handler('get.all.events.intent')
    def get_all_events(self):
        # Save extracted events in string
        collected_events = ""
        results_today, results_future = self.sort_events()

        # Get current time to filter for only upcoming events
        t = datetime.datetime.now()
        if len(results_today) != 0:
            for e in results_today:
                if e.begin.time().hour >= t.hour:
                    collected_events += f"Event '{e.name}' " \
                                        f"on {e.begin.date()}. "

        if len(results_future) != 0:
            for e in results_future:
                collected_events += f"Event '{e.name}' on {e.begin.date()}. "

        # Return dialog if upcoming events exist
        if len(collected_events) != 0:
            self.speak_dialog('get.all.events', {'events': collected_events})
        else:
            self.speak_dialog('no.events')

    @intent_file_handler('create.event.intent')
    def create_event(self, message):
        # Name of the event to be created
        name = message.data.get('name')
        # Following variables describe the date specification and duration
        extracted_datetime = extract_datetime(message.data['utterance'],
                                              new_date.now(self.timezone))[0]
        start_time = self.get_response('get.start.time')
        extracted_start_time = extract_datetime(start_time,
                                                new_date.now(self.timezone))[0]
        end_time = self.get_response('get.end.time')
        extracted_end_time = extract_datetime(end_time,
                                              new_date.now(self.timezone))[0]

        if extracted_end_time.hour >= extracted_start_time.hour:
            if extracted_end_time.hour == extracted_start_time.hour and \
                    extracted_end_time.minute <= extracted_start_time.minute:
                self.speak_dialog('create.event.cancel')
            else:
                # Save the event in calendar
                self.calendar.save_event(
                    dtstart=datetime.datetime(extracted_datetime.year,
                                              extracted_datetime.month,
                                              extracted_datetime.day,
                                              extracted_start_time.hour,
                                              extracted_start_time.minute),
                    dtend=datetime.datetime(extracted_datetime.year,
                                            extracted_datetime.month,
                                            extracted_datetime.day,
                                            extracted_end_time.hour,
                                            extracted_end_time.minute),
                    summary=name)
                # Inform user about saved events
                self.speak_dialog('create.event', {'name': name})
        else:
            self.speak_dialog('create.event.cancel')


    @intent_file_handler('get.events.on.date.intent')
    def get_events_for_date(self, message):
        # Extract specified date from input
        extracted_datetime = extract_datetime(message.data['utterance'],
                                              new_date.now(self.timezone))[0]
        # Form date string to compare against found events
        date = f"{extracted_datetime.year}-{extracted_datetime.month:02d}-" \
               f"{extracted_datetime.day:02d}"
        # Prepare string with found events
        event_str = ""
        for event in self.calendar.events():
            c = Calendar(event.data)
            for e in c.events:
                if str(e.begin.date()) == date:
                    event_str += f"\'{e.name}\' at {e.begin.time().hour}:" \
                                 f"{e.begin.time().minute:02d}."
        # Return information about (not) found events
        if len(event_str) == 0:
            self.speak_dialog('no.events.date')
        else:
            self.speak_dialog('get.events.on.date', {'events': event_str})

    @intent_file_handler('get.next.event.intent')
    def get_next_event(self):
        result = None
        # Extract future events to check against next event
        results_today, results_future = self.sort_events()

        # Retrieve current date to check for next event
        t = datetime.datetime.now()
        # Check if next event is today
        if len(results_today) != 0:
            for e in results_today:
                if e.begin.time().hour >= t.hour:
                    result = e
                else:
                    # If there is a result in today, but the time is in the past, return the next event on another day
                    if len(results_future) != 0:
                        result = results_future[0]
        else:
            # If event is not today, first next event is selected if it exists
            if len(results_future) != 0:
                result = results_future[0]
        # Feedback to user depending on result state
        if result is not None:
            # Inform user about found event
            result_str = f"\'{result.name}\' on {result.begin.date()} at " \
                         f"{result.begin.time().hour}:" \
                         f"{result.begin.time().minute:02d}."
            self.speak_dialog('get.next.event', {'event': result_str})
        else:
            self.speak_dialog('no.events')

    def search_for_event(self, target_event):
        found_event = None
        # Look for a specific event in the calendar
        for event in self.calendar.events():
            c = Calendar(event.data)
            for e in c.events:
                # Check found event against its name
                if e.name == target_event:
                    found_event = event
        return found_event

    @intent_file_handler('remove.event.intent')
    def remove_event(self, message):
        # Get name of event to be removed
        target_event = message.data.get('event')
        # Search for event
        found_event = self.search_for_event(target_event)
        if found_event is not None:
            # confirm deletion
            confirmation = self.ask_yesno('confirm.remove.ask.event.dialog')
            if confirmation == 'yes':
                # delete event if answer is 'yes'
                found_event.delete()
                self.speak_dialog('confirm.yes.remove.event',
                                  {'event': target_event})
            elif confirmation == 'no':
                # do not remove event if answer is 'no'.
                # Inform user about cancelation
                self.speak_dialog('confirm.not.remove.event.dialog')
            else:
                # give feedback if user answer was not recognized
                self.speak_dialog('could.not.understand')
        else:
            self.speak_dialog('no.events', {'event': target_event})

    @intent_file_handler('rename.event.intent')
    def rename_event(self, message):
        # Retrieve event name and new name
        target_event = message.data.get('event')
        new_name = message.data.get('new_name')
        found_event = self.search_for_event(target_event)
        if found_event is not None:
            # Rename event if it was found
            found_event.vobject_instance.vevent.summary.value = new_name
            found_event.save()
            self.speak_dialog('rename.event', {'name': new_name})
        else:
            # Inform user that event to be renamed does not exist
            self.speak_dialog('no.events')

    """
    def __init__(self):
        MycroftSkill.__init__(self)
     
    def initialize(self):
        # Log into nextcloud
        self.calendar = self.log_in()
        # Set user local timezone
        self.timezone = default_timezone()
    """    
        


def create_skill():
    return SiCalendarYekta()
