"""
Club Scheduling
by Alex JPS
2032-02-09
CS 211
"""
from typing import List, Set, Dict, Optional

class Student:

    def __init__(self, name: str,
                 interests: List[str]):
        self.name = name
        self.interests = interests
        self.freetimes = set([8, 9, 10, 11, 12, 13, 14, 15])
        self.meetings: List[int] = []

    def schedule_meeting(self, time: int):
        if time in self.freetimes:
            self.freetimes.remove(time)
            self.meetings.append(time)

    def __str__(self) -> str:
        return f"Student {self.name} with freetimes {self.freetimes}"

class Club:

    def __init__(self, name: str):
        self.name = name
        self.members: List[Student] = []
        self.meeting_time: Optional[int] = None

    def join(self, student: Student):
        self.members.append(student)

    def find_common_time(self) -> int:  
        common = self.members[0].freetimes
        for i in self.members:
            common = common.intersection(i.freetimes)
        return min(common)

    def schedule(self, time: int):
        self.meeting_time = time
        for i in self.members:
            i.schedule_meeting(time)

    def __str__(self) -> str:
        member_names = [member.name for member in self.members]
        return f"{self.name} ({', '.join(member_names)})"

    def __repr__(self) -> str:
        member_names = [member.name for member in self.members]
        return f"{self.name} ({', '.join(member_names)})"

class ASUO:

    def __init__(self):
        self.students: List[Student] = []
        self.clubs: List[Club] = []

    def enroll(self, s: Student):
        self.students.append(s)

    def form_clubs(self):
        clubs_to_form: Dict[str, Club] = {}
        for i in self.students:
            for j in i.interests:
                if j not in clubs_to_form:
                    clubs_to_form[j] = Club(j)
                clubs_to_form[j].join(i)
        self.clubs = clubs_to_form.values()

    def schedule_clubs(self):
        for i in self.clubs:
            common = i.find_common_time()
            i.schedule(common)
    
    def print_club_schedule(self):
        for club in self.clubs:
            if club.meeting_time is not None:
                print(f"{club} meets at {club.meeting_time}")

asuo = ASUO()
asuo.enroll(Student("Marty", ["badminton", "robotics"]))
asuo.enroll(Student("Kim", ["backgammon"]))
asuo.enroll(Student("Tara", ["robotics", "horticulture", "chess"]))
asuo.enroll(Student("George", ["chess", "badminton"]))

asuo.form_clubs()
asuo.schedule_clubs()
asuo.print_club_schedule()
