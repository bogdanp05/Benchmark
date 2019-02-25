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
Start the **benchmark** application and then run `main.py` from the **caller**
application. 