from edupage_api import Edupage
from datetime import datetime, date, timedelta
import json

edupage = Edupage()

try:
    edupage.login("", "", "jaroska")
except BadCredentialsException:
    print("Wrong username or password!")
except LoginDataParsingException:
    print("Try again or open an issue!")

times = []

for i in range(10):
    times.append(timedelta(hours = i + 7, minutes = 5))

free_classrooms = []
today = datetime(
    year=date.today().year,
    month=date.today().month,
    day=date.today().day
)

for time in times:
    print(today + time)
    free_classrooms.append(edupage.get_free_classrooms(today + time))

print(free_classrooms)

free_classrooms_translated = []

for list in free_classrooms:
    f = []
    for cl in list:
        f.append({"classroom_id": cl.classroom_id, "name": cl.name, "short": cl.short})
    free_classrooms_translated.append(f)

free_classrooms = free_classrooms_translated

bad_ids = [-52, -53, -54, -93, -94, -95, -96, -70, -60, -99, -98, -100, -97, -101, -2, -69, -102]

volno_jaroska = []
volno_pricni = []

def myFunc(e):
    return e["name"].split(" - ")[1]

for lesson in free_classrooms:
    lesson_list = []
    for floor in range(4):
        floor_list = []
        for classroom in lesson:
            if not classroom["classroom_id"] in bad_ids:
                print(classroom["name"])
                if classroom["name"].split(" - ")[1][0] == str(floor + 2):
                    floor_list.append(classroom)
        floor_list.sort(key=myFunc)
        lesson_list.append(floor_list)
    volno_jaroska.append(lesson_list)

for lesson in free_classrooms:
    lesson_list = []
    for floor in range(3):
        floor_list = []
        for classroom in lesson:
            if not classroom["classroom_id"] in bad_ids:
                 if classroom["name"].split(" - ")[1][1] == str(floor + 1) and \
                 classroom["name"].split(" - ")[1][0] == "P":
                    floor_list.append(classroom)
        floor_list.sort(key=myFunc)
        lesson_list.append(floor_list)
    volno_pricni.append(lesson_list)

print(volno_jaroska)
print(volno_pricni)

datadump = []
datadump.append(volno_jaroska)
datadump.append(volno_pricni)

f = open("data.json", "w")
f.write(json.dumps(datadump))
f.close()
