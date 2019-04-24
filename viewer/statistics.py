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
        # y = [s['mean'] for s in stats[k]]
        model = LinearRegression().fit(x, y)
        print("Monitoring level %s: b0: %f, b1: %f, score: %f"
              % (k, model.intercept_, model.coef_[0], model.score(x, y)))
    print()
