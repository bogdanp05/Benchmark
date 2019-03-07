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

First, make sure to efine the hyper parameters in the `config.ini` file.

To run the benchmarks, go in the root of the project and run:
```
python -m caller
```

<!---
To generate the plots, go in the root of the project and run:
```
python -m caller.plot.generate
```
-->

The results are saved into json files, in the `/results` folder.

To compare results, from the root run:
```
python -m perf compare_to results/190305_12:35:44_-1.json results/190305_12:35:44_3.json --table
```

### 3. Visualize results
The results are saved into json files, in the `/results` folder. There
are 2 ways of viewing them:

#### 3.1 Using the `perf` module 

From the root run:
```
python -m perf compare_to results/190305_12:35:44_-1.json results/190305_12:35:44_3.json --table
```
Make sure to replace the files in the command above with your own.

#### 3.2 Using the `plot` (local) module

*Work in progress*

## Clean up
To remove all the db's created by FMD, run:
```
make clear
```
If there's a failure, the server will not shutdown and port 5000 is unusable.
To shut down the server, run:
```
make shutdown
```

