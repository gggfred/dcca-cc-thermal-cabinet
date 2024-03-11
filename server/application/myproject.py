from flask import Flask, request
import json

import calendar
import time

from controller import Controller
import dbapi

import logging
import logging.handlers

my_logger = logging.getLogger('myproject')
my_logger.setLevel(logging.DEBUG)

handler = logging.handlers.SysLogHandler(address = '/dev/log')
my_logger.addHandler(handler)

control = Controller()

def getRemoteIp(request):
    if request.headers.getlist("X-Forwarded-For"):
        return request.headers.getlist("X-Forwarded-For")[0]
    else:
        return request.remote_addr

def processData(data, command):
    if command == "door":
        pCmd = data.get('state')

        if not pCmd:
            ans = {'status':'error', 'message' : 'missing data'}
            code = 400
            return ans, code

        res = control.setDoorState(pCmd)

        if res == False:
            ans = {'status':'error', 'message' : 'state error, it must be open/closed'}
            code = 400
            return json.dumps(ans), code

        ans = {'status':'ok'}
        code = 200
    elif command == 'temperature':
        pCmd = data.get('temperature')

        if not pCmd:
            ans = {'status':'error', 'message' : 'missing data'}
            code = 400
            return ans, code

        control.setTemperature(float(pCmd))
        dbapi.postMeasure(data)

        ans = {'status':'ok'}
        code = 200
    elif command == 'history':
        pCmd = data.get('qty')
        measurements = dbapi.getHistory(pCmd)
        my_logger.debug(f"myproject: {measurements}")
        ans = {'status' : 'ok', 'measurements' : measurements}
        code = 200
    else:
        ans = {'status':'error', 'message' : 'missing command'}
        code = 400

    return ans, code

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1 style='color:blue'>Hello There!</h1>"


@app.route("/epoch", methods = ['GET'] )
def getEpoch():
    ip = getRemoteIp(request)

    try:
        epoch = calendar.timegm(time.gmtime())

        my_logger.debug(f"ip {ip}, epoch {epoch}")

        return json.dumps({'status':'ok','epoch': epoch}), 200

    except Exception as e:
        return json.dumps({'status':'error','message': str(e)}), 400


@app.route("/heater", methods = ['GET'] )
def heater():
    ip = getRemoteIp(request)

    try:
        epoch = calendar.timegm(time.gmtime())

        my_logger.debug(f"ip {ip}, epoch {epoch}")

        return json.dumps({'status':'ok','epoch': epoch}), 200

    except Exception as e:
        return json.dumps({'status':'error','message': str(e)}), 400


@app.route("/door", methods = ['GET', 'POST'] )
def door():
    ip = getRemoteIp(request)

    try:
        if request.method == "GET":
            ans = {'state': control._door}
            code = 200
        elif request.method == "POST":
            data = request.get_json()

            my_logger.debug(f"ip {ip}, data: {json.dumps(data)}")
            ans, code = processData(data, 'door')

        return json.dumps(ans), code
    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        return json.dumps({'status':'error','message': str(e)}), 400


@app.route("/measurement", methods = ['GET','POST'] )
def measurement():
    ip = getRemoteIp(request)

    try:
        data = request.get_json()

        if request.method == "GET":
            ans = {'temperature' : control.getTemperature()}
            code = 200
        elif request.method == "POST":
            my_logger.debug("ip %s, data: %s",ip, json.dumps(data))
            ans, code = processData(data, 'temperature')

        my_logger.debug(f"myproject: answer: {ans}, code: {code}")

        return json.dumps(ans), code

    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        return json.dumps({'status':'error','message': str(e)}), 400


@app.route("/history", methods = ['GET'] )
def history():
    ip = getRemoteIp(request)

    try:
        data = request.get_json()

        my_logger.debug(f"ip {ip}, data: {json.dumps(data)}")

        ans, code = processData(data, 'history')

        return json.dumps(ans), code
    except Exception as e:
        # Handle any exceptions (e.g., invalid JSON format)
        return json.dumps({'status':'error','message': str(e)}), 400


if __name__ == "__main__":
    app.run(host='0.0.0.0')