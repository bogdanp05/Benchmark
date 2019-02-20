from flask import Flask


app = Flask(__name__)


@app.route('/endpoint')
def endpoint3():
    return 'Ok'
