from datetime import datetime, timedelta
import pytz, uuid

tz = pytz.timezone("Europe/Amsterdam")

def event(title, start, duration_min, location):
    uid = str(uuid.uuid4())
    start = tz.localize(start)
    end = start + timedelta(minutes=duration_min)

    return f"""BEGIN:VEVENT
UID:{uid}
DTSTART;TZID=Europe/Amsterdam:{start.strftime('%Y%m%dT%H%M%S')}
DTEND;TZID=Europe/Amsterdam:{end.strftime('%Y%m%dT%H%M%S')}
SUMMARY:{title}
LOCATION:{location}
BEGIN:VALARM
TRIGGER:-PT30M
ACTION:DISPLAY
DESCRIPTION:Reminder
END:VALARM
END:VEVENT
"""

def wrap(events):
    return "BEGIN:VCALENDAR\nVERSION:2.0\n" + "".join(events) + "END:VCALENDAR"

events = []

events.append(event(
    "TEST EVENT",
    datetime(2026,6,1,12,0),
    60,
    "Test Location"
))

with open("calendar.ics","w") as f:
    f.write(wrap(events))
