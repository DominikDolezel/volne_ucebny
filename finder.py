from edupage_api import Edupage
from edupage_api.classrooms import Classroom
from edupage_api.timetables import Timetable
from edupage_api.exceptions import BadCredentialsException
from datetime import datetime, date, timedelta
import json
from typing import Optional
from helpers import get_config, sort_func, save_to_file


class Finder:
    def __init__(self):
        self._config = get_config()
        self._edupage = Edupage()
        self.try_edupage_login()


    def try_edupage_login(self):
        """Try to log in to edupage."""
        try:
            self._edupage.login(self._config["login"], self._config["password"],
                self._config["school"])
        except BadCredentialsException:
            print("Wrong username or password!")
        except Exception as e:
            print(f"{e} Try again or open an issue!")


    def _get_timetable_for_classroom(
        self, classroom: Classroom,
        datetime: datetime) -> Optional[Timetable]:
        """Get the timetable for a classroom object."""
        return self._edupage.get_timetable(classroom, datetime)


    def _select_today_lessons(
        self, classroom_timetable: Timetable,
        datetime: datetime) -> Optional[list]:
        """Select the lessons of a classroom that are today."""
        today_lessons = []

        for lesson in classroom_timetable:
            if lesson.weekday is datetime.weekday():
                today_lessons.append(lesson)

        return today_lessons


    def _check_if_lesson_is_free(
        self, today_lessons: Optional[list], datetime) -> bool:
        """Check if there is a lesson in a classroom at a given time."""
        free = True

        for lesson in today_lessons:
            if lesson.start_time <= datetime.time() and \
                lesson.end_time >= datetime.time():
                free = False

        return free


    def _get_free_classrooms_from_edupage(
        self, datetime: datetime) -> Optional[list]:
        """Load free classrooms from eduapge."""
        classrooms = self._edupage.get_classrooms()
        free_classrooms = []

        for classroom in classrooms:
            classroom_timetable = self._get_timetable_for_classroom(
                classroom, datetime)

            today_lessons = self._select_today_lessons(
                classroom_timetable, datetime)

            if self._check_if_lesson_is_free(today_lessons, datetime):
                free_classrooms.append(classroom)

        return free_classrooms


    def _construct_times_to_check_at(self) -> list:
        """Construct the list of datetimes that will be checked."""
        times = []

        for i in range(self._config["number_of_lessons"]):
            times.append(timedelta(hours = i + self._config["hour_to_check_at"],
                minutes = self._config["minute_to_check_at"]))

        return times


    def get_today_datetime(self) -> datetime:
        """Get today as a datetime."""
        today = datetime(
            year=date.today().year,
            month=date.today().month,
            day=date.today().day
        )

        return today


    def _translate_classroom_names_to_dict(self, free_classrooms: list) -> list:
        """Translate classrooms from an edupage object to a dict."""
        free_classrooms_translated = []

        for list in free_classrooms:
            f = []
            for cl in list:
                f.append({"classroom_id": cl.classroom_id, "name": cl.name,
                    "short": cl.short})
            free_classrooms_translated.append(f)

        return free_classrooms_translated


    def _prettify_classroom_names(
        self, free_classrooms: list, n_of_floors: int) -> list:
        """Prettify the classroom names."""
        building_list = []
        for lesson in free_classrooms:
            lesson_list = []
            for floor in range(n_of_floors):
                floor_list = []
                for classroom in lesson:
                    if not classroom["classroom_id"] in self._config["bad_ids"]:
                        print(classroom["name"])
                        if classroom["name"].split(
                            self._config["split_character"])[1][0] == str(floor + 2):
                            floor_list.append(classroom)
                floor_list.sort(key=sort_func)
                lesson_list.append(floor_list)
            building_list.append(lesson_list)

        return building_list


    def get_free_classrooms(self) -> list:
        """Get the list of free classrooms for every lesson and save them to
        the data.json file.
        """
        times = self._construct_times_to_check_at()

        free_classrooms = []
        today = self.get_today_datetime()

        for time in times:
            print(today + time)
            free_classrooms.append(
                self._get_free_classrooms_from_edupage(today + time))

        print(free_classrooms)

        free_classrooms = self._translate_classroom_names_to_dict(
            free_classrooms)

        volno_jaroska = self._prettify_classroom_names(free_classrooms, 4)
        volno_pricni = self._prettify_classroom_names(free_classrooms, 3)

        print(volno_jaroska)
        print(volno_pricni)

        datadump = []
        datadump.append(volno_jaroska)
        datadump.append(volno_pricni)

        save_to_file("data.json", datadump)


if __name__ == "__main__":
    finder = Finder()
    finder.get_free_classrooms()
