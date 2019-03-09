from flask import Flask, render_template, json, request
import random
import os
import time

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/get_sensor_data', methods=['GET', 'POST'])
def get_sensors_data():
    f = open('last_data.json', 'r')
    s = f.read()
    f.close()

    return json.dumps(s)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', port=4000)
