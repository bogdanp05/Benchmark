import timeit
from decimal import Decimal, getcontext


def pi(precision, verbose=False):
    def pi_archimedes(n):
        """
        Calculate n iterations of Archimedes PI recurrence relation
        """
        polygon_edge_length_squared = Decimal(2)
        polygon_sides = 2
        for i in range(n):
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


def main():
    t0 = timeit.default_timer()
    t_previous = t0
    pi(200)
    t_now = timeit.default_timer()
    print("Calculating pi took %f seconds" % (t_now - t_previous))


if __name__ == "__main__":
    main()