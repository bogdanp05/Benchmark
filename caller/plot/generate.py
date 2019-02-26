# import matplotlib.pyplot as plt
# plt.plot([1, 2, 3, 4])
# plt.ylabel('some numbers')
# plt.show()

from caller.database.run import get_runs
from collections import defaultdict


runs = get_runs("powerset")

loads = range(15, 23)

"""
{
    fmd_level : {
                    load : [resp_times]
                }
} 
"""
graph = defaultdict(lambda: defaultdict(list))
for r in runs:
    level = r.fmd_level
    load = r.parameter
    resp_time = r.response_time
    graph[level][load].append(resp_time)


# for level in graph.keys():
#     # x_values = graph[level].keys()
#     x_values = [22, 23]
#     y_values = []
#     for x in x_values:
#         y = sum(graph[level][x])/len(graph[level][x])
#         y_values.append(y)
#     plt.plot(x_values, y_values)

from plotly.offline import plot
import plotly.graph_objs as go

# Create random data with numpy
import numpy as np

N = 500
random_x = np.linspace(0, 1, N)
random_y = np.random.randn(N)

# Create a trace
data = []
for level in graph.keys():
    # x_values = graph[level].keys()
    x_values = [22, 23]
    y_values = []
    for x in x_values:
        y = sum(graph[level][x])/len(graph[level][x])
        y_values.append(y)
    data.append(go.Scatter(x=x_values, y=y_values))

plot(data)


