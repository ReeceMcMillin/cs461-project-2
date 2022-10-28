from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from functools import cached_property, partial
from math import exp
import sys
from typing import Any, Dict, List, Literal, Optional, Set, Tuple
from typing_extensions import Self


@dataclass
class Room:
    name: str
    capacity: int

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Room":
        return Room(**d)

    def __hash__(self) -> int:
        return hash((self.name, self.capacity))


@dataclass
class Course:
    name: str
    section: Optional[str]
    expected_enrollment: int
    preferred_instructors: Set[str]
    other_instructors: Set[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Course":
        return Course(**d)

    def __str__(self) -> str:
        return f"Course({self.name}, {self.section}, {self.expected_enrollment})"

    def __hash__(self) -> int:
        return hash((self.name, self.section, self.expected_enrollment))


@dataclass
class ScheduledCourse:
    course: Course
    instructor: str
    room: Room
    start_time: Literal[
        Literal[10],
        Literal[11],
        Literal[12],
        Literal[13],
        Literal[14],
        Literal[15],
    ]
    fitness: float = 0

    def __str__(self) -> str:
        return f"{self.course} {self.instructor} ({'pref' if self.has_preferred_instructor() else 'not pref'}) - {self.room} @ {self.start_time}:00 (fitness: {self.fitness})"

    def has_preferred_instructor(self) -> bool:
        return self.instructor in self.course.preferred_instructors

    def has_other_instructor(self) -> bool:
        return self.instructor in self.course.other_instructors

    def has_invalid_instructor(self) -> bool:
        return not (self.has_preferred_instructor() or self.has_other_instructor)

    @property
    def enrollment_capacity_ratio(self) -> float:
        return self.course.expected_enrollment / self.room.capacity

    def schedule(self) -> Tuple[Room, int]:
        return (self.room, self.start_time)

    def has_conflict_with(self, other: "ScheduledCourse") -> bool:
        if self == other:
            return False
        return self.schedule == other.schedule

    def __hash__(self) -> int:
        return hash((self.course, self.room, self.start_time))


class Schedule(List[ScheduledCourse]):
    def __lt__(self, other: Self) -> bool:
        return self.fitness() < other.fitness()

    def __gt__(self, other: Self) -> bool:
        return self.fitness() > other.fitness()

    def __eq__(self, other: Self) -> bool:
        return self.fitness() == other.fitness()

    def fitness(self):
        room_conflicts = Counter(map(lambda course: course.schedule(), self))
        instructor_conflicts = Counter(
            [(course.instructor, course.start_time) for course in self]
        )
        instructor_total_courses = Counter([course.instructor for course in self])
        parent_fitness = 0

        cs101a, cs101b = self[0], self[1]
        cs191a, cs191b = self[2], self[3]

        if cs101a.start_time == cs101b.start_time:
            parent_fitness -= 0.5
        elif abs(cs101a.start_time - cs101b.start_time) > 4:
            parent_fitness += 0.5

        if cs191a.start_time == cs191b.start_time:
            parent_fitness -= 0.5
        elif abs(cs191a.start_time - cs191b.start_time) > 4:
            parent_fitness += 0.5

        for cs101 in (cs101a, cs101b):
            for cs191 in (cs191a, cs191b):
                if abs(cs101.start_time - cs191.start_time) == 1:
                    match (cs101.room.name, cs191.room.name):
                        case ("Bloch", "Katz"):
                            parent_fitness -= 0.4
                        case ("Katz", "Bloch"):
                            parent_fitness -= 0.4
                        case _:
                            parent_fitness += 0.5

        for section in [(cs101a, cs191a), (cs101b, cs191b)]:
            match abs(section[0].start_time - section[1].start_time):
                case 0:
                    parent_fitness += 0.25
                case 2:
                    parent_fitness -= 0.25

        for course in self:
            course.fitness = 0  # reset fitness before re-evaluating
            if course.has_preferred_instructor():
                course.fitness += 0.5
            elif course.has_other_instructor():
                course.fitness += 0.2
            elif course.has_invalid_instructor():
                course.fitness -= 0.1

            if instructor_conflicts[(course.instructor, course.start_time)] > 1:
                course.fitness -= 0.2
            else:
                course.fitness += 0.2

            if instructor_total_courses[course.instructor] > 4:
                course.fitness -= 0.5
            elif (
                instructor_total_courses[course.instructor] in (1, 2)
                and course.instructor != "Xu"
            ):
                course.fitness -= 0.4

            course.fitness -= 0.5 * (room_conflicts[course.schedule()] - 1)
            if course.enrollment_capacity_ratio < 1:
                course.fitness -= 0.5
            elif course.enrollment_capacity_ratio > 6:
                course.fitness -= 0.4
            elif course.enrollment_capacity_ratio > 3:
                course.fitness -= 0.2
            else:
                course.fitness += 0.3

        return sum(course.fitness for course in self) + parent_fitness

    def __hash__(self) -> int:
        return sum(hash(course) for course in self)
