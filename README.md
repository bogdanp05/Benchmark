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

Remove all previously created `.db` files:
```
make clear
```

To run the benchmarks, go in the root of the project and run:
```
python -m caller
```


The results are saved into json files, in the `/results` folder.


### 3. Visualize results
The results are saved into json files, in the `/results` folder. There
are 2 ways of viewing them:

#### 3.1 Using the `perf` module 

From the root run:
```
python -m perf compare_to results/190308_15:25:37/-1.json results/190308_15:25:37/3.json --table
```
This will show a table similar to:
```
+---------------------+--------+--------------------------------+
| Benchmark           | -1     | 3                              |
+=====================+========+================================+
| pidigits            | 279 ms | 315 ms: 1.13x slower (+13%)    |
+---------------------+--------+--------------------------------+
| float               | 259 ms | 304 ms: 1.17x slower (+17%)    |
+---------------------+--------+--------------------------------+
| json_loads          | 249 ms | 283 ms: 1.14x slower (+14%)    |
+---------------------+--------+--------------------------------+
| pathlib             | 636 ms | 1.85 sec: 2.91x slower (+191%) |
+---------------------+--------+--------------------------------+
| sqlalchemy_combined | 209 ms | 586 ms: 2.80x slower (+180%)   |
+---------------------+--------+--------------------------------+
| sqlalchemy_writes   | 207 ms | 499 ms: 2.41x slower (+141%)   |
+---------------------+--------+--------------------------------+
| sqlalchemy_reads    | 205 ms | 346 ms: 1.69x slower (+69%)    |
+---------------------+--------+--------------------------------+
```
Make sure to replace the files in the command above with your own.

#### 3.2 Using the `plot` (local) module

*Work in progress*


## Clean up
To remove all the databases created by the benchmarks and FMD, run:
```
make clear
```
If there's a failure, the server will not shutdown and port 5000 is unusable.
To shut down the server, run:
```
make shutdown
```

