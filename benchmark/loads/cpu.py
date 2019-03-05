import math
from decimal import Decimal, getcontext


def pi(precision, verbose=False):
    def pi_archimedes(n):
        """
        Calculate n iterations of Archimedes PI recurrence relation
        """
        polygon_edge_length_squared = Decimal(2)
        polygon_sides = 2
        for k in range(n):
            polygon_edge_length_squared = 2 - 2 * (1 - polygon_edge_length_squared / 4).sqrt()
            polygon_sides *= 2
        return polygon_sides * polygon_edge_length_squared.sqrt()

    old_result = None
    for i in range(10*precision):
        # Do calculations with double precision
        getcontext().prec = 2 * precision
        result = pi_archimedes(i)
        # Print the result with single precision
        getcontext().prec = precision
        result = +result  # do the rounding on result
        if verbose:
            print("%3d: %s" % (i, result))
        if result == old_result:
            break
        old_result = result


def factorial(n):
    return math.factorial(n)


def find_primes(n):
    # Initialize a list
    primes = []
    for possiblePrime in range(2, n + 1):
        # Assume number is prime until shown it is not.
        is_prime = True
        for num in range(2, int(possiblePrime ** 0.5) + 1):
            if possiblePrime % num == 0:
                is_prime = False
                break
        if is_prime:
            primes.append(possiblePrime)

    return primes


def pidigits():
    from performance.benchmarks import bm_pidigits
    bm_pidigits.calc_ndigits(bm_pidigits.DEFAULT_DIGITS)
