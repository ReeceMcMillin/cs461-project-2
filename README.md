# Overview

This is a course assignment for an introductory AI course. I implemented a simple genetic algorithm that uses a list of incentives/penalties to randomly assign buildings and start times to a set of courses.

Some charts on convergence speed for various mutation rates live in the charts folder.

For each run:
- The worst, average, and best fitness scores for each generation are logged in [genlog.txt](genlog.txt).
- The overall schedule and its fitness are logged in [results.txt](results.txt). 

An example for each are provided in the repo.

# Sample Output

```
[11:57] pop-os:program2 (optimizing *%) | python3.10 main.py
        7.7s < Sun 30 Oct 2022 11:57:32 AM CDT
+-----------------+-------------------+---------+
| generation 000: |  2.700  |  3.593  |  7.800  |
+-----------------+-------------------+---------+
| generation 001: |  3.750  |  3.688  |  7.800  |
+-----------------+-------------------+---------+
|                      ...                      +
+-----------------+-------------------+---------+
| generation 013: |  1.900  |  3.916  |  7.850  |
+-----------------+-------------------+---------+
| generation 014: |  0.250  |  3.964  |  8.100  |
+-----------------+-------------------+---------+
| generation 015: |  1.350  |  4.094  |  8.100  |
+-----------------+-------------------+---------+
|                      ...                      +
+-----------------+-------------------+---------+
| generation 497: |  3.900  |  8.902  | 13.500  |
+-----------------+-------------------+---------+
| generation 498: |  7.200  |  8.924  | 13.500  |
+-----------------+-------------------+---------+
| generation 499: |  8.000  |  8.876  | 13.500  |
+-----------------+-------------------+---------+

CS101A (✓)   Zein el Din    Haag 301   50/75  (1.50) 14:00 (fitness:  0.80)
CS101B (✓)     Gharibi     Royall 201  50/50  (1.00) 11:00 (fitness:  0.80)
CS191A (✓)       Hare       Haag 201   50/60  (1.20) 15:00 (fitness:  0.80)
CS191B (✓)     Gladbach      FH 310   50/108  (2.16) 10:00 (fitness:  0.80)
CS201  (✓)     Gladbach     Haag 201   50/60  (1.20) 11:00 (fitness:  0.80)
CS291  (✓)     Gharibi     Bloch 119   50/60  (1.20) 12:00 (fitness:  0.80)
CS303  (✓)   Zein el Din     FH 310   60/108  (1.80) 13:00 (fitness:  0.80)
CS304  (✓)        Xu        Katz 003   25/45  (1.80) 13:00 (fitness:  0.80)
CS394  (✓)       Song        FH 216    20/30  (1.50) 13:00 (fitness:  0.80)
CS449  (✓)       Song       Haag 201   60/60  (1.00) 12:00 (fitness:  0.80)
CS451  (✓)        Xu         FH 310   100/108 (1.08) 12:00 (fitness:  0.80)

Fitness Breakdown
-----------------
+0.50: CS191A and CS191B are more than 4 hours apart.
+0.50: CS101A and CS191A are consecutive and not far apart.
+0.50: CS101B and CS191B are consecutive and not far apart.
+0.20: Gladbach teaches consecutive courses close to each other.
+0.20: Gharibi teaches consecutive courses close to each other.
+0.20: Song teaches consecutive courses close to each other.
+0.20: Xu teaches consecutive courses close to each other.
+0.20: Zein el Din teaches consecutive courses close to each other.
+2.20: From instructors without timeslot conflicts.
+8.80: Sum of the total fitness of all individual courses.
-----------------
Total fitness: 13.50
```