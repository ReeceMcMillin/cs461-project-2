from copy import deepcopy
import json
from random import choice, randint, random
from typing import List
from model import Course, Room, Schedule, ScheduledCourse
from util import random_instructor
import pandas as pd

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


def seed(courses, rooms, n: int):
    return [Schedule(random_schedule(courses, rooms)) for _ in range(n)]


def reproduce(first: Schedule, second: Schedule):
    crossover = randint(0, len(first))
    return Schedule(deepcopy(first[:crossover]) + deepcopy(second[crossover:]))


def mutate(
    population: List[Schedule], room_list: List[Room], rate=0.01
) -> List[Schedule]:
    new_population = deepcopy(population)
    for schedule in new_population:
        for course in schedule:
            if random() <= rate:
                # This is more of an implementation choice, I only mutate one property at a time.
                match randint(1, 3):
                    case 1:
                        course.instructor = random_instructor()
                    case 2:
                        course.room = choice(room_list)
                    case 3:
                        course.start_time = choice([10, 11, 12, 13, 14, 15])
    return new_population


if __name__ == "__main__":
    with open("rooms.json", "r") as f:
        rooms = list(map(Room.from_dict, json.load(f)))

    with open("courses.json", "r") as f:
        courses = list(map(Course.from_dict, json.load(f)))

    mutation_stats = {"rate": [], "gen": [], "fit": []}

    sample_rates = [0.001, 0.01, 0.1, 1]
    sample_rates = [0.01]

    for mutation_rate in sample_rates:

        generation = seed(courses, rooms, 200)

        print(f"+{'-' * 17}+{'-' * 19}+{'-' * 9}+")

        for i in range(500):
            parents = sorted(generation)[-2:]
            child = reproduce(*parents)

            average = sum([schedule.fitness() for schedule in generation]) / len(
                generation
            )

            worst = min(generation)
            generation.remove(worst)
            generation.append(child)
            generation = mutate(generation, rooms)

            print(
                f"| generation {i:0>3}: |{worst.fitness():^9.3f}|{average:^9.3f}|{max(parents).fitness():^9.3f}|"
            )
            print(f"+{'-' * 17}+{'-' * 19}+{'-' * 9}+")

            # stats collection for charts :)
            mutation_stats["rate"].append(mutation_rate)
            mutation_stats["gen"].append(i)
            mutation_stats["fit"].append(max(parents).fitness())

        best = max(generation)
        print(f"Final: {best.fitness()}")
        for course in best:
            print(course)

    df = pd.DataFrame.from_records(mutation_stats)

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(8, 6))
    for label, group in df.groupby("rate"):
        group.plot(x="gen", y="fit", ax=ax, label=label)
    plt.legend()
    plt.show()
    # print(sum(course.fitness for course in sorted_by_fitness[0]))
    # for course in courses:
    #     print(course)
    # seed = seed(courses, rooms, 2)

    # sample = seed[0]

    # print(sample)
