import cProfile
from concurrent.futures import ThreadPoolExecutor
from operator import itemgetter
from copy import copy, deepcopy
from heapq import heappushpop
import json
from random import choice, choices, randint, random
from time import process_time
from typing import List, Tuple
from model import Course, Room, Schedule, ScheduledCourse
from util import random_instructor
import pandas as pd

def random_schedule(courses: List[Course], rooms: List[Room]) -> List[ScheduledCourse]:
    return Schedule([
        ScheduledCourse(
            course,
            random_instructor(),
            choice(rooms),
            choice([10, 11, 12, 13, 14, 15]),
        )
        for course in courses
    ])
    


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

    population_size = 200
    
    generation = seed(courses, rooms, population_size)

    print(f"+{'-' * 17}+{'-' * 19}+{'-' * 9}+")
    
    fit_dict = dict()

    for i in range(200):
        parents = select_parents(generation)
        child = reproduce(*parents)
        
        # stats collection for charts :)
        average = sum(map(lambda x: x.fitness, generation)) / len(generation)
        fit_dict[i] = sorted([s.fitness for s in generation])
        worst = heappushpop(generation, child)
        
        print(
            f"| generation {i:0>3}: |{worst.fitness:^9.3f}|{average:^9.3f}|{max(parents).fitness:^9.3f}|"
        )
        print(f"+{'-' * 17}+{'-' * 19}+{'-' * 9}+")
    
        generation = mutate(generation, rooms)


    best = max(generation)

    print()
    for course in best:
        print(course)
        
    print("\nFitness Breakdown")
    print("-----------------")
    for explanation in best.explanations:
        if explanation.amount != 0:
            print(explanation)
    print("-----------------")
    print(f"Total fitness: {best.fitness:.2f}")

    df = pd.DataFrame.from_dict(fit_dict)
    import matplotlib.pyplot as plt
    df.plot.box()
    plt.savefig("charts/fit.png", format="png")

if __name__ == "__main__":
    main()
    # cProfile.run("main()", sort="time")