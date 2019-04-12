from micro.loads import FIB


def fibonacci_bm():
    get_fib(FIB)


def get_fib(n):
    if n <= 1:
        return n
    else:
        return get_fib(n - 1) + get_fib(n - 2)
