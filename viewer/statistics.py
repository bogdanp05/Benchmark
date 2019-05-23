from sklearn.linear_model import LinearRegression

BASE = -1


def linear_regression(stats, bm, comparison_stats=None):
    x = [[s['mean']] for s in stats[BASE]]
    print('Linear regression results for %s' % bm)
    for k in stats.keys():
        if k == BASE:
            continue
        y = []
        for idx, dur in enumerate(stats[k]):
            y.append(dur['mean'] - stats[BASE][idx]['mean'])
        model = LinearRegression().fit(x, y)
        print("Level %s: b0: %f, b1: %f, score: %f"
              % (k, model.intercept_, model.coef_[0], model.score(x, y)))
        print("Level %s overheads(ms): %s, mean: %f" %
              (k, sorted([round(val*1000, 2) for val in y]), sum(y)/len(y)*1000))
        if comparison_stats:
            y2 = []
            for idx, dur in enumerate(comparison_stats[k]):
                y2.append(dur['mean'] - comparison_stats[BASE][idx]['mean'])
            print("Level %s comparison overheads(ms): %s, mean: %f" %
                  (k, sorted([round(val * 1000, 2) for val in y2]), sum(y2) / len(y2) * 1000))

    print()
