from micro import BM_SPEED

if BM_SPEED == "very fast":
    picker = 0
elif BM_SPEED == "fast":
    picker = 1
else:
    picker = 2

PI_DIGITS = [700, 1100, 1600][picker]
FLOAT_POINTS = [17500, 35000, 70000][picker]
NBODY_ITER = [3100, 6300, 13000][picker]

FIB = [26, 27, 28][picker]
JSON_LOOPS = [35, 69, 143][picker]
LIST_LOOPS = [63, 125, 250][picker]
POWERSET = [16, 17, 18][picker]
PATH_LIB_NUM_FILES = [100, 200, 400][picker]
PATH_LIB_LOOPS = [3, 4, 6][picker]

SQL_COMBINED = [3, 5, 10][picker]
SQL_WRITES = [2, 3, 7][picker]
SQL_READS = [3, 5, 11][picker]
FILE_WRITES = [170, 350, 700][picker]
FILE_READS = [1000, 2000, 3500][picker]
