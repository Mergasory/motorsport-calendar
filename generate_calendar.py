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

# ---------------- MotoGP ----------------
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

for name,loc,m,d in motogp:
    events.append(event(
        f"MotoGP - {name} ({loc}) (TBC)",
        datetime(2026,m,d,14,0),
        45,
        loc
    ))

# ---------------- F1 ----------------
f1 = [
("Bahrain GP","Sakhir",3,8),
("Saudi Arabia GP","Jeddah",3,15),
("Australia GP","Melbourne",3,29),
("Japan GP","Suzuka",4,5),
("China GP","Shanghai",4,19),
("Miami GP","Miami",5,3),
("Emilia Romagna GP","Imola",5,17),
("Monaco GP","Monaco",5,24),
("Spain GP","Barcelona",6,7),
("Canada GP","Montreal",6,21),
("Austria GP","Spielberg",6,28),
("UK GP","Silverstone",7,12),
("Hungary GP","Budapest",7,26),
("Belgium GP","Spa",8,30),
("Dutch GP","Zandvoort",9,6),
("Italy GP","Monza",9,13),
("Singapore GP","Singapore",9,27),
("USA GP","Austin",10,18),
("Mexico GP","Mexico City",10,25),
("Brazil GP","Sao Paulo",11,8),
("Las Vegas GP","Las Vegas",11,21),
("Abu Dhabi GP","Abu Dhabi",12,6),
]

for name,loc,m,d in f1:
    events.append(event(
        f"F1 - {name} ({loc}) (TBC)",
        datetime(2026,m,d,15,0),
        120,
        loc
    ))

# ---------------- WEC ----------------
wec = [
("Qatar 1812km","Lusail",3,1,600),
("Imola 6H","Imola",4,19,360),
("Spa 6H","Spa",5,9,360),
("Le Mans 24H","Le Mans",6,13,1440),
("Fuji 6H","Fuji",9,20,360),
("Bahrain 8H","Bahrain",11,7,480),
]

for name,loc,m,d,dur in wec:
    events.append(event(
        f"WEC - {name} (TBC)",
        datetime(2026,m,d,13,0),
        dur,
        loc
    ))

# ---------------- DTM ----------------
dtm = [
("Hockenheim",5,2),
("Lausitzring",5,23),
("Zandvoort",6,6),
("Norisring",7,4),
("Nürburgring",8,8),
("Red Bull Ring",9,12),
("Hockenheim Finale",10,3),
]

for name,m,d in dtm:
    events.append(event(
        f"DTM - {name} - Race 1 (TBC)",
        datetime(2026,m,d,13,30),
        60,
        name
    ))
    events.append(event(
        f"DTM - {name} - Race 2 (TBC)",
        datetime(2026,m,d+1,13,30),
        60,
        name
    ))

# ---------------- WRC ----------------
wrc = [
("Monte Carlo",1,22),
("Sweden",2,12),
("Mexico",3,12),
("Croatia",4,23),
("Portugal",5,21),
("Sardinia",6,4),
("Kenya",6,25),
("Finland",7,30),
("Greece",9,10),
("Chile",10,1),
("Japan",11,12),
]

for name,m,d in wrc:
    base = datetime(2026,m,d,8,0)
    for i in range(3):
        events.append(event(
            f"WRC - {name} (Day {i+1}) (TBC)",
            base + timedelta(days=i),
            480,
            name
        ))

# ---- SAVE ----
with open("calendar.ics","w") as f:
    f.write(wrap(events))
