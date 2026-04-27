from datetime import datetime, timedelta
import pytz, uuid, requests

tz = pytz.timezone("Europe/Amsterdam")

def make_event(title, start, duration_min, location):
    uid = str(uuid.uuid4())

    start = tz.localize(start)
    end = start + timedelta(minutes=duration_min)

    return {
        "uid": uid,
        "start": start,
        "ics": f"""BEGIN:VEVENT
UID:{uid}
SEQUENCE:0
DTSTAMP:{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}
DTSTART;TZID=Europe/Amsterdam:{start.strftime('%Y%m%dT%H%M%S')}
DTEND;TZID=Europe/Amsterdam:{end.strftime('%Y%m%dT%H%M%S')}
SUMMARY:{title}
LOCATION:{location}
BEGIN:VALARM
TRIGGER:-PT30M
ACTION:DISPLAY
DESCRIPTION:Race reminder
END:VALARM
END:VEVENT
"""
    }

def wrap(events):
    return """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Motorsport Final Boss//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
""" + "".join(e["ics"] for e in events) + "END:VCALENDAR"

events = {}
def add(e):
    events[e["uid"]] = e

# ================= F1 LIVE =================
try:
    data = requests.get("https://ergast.com/api/f1/2026.json", timeout=10).json()
    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

    for race in races:
        name = race.get("raceName", "F1 Race")
        location = race.get("Circuit", {}).get("circuitName", "Unknown")
        time_str = race.get("time", "15:00:00Z")

        dt_utc = datetime.strptime(
            race["date"] + " " + time_str.replace("Z",""),
            "%Y-%m-%d %H:%M:%S"
        )
        dt_utc = pytz.utc.localize(dt_utc)
        dt_local = dt_utc.astimezone(tz)

        add(make_event(
            f"F1 - {name} ({location})",
            dt_local.replace(tzinfo=None),
            120,
            location
        ))
except:
    add(make_event("F1 - Season (TBC)", datetime(2026,3,1,15,0), 120, "Unknown"))

# ================= MotoGP =================
motogp = [
("Dutch GP","TT Assen",6,28),
("Valencia GP","Valencia",11,15),
]

for name, loc, m, d in motogp:
    add(make_event(
        f"MotoGP - {name} ({loc}) (TBC)",
        datetime(2026, m, d, 14, 0),
        45,
        loc
    ))

# ================= WEC =================
add(make_event(
    "WEC - 24h Le Mans (TBC)",
    datetime(2026,6,13,16,0),
    1440,
    "Le Mans"
))

# ================= DTM =================
add(make_event(
    "DTM - Zandvoort - Race 1 (TBC)",
    datetime(2026,6,6,13,30),
    60,
    "Zandvoort"
))
add(make_event(
    "DTM - Zandvoort - Race 2 (TBC)",
    datetime(2026,6,7,13,30),
    60,
    "Zandvoort"
))

# ================= WRC =================
add(make_event(
    "WRC - Monte Carlo (Day 1) (TBC)",
    datetime(2026,1,22,8,0),
    480,
    "Monte Carlo"
))

# ================= SORT =================
final_events = sorted(events.values(), key=lambda e: e["start"])

# ================= SAVE =================
with open("calendar.ics", "w") as f:
    f.write(wrap(final_events))
