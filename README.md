# Benchmark
Framework for measuring the overhead of [Flask Monitoring Dashboard](https://github.com/flask-dashboard/Flask-MonitoringDashboard)
on a monitored application.


## Structure
The repository contains two applications: **benchmark** and **caller**.

### benchmark
Flask web application containing cpu, memory, and database intensive endpoints.
After executing, it returns the response times and the system probe
information.

### caller
Python application calling the defined in **benchmark** and logging and storing
the response time and system probe parameters in a database.


## How to run
There are 3 steps you have to take:

### 1. Set up the environment
Install a virtual environment with `virtualenv`:
```
virtualenv --python=python3.7 ENV
```
Activate it:
```
source ENV/bin/activate
```
Go in the root of the project and install the requirements:
```
pip install -r requirements.txt
```


### 2. Run benchmarks

**Make sure to define the hyper parameters in the `config.ini` file.**

To run the benchmarks, go in the root of the project and run:
```
make run
```


The results are saved into json files, in the `/results` folder.


### 3. Visualize results
The results are saved into json files, in the `/results` folder. There
are 2 ways of viewing them:

#### 3.1 Using the `perf` package 

From the root run:
```
python -m perf compare_to results/190308_15:25:37/-1.json results/190308_15:25:37/3.json --table
```
This will show a table similar to:
```
+---------------------+--------+------------------------------+
| Benchmark           | -1     | 3                            |
+=====================+========+==============================+
| pidigits            | 284 ms | 314 ms: 1.11x slower (+11%)  |
+---------------------+--------+------------------------------+
| float               | 255 ms | 304 ms: 1.19x slower (+19%)  |
+---------------------+--------+------------------------------+
| json_loads          | 250 ms | 291 ms: 1.16x slower (+16%)  |
+---------------------+--------+------------------------------+
| pathlib             | 235 ms | 700 ms: 2.98x slower (+198%) |
+---------------------+--------+------------------------------+
| sqlalchemy_combined | 207 ms | 589 ms: 2.84x slower (+184%) |
+---------------------+--------+------------------------------+
| sqlalchemy_writes   | 211 ms | 531 ms: 2.51x slower (+151%) |
+---------------------+--------+------------------------------+
| sqlalchemy_reads    | 208 ms | 353 ms: 1.69x slower (+69%)  |
+---------------------+--------+------------------------------+
```
Make sure to replace the files in the command above with your own.

#### 3.2 Using the `visualize` (local) package
To get plots of all the benchmarks, run:
```
python -m visualize results/190320_15:03:54 --type t
```
where `t` can be:
- `violin` for [violin plots](https://en.wikipedia.org/wiki/Violin_plot)
- `line` for line graphs
- `both`

**OR**

```
make view
```

to get violin plots of the most recent results.


## Clean up
To remove all the databases created by the benchmarks and FMD, run:
```
make clear
```

To remove all the `html` files containing the plots, run:
```
make rm_plots
```

If there's a failure, the server will not shutdown and port 5000 is unusable.
To shut down the server, run:
```
make shutdown
```


## Conduit app

In order to set up the Conduit app type the following commands from
the root of the project:
```
cd flask_conduit
export FLASK_APP=./autoapp.py
Flask db init
Flask db migrate
Flask db upgrade
```

