import requests
import perf

# from caller.main import APP_PATH
BASE_URL = 'http://127.0.0.1:'
PORT = '5000'
APP_PATH = BASE_URL + PORT + '/'


def pidigits():
    r = requests.get(APP_PATH + 'pidigits/')
    r.json()


if __name__ == "__main__":
    runner = perf.Runner(values=5)
    runner.metadata['description'] = "Compute digits of pi."
    runner.bench_func('pidigits', pidigits)
