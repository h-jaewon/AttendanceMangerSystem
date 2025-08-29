from enum import Enum

class Grade(Enum):
    NORMAL = 0
    GOLD = 1
    SILVER = 2


class Day(Enum):
    MON = 0
    TUE = 1
    WED = 2
    THU = 3
    FRI = 4
    WEEKEND = 5

day_index_map = {
    "monday": Day.MON.value,
    "tuesday": Day.TUE.value,
    "wednesday": Day.WED.value,
    "thursday": Day.THU.value,
    "friday": Day.FRI.value,
    "saturday": Day.WEEKEND.value,
    "sunday": Day.WEEKEND.value
}
GRADE = ["NORMAL", "SILVER", "GOLD"]
player_name_id_map = {}
player_info_list = []
player_attendance_list = []

def set_player_info(player_name):
    if player_name not in player_name_id_map:
        player_name_id_map[player_name] = len(player_info_list)
        player_info_list.append({
            "name": player_name,
            "point": 0,
            "grade": Grade.NORMAL
        })
        player_attendance_list.append([0,0,0,0,0,0])


def check_attendance(player_name, attend_day):
    player_id = player_name_id_map[player_name]
    day_index = day_index_map[attend_day]
    player_attendance_list[player_id][day_index] += 1


def calc_point():
    for player_id, attendance_info in enumerate(player_attendance_list):
        player_info_list[player_id]["point"] = (attendance_info[Day.MON.value] +
                                                attendance_info[Day.TUE.value] +
                                                attendance_info[Day.WED.value]*3 +
                                                attendance_info[Day.THU.value] +
                                                attendance_info[Day.FRI.value] +
                                                attendance_info[Day.WEEKEND.value]*2
                                                )
        if attendance_info[Day.WED.value] >= 10:
            player_info_list[player_id]["point"] += 10

        if attendance_info[Day.WEEKEND.value] >= 10:
            player_info_list[player_id]["point"] += 10


def set_grade():
    for player_id, player_info in enumerate(player_info_list):
        if player_info["point"] >= 50:
            player_info["grade"] = Grade.GOLD
        elif player_info["point"] >= 30:
            player_info["grade"] = Grade.SILVER


def print_grade():
    for player_info in player_info_list:
        name = player_info["name"]
        point = player_info["point"]
        grade = GRADE[player_info["grade"].value]
        print(f"NAME : {name}, POINT : {point}, GRADE : {grade}", end="\n")


def print_removed_player():
    print("\nRemoved player")
    print("==============")
    for player_id, player_info in enumerate(player_info_list):
        if player_info["grade"] != Grade.NORMAL:
            continue
        if player_attendance_list[player_id][Day.WED.value] != 0:
            continue
        if player_attendance_list[player_id][Day.WEEKEND.value]!= 0:
            continue
        print(player_info["name"])


def input_file():
    try:
        with open("../attendance_weekday_500.txt", encoding='utf-8') as f:
            for _ in range(500):
                line = f.readline()
                if not line:
                    break
                parts = line.strip().split()
                if len(parts) == 2:
                    player_name = parts[0]
                    attend_day = parts[1]
                    set_player_info(player_name)
                    check_attendance(player_name, attend_day)

        calc_point()
        set_grade()
        print_grade()
        print_removed_player()

    except FileNotFoundError:
        print("파일을 찾을 수 없습니다.")

if __name__ == "__main__":
    input_file()