import icalendar
from datetime import datetime
import requests

# Uncomment to read from file
# file = "myschedule.ics"
# with open(file) as f:
#     calendar = icalendar.Calendar.from_ical(f.read())

# Uncomment to read from URL
url = input("Enter .ics URL:")
calendar = icalendar.Calendar.from_ical(requests.get(url).text)

# Set to start of pay period
periodStart = datetime.now()

# Set to specific start time
# PeriodStart = datetime(2024,2,11,0,0,0)

# Enter your wage here
pay = 17.55

hours = 0
paidHours = 0
unpaidHours = 0

for shift in calendar.walk('VEVENT'):
    start = shift.get("DTSTART").dt
    end = shift.get("DTEND").dt

    # Caps pay period to 2 weeks
    if (end.replace(tzinfo=None) - periodStart).days > 13:
        break
    periodEnd = end

    duration = (end-start).seconds/3600
    print(start," gives ",duration," hours")
    # Shifts <= 5 hours
    if duration <= 5:
        print("15 Minute break")
        print("Paid time: ",duration," hours")
        paidHours += duration
        print("Unpaid time: ",0)
    # Shifts > 5 hours and < 8 hours
    elif duration > 5 and duration < 8:
        print("45 Minute break")
        print("Paid time: ",duration-0.5," hours")
        paidHours += duration-0.5
        print("Unpaid time: 30 Minutes",)
        unpaidHours += 0.5
    # Shifts >= 8 hours
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
print(unpaidHours," hours of unpaid breaks")
