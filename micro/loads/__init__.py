from micro import BM_SPEED

if BM_SPEED == "50":
    picker = 0
elif BM_SPEED == "100":
    picker = 1
elif BM_SPEED == "200":
    picker = 2
elif BM_SPEED == "500":
    picker = 3
elif BM_SPEED == "1000":
    picker = 4
elif BM_SPEED == "10":
    picker = 0
else:
    picker = 1

PI_DIGITS = [700, 1100, 1600, 2550, 3500][picker]
NBODY_ITER = [3100, 6300, 13000, 34000, 67000][picker]
FLOAT_POINTS = [17500, 35000, 70000, 140000, 280000][picker]

FIB = [26, 27, 28, 30, 31][picker]
LIST_LOOPS = [63, 125, 250, 630, 1300][picker]
JSON_LOOPS = [35, 69, 143, 360, 720][picker]
POWERSET = [16, 17, 18, 19, 20][picker]
PATH_LIB_NUM_FILES = [100, 200, 400, 600, 1][picker]
PATH_LIB_LOOPS = [3, 4, 6, 8, 1][picker]

# SQL_COMBINED = [3, 5, 10, 26, 50, 1][picker]
SQL_COMBINED = [1, 5, 10, 26, 50, 1][picker]
SQL_WRITES = [2, 3, 7, 17, 33][picker]
SQL_READS = [3, 5, 11, 28, 54][picker]
FILE_WRITES = [170, 350, 700, 1500, 3000][picker]
FILE_READS = [1000, 2000, 3500, 8000, 16000][picker]
