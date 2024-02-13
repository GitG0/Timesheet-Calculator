import icalendar
from datetime import datetime
import requests

file = "myschedule.ics"
with open(file) as f:
    calendar = icalendar.Calendar.from_ical(f.read())

# url = input("Enter .ics URL:")
# calendar = icalendar.Calendar.from_ical(requests.get(url).text)

hours = 0
paidHours = 0
unpaidHours = 0
pay = 17.55
# periodStart = datetime.now()
periodStart = datetime(2024,2,11,0,0,0)

for shift in calendar.walk('VEVENT'):
    start = shift.get("DTSTART").dt
    end = shift.get("DTEND").dt

    if (end.replace(tzinfo=None) - periodStart).days > 13:
        break
    periodEnd = end

    duration = (end-start).seconds/3600
    print(start," gives ",duration," hours")
    if duration <= 5:
        print("15 Minute break")
        print("Paid time: ",duration," hours")
        paidHours += duration
        print("Unpaid time: ",0)
    elif duration > 5 and duration < 8:
        print("45 Minute break")
        print("Paid time: ",duration-0.5," hours")
        paidHours += duration-0.5
        print("Unpaid time: 30 Minutes",)
        unpaidHours += 0.5
    else:
        print("1 Hour break")
        print("Paid time: ",duration-0.5," hours")
        paidHours += duration-0.5
        print("Unpaid time: 30 Minutes")
        unpaidHours += 0.5
    hours += duration
    print("---------------------------------")

print(hours," hours between ",str(periodStart)[:10]," -> ",str(periodEnd)[:10])
print(paidHours," hours paid = ",round(hours*pay,2))
print(unpaidHours," break hours")
