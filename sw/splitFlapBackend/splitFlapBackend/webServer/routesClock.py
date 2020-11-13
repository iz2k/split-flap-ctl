import datetime

from flask import Flask, request
from flask_socketio import SocketIO

from splitFlapBackend.clock.clock import clock
from splitFlapBackend.tools.jsonTools import prettyJson
from splitFlapBackend.tools.timeTools import getDateTime


def defineClockRoutes(app : Flask, sio : SocketIO, clk : clock):

    @app.route('/get-time', methods=['GET'])
    def setPhase():
        return prettyJson(getDateTime())

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/get-status', methods=['GET'])
    def getStatus():
        try:
            type = request.args.get('type')
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
            mode = request.args.get('mode')
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
            type = request.args.get('type')
            parameter = request.args.get('parameter')
            value = int(request.args.get('value'))
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
