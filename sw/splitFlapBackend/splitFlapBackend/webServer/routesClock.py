import pytz
from flask import Flask
from flask import request as flask_request
from flask_socketio import SocketIO

from splitFlapBackend.clock.clock import Clock
from splitFlapBackend.tools.jsonTools import prettyJson
from splitFlapBackend.tools.timeTools import getDateTime, setTimeZone


def defineClockRoutes(app : Flask, sio : SocketIO, clk : Clock):

    @app.route('/get-time', methods=['GET'])
    def setPhase():
        return prettyJson(getDateTime())

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/get-status', methods=['GET'])
    def getStatus():
        try:
            type = flask_request.args.get('type')
            if (type == 'hh'):
                return prettyJson(clk.hh.getStatus())
            if (type == 'mm'):
                return prettyJson(clk.mm.getStatus())
            return 'Invalid type'
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/get-mode', methods=['GET'])
    def getMode():
            return prettyJson({
                'mode' : clk.mode
            })

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-mode', methods=['GET'])
    def setMode():
        try:
            mode = flask_request.args.get('mode')
            clk.mode = mode
            return prettyJson({
                'mode' : clk.mode
            })
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-parameter', methods=['GET'])
    def setParameter():
        try:
            type = flask_request.args.get('type')
            parameter = flask_request.args.get('parameter')
            value = int(flask_request.args.get('value'))
            if (type == 'hh'):
                clk.hh.setParameter(parameter, value)
            elif (type == 'mm'):
                clk.mm.setParameter(parameter, value)
            else:
                return 'Invalid type'
            return prettyJson({'status': 'ok'})
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    @app.route('/set-timezone', methods=['POST'])
    def setTimezone():
        content = flask_request.get_json(silent=True)
        if (content != None):
            setTimeZone(content['nameValue'])
            clk.timezone = pytz.timezone(content['nameValue'])
        return prettyJson({'status' : 'Timezone modified!'})