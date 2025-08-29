import pytest

from mission2.attendance import Attendance, Day, Player


def test_set_grade_system():
    attendance = Attendance()
    assert attendance.grade_system.get_grade(-1) == "ERROR"
    assert attendance.grade_system.get_grade(10) == "NORMAL"
    assert attendance.grade_system.get_grade(30) == "SILVER"
    assert attendance.grade_system.get_grade(50) == "GOLD"


def test_append_new_player():
    attendance = Attendance()
    before = attendance._total_player
    attendance.append_new_player("jaewon")
    assert attendance._total_player == before + 1
    assert attendance.player_name_id_map["jaewon"] == attendance._total_player-1


def test_get_player_point():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    assert player.point == 0


def test_set_player_point():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    player.point = 10
    assert player.point == 10


def test_get_player_grade():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    assert player.grade == "NORMAL"


def test_set_player_grade():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    player.grade = "PLATINUM"
    assert player.grade == "PLATINUM"

def test_get_player_name():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    assert player.name == "jaewon"

def test_save_player_attendance():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    attendance.save_player_attendance("jaewon", "monday")
    assert player.get_a_day_attendance(Day.MON) == 1
    assert player.get_weekend_attendance() == 0

    attendance.save_player_attendance("jaewon", "saturday")
    assert player.get_weekend_attendance() == 1

def test_player_count_attendance():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    player.count_attendance(0)
    assert player.get_a_day_attendance(Day.MON) == 1
    assert player.get_weekend_attendance() == 0

def test_player_defalt_grade():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    assert player.is_player_normal_grade()


def test_input_file_fail(capfd):
    attendance = Attendance()
    attendance.input_file("asbas", 100)
    out, error = capfd.readouterr()
    assert "파일을 찾을 수 없습니다." in out

def test_input_file_success(capfd):
    attendance = Attendance()
    attendance.input_file("../attendance_weekday_500.txt", 100)
    assert True

def test_calc_player_attendance_point():
    attendance = Attendance()
    attendance.append_new_player("jaewon")
    id = attendance.player_name_id_map["jaewon"]
    player = attendance._player_list[id]
    attendance.save_player_attendance("jaewon", "monday")
    assert player.get_a_day_attendance(Day.MON) == 1
    assert player.get_weekend_attendance() == 0


def test_print_removed_player_list(capfd):
    attendance = Attendance()
    attendance.removed_player_list = []
    attendance.print_removed_player_list()
    out, error = capfd.readouterr()
    assert out == ""

def test_print_removed_player_list_exist(capfd):
    attendance = Attendance()
    attendance.removed_player_list = [Player("jaewon")]
    attendance.print_removed_player_list()
    out, error = capfd.readouterr()
    assert out == "\nRemoved player\n==============\njaewon\n"


def test_run_attendance_system_and_print_result(mocker):
    attendance = Attendance()
    input_file = mocker.spy(attendance, 'input_file')
    calc_player_attendance_point = mocker.spy(attendance, 'calc_player_attendance_point')
    set_player_grade = mocker.spy(attendance, 'set_player_grade')
    set_removed_player = mocker.spy(attendance, 'set_removed_player')
    print_player_info = mocker.spy(attendance, 'print_player_info')
    print_removed_player_list = mocker.spy(attendance, 'print_removed_player_list')
    attendance.run_attendance_system_and_print_result()
    assert input_file.call_count == 1
    assert calc_player_attendance_point.call_count == 1
    assert set_player_grade.call_count == 1
    assert set_removed_player.call_count == 1
    assert print_player_info.call_count == 1
    assert print_removed_player_list.call_count == 1


