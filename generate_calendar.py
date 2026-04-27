from datetime import datetime, timedelta
import pytz, uuid, requests

tz = pytz.timezone("Europe/Amsterdam")

def event(title, start, duration_min, location):
    uid = str(uuid.uuid4())
    start = tz.localize(start)
    end = start + timedelta(minutes=duration_min)

    return f"""BEGIN:VEVENT
UID:{uid}
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

def wrap(events):
    return "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Motorsport Calendar//EN\n" + "".join(events) + "END:VCALENDAR"

events = []
seen = set()

def safe_add(e):
    if e not in seen:
        events.append(e)
        seen.add(e)

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

        safe_add(event(
            f"F1 - {name} ({location})",
            dt_local.replace(tzinfo=None),
            120,
            location
        ))

except:
    safe_add(event(
        "F1 - Season Placeholder (TBC)",
        datetime(2026,3,1,15,0),
        120,
        "Unknown"
    ))

# ================= MotoGP =================
motogp = [
("Dutch GP","TT Assen",6,28),
("Valencia GP","Valencia",11,15),
]

for name,loc,m,d in motogp:
    safe_add(event(
        f"MotoGP - {name} ({loc}) (TBC)",
        datetime(2026,m,d,14,0),
        45,
        loc
    ))

# ================= WEC =================
safe_add(event(
    "WEC - 24 Hours of Le Mans",
    datetime(2026,6,13,16,0),
    1440,
    "Le Mans"
))

# ================= DTM =================
safe_add(event(
    "DTM - Zandvoort - Race 1 (TBC)",
    datetime(2026,6,6,13,30),
    60,
    "Zandvoort"
))
safe_add(event(
    "DTM - Zandvoort - Race 2 (TBC)",
    datetime(2026,6,7,13,30),
    60,
    "Zandvoort"
))

# ================= WRC =================
base = datetime(2026,1,22,8,0)
for i in range(3):
    safe_add(event(
        f"WRC - Monte Carlo (Day {i+1}) (TBC)",
        base + timedelta(days=i),
        480,
        "Monte Carlo"
    ))

# ================= SORT =================
def extract_start(e):
    for line in e.split("\n"):
        if line.startswith("DTSTART"):
            return line
    return ""

events.sort(key=extract_start)

# ================= SAVE =================
with open("calendar.ics","w") as f:
    f.write(wrap(events))
