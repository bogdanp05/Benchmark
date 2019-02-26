from collections import defaultdict

import plotly.graph_objs as go
from plotly.offline import plot

from caller.database.run import get_runs

runs = get_runs("powerset")

loads = range(10, 15)

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


data = []
for level in graph.keys():
    x_values = list(graph[level].keys())[:4]
    y_values = []
    for x in x_values:
        y = sum(graph[level][x])/len(graph[level][x])
        y_values.append(y)
    data.append(go.Scatter(x=x_values,
                           y=y_values,
                           mode='lines+markers',
                           name='FMD level ' + str(level)))

layout = go.Layout(
    title='Average response times of the "powerset" endpoint with different FMD monitoring levels',
    xaxis=dict(
        title="load"
    ),
    yaxis=dict(
        title="response time (s)"
        # type='log'
    )
)

fig = go.Figure(data=data, layout=layout)
plot(fig)
