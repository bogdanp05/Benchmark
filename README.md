# Benchmark
Framework for measuring the overhead of [Flask Monitoring Dashboard](https://github.com/flask-dashboard/Flask-MonitoringDashboard)
on the monitored Flask application.



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
For this to work on Ubuntu, you need to make sure you have `gcc` and `python3.7-dev` installed. It won't work without it.


### 2. Run benchmarks

**Make sure to configure the benchmark parameters. Use the `config_micro.ini` 
and `config_macro.ini` files for the micro and macro benchmarks
respectively.**


#### 2.1. Micro benchmarks
To run the micro benchmarks, go in the root of the project and run:
```
make run_micro
```

The results are saved into json files, in the `/results/micro` folder.

#### 2.2. Macro benchmark
The macro benchmark consists of a real world Flask application, 
[Conduit](https://github.com/gothinkster/flask-realworld-example-app).
To set up the Conduit app type the following commands from
the root of the project:
```
cd macro
export FLASK_APP=./autoapp.py
Flask db init
Flask db migrate
Flask db upgrade
mv macro.db ../macro.db
```

To generate a load run from the root:

```
python -m caller --load true
``` 
This will create an SQLite db of ~63MB, named as in the config file. The db
consists of 500 users, each with 10 articles of 10KB each, 30 comments per
user, 3 tags per article, each user follows 3 other users and favorites 3
articles.


To run the macro benchmarks, go in the root of the project and run:
```
make run_macro
```

The results are saved into json files, in the `/results/macro` folder.

TODO


### 3. Visualize results
The results are saved into json files, in the `/results` folder. There
are 2 ways of viewing them:

#### 3.1 Using the `pyperf` package 

From the root run:
```
python -m pyperf compare_to results/micro/190308_15:25:37/-1.json results/micro/190308_15:25:37/3.json --table
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

#### 3.2 Using the `viewer` (local) package
To get plots of all the benchmarks, type:
```
python -m viewer --path results/micro/190415_16:25:30 --type t
```
where `t` can be:
- `violin` for [violin plots](https://en.wikipedia.org/wiki/Violin_plot)
- `line` for line graphs
- `both`

To get line charts of the overheads, give a list of results directories
to the `--path` argument, as shown below:

```
python -m viewer --path results/micro/190415_16:25:30 results/micro/190415_13:06:04
```


To get violin plots of the most recent results, type:

```
make view
```




## Clean up
To remove all the databases created by the benchmarks and FMD, run:
```
make clear
```

To remove all the `html` files containing the plots, run:
```
make free_space
```

If there's a failure, the server will not shutdown and port 5000 is unusable.
To shut down the server, run:
```
make shutdown
```


