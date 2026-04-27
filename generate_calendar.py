from datetime import datetime, timedelta
import pytz, uuid, requests

tz = pytz.timezone("Europe/Amsterdam")

def make_event(title, start, duration_min, location):
    uid = f"{title}-{start.isoformat()}"

    start = tz.localize(start)
    end = start + timedelta(minutes=duration_min)

    return {
        "uid": uid,
        "start": start,
        "ics": f"""BEGIN:VEVENT
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
    }

def wrap(events):
    return "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Motorsport Final Boss//EN\nCALSCALE:GREGORIAN\n" + "".join(e["ics"] for e in events) + "END:VCALENDAR"

events = {}
def add_event(e):
    events[e["uid"]] = e

# ================= F1 (LIVE) =================
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

        add_event(make_event(
            f"F1 - {name} ({location})",
            dt_local.replace(tzinfo=None),
            120,
            location
        ))

except:
    add_event(make_event(
        "F1 - Season (TBC)",
        datetime(2026,3,1,15,0),
        120,
        "Unknown"
    ))

# ================= MotoGP =================
motogp = [
("Qatar GP","Lusail",3,29),
("Portugal GP","Portimao",4,12),
("Americas GP","Austin",4,26),
("Spain GP","Jerez",5,3),
("France GP","Le Mans",5,17),
("Italy GP","Mugello",5,31),
("Catalunya GP","Barcelona",6,7),
("Germany GP","Sachsenring",6,21),
("Dutch GP","TT Assen",6,28),
("UK GP","Silverstone",7,12),
("Austria GP","Red Bull Ring",8,16),
("Czech GP","Brno",8,23),
("San Marino GP","Misano",9,13),
("Aragon GP","MotorLand Aragon",9,27),
("Japan GP","Motegi",10,4),
("Indonesia GP","Mandalika",10,18),
("Australia GP","Phillip Island",10,25),
("Malaysia GP","Sepang",11,1),
("Valencia GP","Valencia",11,15),
]

for name, loc, m, d in motogp:
    add_event(make_event(
        f"MotoGP - {name} ({loc}) (TBC)",
        datetime(2026, m, d, 14, 0),
        45,
        loc
    ))

# ================= WEC =================
wec = [
("Qatar 1812km","Lusail",3,1,600),
("Imola 6H","Imola",4,19,360),
("Spa 6H","Spa",5,9,360),
("24h Le Mans","Le Mans",6,13,1440),
("Fuji 6H","Fuji",9,20,360),
("Bahrain 8H","Bahrain",11,7,480),
]

for name, loc, m, d, dur in wec:
    add_event(make_event(
        f"WEC - {name} (TBC)",
        datetime(2026, m, d, 13, 0),
        dur,
        loc
    ))

# ================= DTM =================
dtm = [
("Hockenheim",5,2),
("Lausitzring",5,23),
("Zandvoort",6,6),
("Norisring",7,4),
("Nürburgring",8,8),
("Red Bull Ring",9,12),
("Hockenheim Finale",10,3),
]

for name, m, d in dtm:
    add_event(make_event(
        f"DTM - {name} - Race 1 (TBC)",
        datetime(2026, m, d, 13, 30),
        60,
        name
    ))
    add_event(make_event(
        f"DTM - {name} - Race 2 (TBC)",
        datetime(2026, m, d + 1, 13, 30),
        60,
        name
    ))

# ================= WRC =================
wrc = [
("Monte Carlo",1,22),
("Sweden",2,12),
("Mexico",3,12),
("Croatia",4,23),
("Portugal",5,21),
("Sardinia",6,4),
("Kenya Safari",6,25),
("Finland",7,30),
("Greece",9,10),
("Chile",10,1),
("Japan",11,12),
]

for name, m, d in wrc:
    base = datetime(2026, m, d, 8, 0)
    for i in range(3):
        add_event(make_event(
            f"WRC - {name} (Day {i+1}) (TBC)",
            base + timedelta(days=i),
            480,
            name
        ))

# ================= SORT =================
sorted_events = sorted(events.values(), key=lambda e: e["start"])

# ================= SAVE =================
with open("calendar.ics", "w") as f:
    f.write(wrap(sorted_events))
