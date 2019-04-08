from micro import config

FIB = 27 if config.speed == "fast" else 28


def fibonacci_bm():
    get_fib(FIB)


def get_fib(n):
    if n <= 1:
        return n
    else:
        return get_fib(n - 1) + get_fib(n - 2)
