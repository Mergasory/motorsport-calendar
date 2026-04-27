from datetime import datetime, timedelta
import pytz, uuid, requests, traceback

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

# ---------------- LIVE F1 DATA ----------------
try:
    url = "https://ergast.com/api/f1/2026.json"
    response = requests.get(url, timeout=10)

    if response.status_code != 200:
        raise Exception("F1 API niet bereikbaar")

    data = response.json()

    races = data.get("MRData", {}).get("RaceTable", {}).get("Races", [])

    for race in races:
        name = race.get("raceName", "Unknown")
        location = race.get("Circuit", {}).get("circuitName", "Unknown")
        time_str = race.get("time", "15:00:00Z")

        dt_utc = datetime.strptime(
            race["date"] + " " + time_str.replace("Z",""),
            "%Y-%m-%d %H:%M:%S"
        )

        dt_utc = pytz.utc.localize(dt_utc)
        dt_local = dt_utc.astimezone(tz)

        events.append(event(
            f"F1 - {name} ({location})",
            dt_local.replace(tzinfo=None),
            120,
            location
        ))

except Exception:
    print("F1 ERROR:")
    traceback.print_exc()

# ---------------- MotoGP ----------------
motogp = [
("Dutch GP","TT Assen",6,28),
("Valencia GP","Valencia",11,15),
]

for name,loc,m,d in motogp:
    events.append(event(
        f"MotoGP - {name} ({loc}) (TBC)",
        datetime(2026,m,d,14,0),
        45,
        loc
    ))

# ---------------- WEC ----------------
events.append(event(
    "WEC - 24 Hours of Le Mans",
    datetime(2026,6,13,16,0),
    1440,
    "Le Mans"
))

# ---------------- DTM ----------------
events.append(event(
    "DTM - Zandvoort - Race 1 (TBC)",
    datetime(2026,6,6,13,30),
    60,
    "Zandvoort"
))

# ---------------- WRC ----------------
events.append(event(
    "WRC - Monte Carlo (Day 1) (TBC)",
    datetime(2026,1,22,8,0),
    480,
    "Monte Carlo"
))

# ---------------- SAVE ----------------
try:
    with open("calendar.ics","w") as f:
        f.write(wrap(events))
except Exception:
    print("SAVE ERROR:")
    traceback.print_exc()
