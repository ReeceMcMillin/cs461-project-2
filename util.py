from random import choice


all_instructors = [
    "Gharibi",
    "Gladbach",
    "Hare",
    "Nait-Abdesselam",
    "Shah",
    "Song",
    "Uddin",
    "Xu",
    "Zaman",
    "Zein el Din",
]


def random_instructor() -> str:
    return choice(all_instructors)
