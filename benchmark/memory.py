import timeit


def powerset(n):
    lst = list(range(0, n))
    # the power set of the empty set has one element, the empty set
    result = [[]]
    for x in lst:
        # for every additional element in our set
        # the power set consists of the subsets that don't
        # contain this element (just take the previous power set)
        # plus the subsets that do contain the element (use list
        # comprehension to add [x] onto everything in the
        # previous power set)
        result.extend([subset + [x] for subset in result])
    return result


def main():
    t0 = timeit.default_timer()
    t_previous = t0
    values = list(range(0, 20))
    powerset(20)
    t_now = timeit.default_timer()
    print("Calculating the powerset of %s took %f seconds" % (str(values), t_now - t_previous))


if __name__ == "__main__":
    main()
