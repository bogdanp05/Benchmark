from sklearn.linear_model import LinearRegression

BASE = -1


def linear_regression(stats, bm):
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
    print()
