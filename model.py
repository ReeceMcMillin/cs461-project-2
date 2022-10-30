from collections import Counter
from dataclasses import dataclass
from functools import cached_property, total_ordering
from itertools import groupby
from random import choice, random
from typing import Any, Dict, List, Literal, Optional, Set, Tuple
from typing_extensions import Self

from util import random_instructor


@dataclass(frozen=True)
class Explanation:
    amount: float
    text: str

    def __str__(self):
        return f"{'+' if self.amount > 0 else ''}{self.amount:.2f}: {self.text}"

@dataclass(frozen=True)
class Room:
    name: str
    capacity: int

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Room":
        return Room(**d)

    def __str__(self) -> str:
        return f"{self.name} ({self.capacity})"

    def __hash__(self) -> int:
        return hash((self.name, self.capacity))


@dataclass(frozen=True)
class Course:
    name: str
    section: Optional[str]
    expected_enrollment: int
    preferred_instructors: Set[str]
    other_instructors: Set[str]

    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "Course":
        return Course(**d)  # type: ignore

    def __str__(self) -> str:
        return f"Course({self.name}, {self.section}, {self.expected_enrollment})"

    def __hash__(self) -> int:
        return hash((self.name, self.section, self.expected_enrollment))


@dataclass(frozen=True)
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

    def __str__(self) -> str:
        return f"""{str(self.course.name) + str(self.course.section or ' ')} \
({'✓' if self.has_preferred_instructor else 'X'}) {self.instructor:^16}\
{self.room.name:^10} {str(self.course.expected_enrollment) + '/' + str(self.room.capacity):^7} ({self.capacity_to_enrollment_ratio:<4.2f}) \
{self.start_time}:00 (fitness: {self.base_fitness:>5.2f})"""

    @cached_property
    def has_preferred_instructor(self) -> bool:
        return self.instructor in self.course.preferred_instructors

    @cached_property
    def has_other_instructor(self) -> bool:
        return self.instructor in self.course.other_instructors

    @cached_property
    def capacity_to_enrollment_ratio(self) -> float:
        return self.room.capacity / self.course.expected_enrollment

    @cached_property
    def room_and_time(self) -> Tuple[Room, int]:
        return (self.room, self.start_time)

    def has_conflict_with(self, other: "ScheduledCourse") -> bool:
        if self == other:
            return False
        return self.room_and_time == other.room_and_time

    def mutate(self, room_list: List[Room], rate=0.01) -> "ScheduledCourse":
        instructor = self.instructor
        room = self.room
        start_time: Literal[10, 11, 12, 13, 14, 15] = self.start_time
        if random() <= rate:
            instructor = random_instructor()
        if random() <= rate:
            room = choice(room_list)
        if random() <= rate:
            start_time = choice([10, 11, 12, 13, 14, 15])
            
        return ScheduledCourse(self.course, instructor, room, start_time)
    
    @cached_property
    def base_fitness(self) -> float:
        fitness = 0.0
        if self.has_preferred_instructor:
            fitness += 0.5
        elif self.has_other_instructor:
            fitness += 0.2
        else:
            fitness -= 0.1
            
        if self.capacity_to_enrollment_ratio < 1:
            fitness -= 0.5
        elif self.capacity_to_enrollment_ratio >= 6:
            fitness -= 0.4
        elif self.capacity_to_enrollment_ratio >= 3:
            fitness -= 0.2
        else:
            fitness += 0.3
            
        return fitness

    def __hash__(self) -> int:
        return hash((self.course, self.room, self.start_time))

