from heapq import heappushpop
import json
from random import choice, randint
from typing import List, Tuple
from model import Course, Room, Schedule, ScheduledCourse
from util import random_instructor


def random_schedule(courses: List[Course], rooms: List[Room]) -> List[ScheduledCourse]:
    return Schedule(
        [
            ScheduledCourse(
                course,
                random_instructor(),
                choice(rooms),
                choice([10, 11, 12, 13, 14, 15]),
            )
            for course in courses
        ]
    )


def seed(courses, rooms, n: int) -> List[Schedule]:
    return [Schedule(random_schedule(courses, rooms)) for _ in range(n)]


def select_parents(generation: List[Schedule]) -> Tuple[Schedule, Schedule]:
    first = max(generation)
    second = max(filter(lambda s: s is not max, generation), key=lambda s: s.fitness)

    return (first, second)


def reproduce(first: Schedule, second: Schedule):
    crossover = randint(0, len(first))
    return Schedule(first[:crossover] + second[crossover:])


def mutate(
    population: List[Schedule], room_list: List[Room], rate=0.005
) -> List[Schedule]:
    def mutate_inner(schedule: Schedule) -> Schedule:
        return Schedule([course.mutate(room_list, rate) for course in schedule])

    return [mutate_inner(schedule) for schedule in population]


def main():
    with open("rooms.json", "r") as f:
        rooms = list(map(Room.from_dict, json.load(f)))

    with open("courses.json", "r") as f:
        courses = list(map(Course.from_dict, json.load(f)))

    population_size = 50
    iterations = 500
    mutation_rate = 0.005

    generation = seed(courses, rooms, population_size)

    with open("genlog.txt", "w") as genlog:
        genlog.write(f"+{'-' * 16}+{'-' * 19}+{'-' * 9}+\n")
        genlog.write(
            f"|   generation   |  worst  | average |  best   |\n"
        )
        genlog.write(f"+{'-' * 16}+{'-' * 19}+{'-' * 9}+\n")
        for i in range(iterations):
            # stats collection for charts :)
            average = sum(map(lambda x: x.fitness, generation)) / len(generation)

            parents = select_parents(generation)
            child = reproduce(*parents)
            worst = heappushpop(generation, child)
            generation = mutate(generation, rooms, mutation_rate)

            genlog.write(
                f"| generation {i:0>3} |{worst.fitness:^9.3f}|{average:^9.3f}|{max(parents).fitness:^9.3f}|\n"
            )
            genlog.write(f"+{'-' * 16}+{'-' * 19}+{'-' * 9}+\n")

        best = max(generation)
        
        with open("results.txt", "w") as f:
            for course in best:
                f.write(f"{course}\n")
                print(course)

            f.write("\nFitness Breakdown\n")
            f.write("-----------------\n")
            for explanation in best.explanations:
                if explanation.amount != 0:
                    f.write(f"{explanation}\n")
            f.write("-----------------\n")
            f.write(f"Total fitness: {best.fitness:.2f}")


if __name__ == "__main__":
    main()
