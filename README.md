# Optimizations

Python doesn't specify explicit semantics for how a lot of operations should be performed, so there's a lot of guess and check here.

1. `deepcopy`ing lists seems to be a bit faster than copying via slices.

# Sample Output

[09:44] pop-os:program2 (main *%) | python3.10 main.py
20s  Sun 30 Oct 2022 09:44:16 AM CDT

+-----------------+-------------------+---------+
+    generation   +  worst  | average |  best   +
+-----------------+-------------------+---------+
| generation 000: |  1.300  |  3.241  |  8.300  |
+-----------------+-------------------+---------+
| generation 001: |  2.400  |  3.276  |  8.300  |
+-----------------+-------------------+---------+
| generation 002: |  2.800  |  3.313  |  8.900  |
+-----------------+-------------------+---------+
+                      ...                      +
+                      ...                      +
+                      ...                      +
+-----------------+-------------------+---------+
| generation 197: | -0.000  |  7.720  | 12.500  |
+-----------------+-------------------+---------+
| generation 198: |  5.500  |  7.744  | 12.500  |
+-----------------+-------------------+---------+
| generation 199: |  5.700  |  7.792  | 12.500  |
+-----------------+-------------------+---------+

CS101A (✓)     Gharibi       FH 310   50/108  (2.16) 12:00 (fitness:  0.80)
CS101B (✓)       Hare      Royall 206  50/75  (1.50) 10:00 (fitness:  0.80)
CS191A (✓)       Hare      Royall 206  50/75  (1.50) 11:00 (fitness:  0.80)
CS191B (✓)     Gharibi     Bloch 119   50/60  (1.20) 11:00 (fitness:  0.80)
CS201  (✓)       Shah       Haag 201   50/60  (1.20) 10:00 (fitness:  0.80)
CS291  (✓)       Song       Haag 301   50/75  (1.50) 11:00 (fitness:  0.80)
CS303  (✓)   Zein el Din     FH 310   60/108  (1.80) 14:00 (fitness:  0.80)
CS304  (✓)     Gladbach    Bloch 119   25/60  (2.40) 12:00 (fitness:  0.80)
CS394  (✓)        Xu       Royall 201  20/50  (2.50) 15:00 (fitness:  0.80)
CS449  (✓)       Shah       Haag 301   60/75  (1.25) 13:00 (fitness:  0.80)
CS451  (✓)       Song        FH 310   100/108 (1.08) 10:00 (fitness:  0.80)

Fitness Breakdown
-----------------
-0.50: CS191A and CS191B share a timeslot.
+0.50: CS101A and CS191A are consecutive and not far apart.
+0.50: CS101A and CS191B are consecutive and not far apart.
+0.50: CS101B and CS191A are consecutive and not far apart.
+0.50: CS101B and CS191B are consecutive and not far apart.
+2.20: From instructors without timeslot conflicts.
+8.80: Sum of the total fitness of all individual courses.
-----------------
Total fitness: 12.50