@total_ordering
class Schedule(List[ScheduledCourse]):
    def __lt__(self, other: Self) -> bool:
        return self.fitness < other.fitness

    def __gt__(self, other: Self) -> bool:
        return self.fitness > other.fitness

    def __eq__(self, other: Self) -> bool:
        return self.fitness == other.fitness
    
    @cached_property
    def room_conflicts(self) -> Counter[Tuple[Room, int]]:
        return Counter(map(lambda course: course.room_and_time, self))
    
    @cached_property
    def instructor_timeslots(self) -> Counter[Tuple[str, int]]:
        return Counter([(course.instructor, course.start_time) for course in self])

    @cached_property
    def instructor_total_courses(self) -> Counter[str]:
        return Counter([course.instructor for course in self if course.instructor != "Xu"])

    @property
    def fitness(self):
        self.explanations: List[Explanation] = []
        course_specific = 0

        cs101a, cs101b = self[0], self[1]
        cs191a, cs191b = self[2], self[3]

        if cs101a.start_time == cs101b.start_time:
            course_specific -= 0.5
            self.explanations.append(Explanation(-0.5, "CS101A and CS101B share a timeslot."))
        elif abs(cs101a.start_time - cs101b.start_time) > 4:
            course_specific += 0.5
            self.explanations.append(Explanation(0.5, "CS101A and CS101B are more than 4 hours apart."))

        if cs191a.start_time == cs191b.start_time:
            course_specific -= 0.5
            self.explanations.append(Explanation(-0.5, "CS191A and CS191B share a timeslot."))
        elif abs(cs191a.start_time - cs191b.start_time) > 4:
            course_specific += 0.5
            self.explanations.append(Explanation(0.5, "CS191A and CS191B are more than 4 hours apart."))

        for cs101 in (cs101a, cs101b):
            for cs191 in (cs191a, cs191b):
                if abs(cs101.start_time - cs191.start_time) == 1:
                    match (cs101.room.name, cs191.room.name):
                        case ("Bloch", "Katz") | ("Katz", "Bloch"):
                            course_specific -= 0.4
                            self.explanations.append(Explanation(-0.4, f"{cs101.course.name}{cs101.course.section} and {cs191.course.name}{cs191.course.section} are consecutive, but on opposite ends of campus."))
                        case _:
                            course_specific += 0.5
                            self.explanations.append(Explanation(0.50, f"{cs101.course.name}{cs101.course.section} and {cs191.course.name}{cs191.course.section} are consecutive and not far apart."))

        for (cs101, cs191) in [(cs101a, cs191a), (cs101b, cs191b)]:
            section = cs101.course.section
            match abs(cs101.start_time - cs191.start_time):
                case 0:
                    course_specific -= 0.25
                    self.explanations.append(Explanation(-0.25, f"CS101{section} and CS191{section} are in the same timeslot."))
                case 2:
                    course_specific += 0.25
                    self.explanations.append(Explanation(0.25, f"CS101{section} and CS191{section} are separated by exactly one hour."))
        
        # ----------------------------------------------------------------------------------------
        # Give bonus fitness to schedules with exactly one timeslot per professor (no conflicts).
        # Penalize schedules with instructors scheduled for multiple classes in the same timeslot.
        # ----------------------------------------------------------------------------------------
        instructor_conflict_p = 0.2 * sum(filter(lambda c: c == 1, self.instructor_timeslots.values()))
        instructor_conflict_n = -0.2 * sum(map(lambda c: c - 1, self.instructor_timeslots.values()))
        self.explanations.append(Explanation(instructor_conflict_p, "From instructors without timeslot conflicts."))
        self.explanations.append(Explanation(instructor_conflict_n, f"From instructors scheduled to teach multiple courses at the same time."))
        instructor_conflict = instructor_conflict_p + instructor_conflict_n
        
        # ----------------------------------------------------------------------------------------
        # Penalize schedules with instructors scheduled to teach more than 4 courses.
        # ----------------------------------------------------------------------------------------
        too_many_courses = -0.5 * sum(map(lambda c: c > 4, self.instructor_total_courses.values()))
        self.explanations.append(Explanation(too_many_courses, "Some instructors are scheduled to teach more than 4 courses."))
        
        # ----------------------------------------------------------------------------------------
        # Penalize schedules with multiple courses scheduled in the same room at the same time.
        # ----------------------------------------------------------------------------------------
        room_conflict = -0.5 * sum(map(lambda c: c - 1, self.room_conflicts.values()))
        self.explanations.append(Explanation(room_conflict, f"Multiple courses are scheduled in the same room at the same time."))
        
        # ----------------------------------------------------------------------------------------
        # Penalize schedules with instructors only scheduled to teach 1 or 2 courses (except Xu).
        # ----------------------------------------------------------------------------------------
        limited_courses = -0.4 * sum(map(lambda c: c not in {1, 2}, self.instructor_total_courses.values()))
        self.explanations.append(Explanation(limited_courses, "Some instructors are only scheduled to teach 1 or 2 courses (Xu is exempt)."))

        course_fitness = sum(course.base_fitness for course in self)
        self.explanations.append(Explanation(course_fitness, "Sum of the total fitness of all individual courses."))
        
        return course_fitness + course_specific + instructor_conflict + limited_courses + too_many_courses + room_conflict

    def __hash__(self) -> int:
        return hash(tuple(hash(course) for course in self))
