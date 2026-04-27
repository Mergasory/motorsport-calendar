from datetime import datetime, timedelta
import pytz, uuid

tz = pytz.timezone("Europe/Amsterdam")

def event(uid, title, start, duration_min, location):
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

# --- MotoGP voorbeeld ---
events.append(event(uuid.uuid4(),
    "MotoGP - Dutch GP (TT Assen) (TBC)",
    datetime(2026,6,28,14,0),
    45,
    "TT Assen"))

# --- F1 voorbeeld ---
events.append(event(uuid.uuid4(),
    "F1 - Dutch Grand Prix (Zandvoort) (TBC)",
    datetime(2026,8,30,15,0),
    120,
    "Zandvoort"))

# TODO: hier kun je later automatisch data uitbreiden

with open("calendar.ics","w") as f:
    f.write(wrap(events))
