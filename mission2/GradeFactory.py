class Grade:
    def __init__(self, name, standard_point):
        self.name = name
        self.standard = standard_point

    def is_this_grade(self, point):
        if point < self.standard:
            return False
        return True


class GradeFactory:
    def __init__(self):
        self.grades = []

    def add_grade(self, grade):
        self.grades.append(grade)
        self.grades.sort(key=lambda x: x.standard, reverse=True)

    def get_grade(self, point)->str:
        for grade in self.grades:
            if grade.is_this_grade(point):
                return grade.name

        return "ERROR"

