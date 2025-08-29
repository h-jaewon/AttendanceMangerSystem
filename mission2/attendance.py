from enum import Enum
from mission2.GradeFactory import GradeFactory, Grade


class Day(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    SAT = 5
    SUN = 6


class Player:
    def __init__(self, name):
        self._name = name
        self._point = 0
        self._grade = "NORMAL"
        self.week_attend_log = [0,0,0,0,0,0,0]

    @property
    def point(self):
        return self._point

    @point.setter
    def point(self, val):
        self._point = val

    @property
    def grade(self)->str:
        return self._grade

    @grade.setter
    def grade(self, val):
        self._grade = val

    @property
    def name(self):
        return self._name

    def count_attendance(self, day_index):
        self.week_attend_log[day_index] += 1

    def get_a_day_attendance(self, day:Day):
        return self.week_attend_log[day.value]

    def get_weekend_attendance(self):
        return self.week_attend_log[Day.SAT.value] + self.week_attend_log[Day.SUN.value]

    def is_player_normal_grade(self):
        return self.grade == "NORMAL"


class Attendance:
    player_name_id_map = {}
    player_info_list = []
    player_attendance_list = []
    def __init__(self):
        self._player_list = []
        self.player_name_id_map = {}
        self._total_player = 0
        self.removed_player_list = []
        self.grade_system = GradeFactory()
        self.set_grade_system()

    def set_grade_system(self):
        self.grade_system.add_grade(Grade("NORMAL", 0))
        self.grade_system.add_grade(Grade("SILVER", 30))
        self.grade_system.add_grade(Grade("GOLD", 50))

    def append_new_player(self, player_name):
        player_id = self._total_player
        self.player_name_id_map[player_name] = player_id
        self._player_list.append(Player(player_name))
        self._total_player += 1


    def save_player_attendance(self, player_name, day):
        day_map = {
            "monday": Day.MON.value,
            "tuesday": Day.TUE.value,
            "wednesday": Day.WED.value,
            "thursday": Day.THU.value,
            "friday": Day.FRI.value,
            "saturday": Day.SAT.value,
            "sunday": Day.SUN.value
        }
        player_id = self.player_name_id_map[player_name]
        player = self._player_list[player_id]
        player.week_attend_log[day_map[day]] += 1


    def input_file(self, filename="../attendance_weekday_500.txt", read_length=500):
        try:
            with open(filename, encoding='utf-8') as f:
                for _ in range(read_length):
                    line = f.readline()
                    parts = line.strip().split()
                    player_name, attend_day = parts
                    if player_name not in self.player_name_id_map:
                        self.append_new_player(player_name)
                    self.save_player_attendance(player_name, attend_day)
        except FileNotFoundError:
            print("파일을 찾을 수 없습니다.")


    def calc_player_attendance_point(self):
        WEEK_POINT = 1
        WEEKEND_POINT = 2
        WEDNSEDAY_BONUS = 2
        SPECIAL_BONUS = 10
        for player in self._player_list:
            total_point = 0
            total_point += player.get_a_day_attendance(Day.MON) * WEEK_POINT
            total_point += player.get_a_day_attendance(Day.TUE) * WEEK_POINT
            total_point += player.get_a_day_attendance(Day.WED) * (WEEK_POINT+WEDNSEDAY_BONUS)
            total_point += player.get_a_day_attendance(Day.THU) * WEEK_POINT
            total_point += player.get_a_day_attendance(Day.FRI) * WEEK_POINT
            total_point += player.get_weekend_attendance() * WEEKEND_POINT

            if player.get_a_day_attendance(Day.WED) >= 10:
                total_point += SPECIAL_BONUS

            if player.get_weekend_attendance() >= 10:
                total_point += SPECIAL_BONUS

            player.point = total_point

    def set_player_grade(self):
        for player in self._player_list:
            player.grade = self.grade_system.get_grade(player.point)

    def print_player_info(self):
        for player in self._player_list:
            print(f"NAME : {player.name}, POINT : {player.point}, GRADE : {player.grade}", end="\n")


    def set_removed_player(self):
        self.removed_player_list = []
        for player in self._player_list:
            if not player.is_player_normal_grade():
                continue
            if player.get_a_day_attendance(Day.WED) != 0:
                continue
            if player.get_weekend_attendance() != 0:
                continue
            self.removed_player_list.append(player)


    def print_removed_player_list(self):
        if not self.removed_player_list:
            return
        print("\nRemoved player")
        print("==============")
        for player in self.removed_player_list:
            print(player.name)


    def run_attendance_system_and_print_result(self, filename="../attendance_weekday_500.txt", read_length=500):
        self.input_file(filename, read_length)
        self.calc_player_attendance_point()
        self.set_player_grade()
        self.set_removed_player()
        self.print_player_info()
        self.print_removed_player_list()
