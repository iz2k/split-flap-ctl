import datetime

from flask import Flask, request
from flask_socketio import SocketIO

from splitFlapBackend.osInfo.osInfo import osInfo
from splitFlapBackend.tools.jsontools import prettyJson


def defineClockRoutes(app : Flask, sio : SocketIO, osinfo : osInfo):

    @app.route('/get-time', methods=['GET'])
    def setPhase():
        return prettyJson(osinfo.getDateTime())

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/get-status', methods=['GET'])
    def getStatus():
        try:
            type = request.args.get('type')
            if (type == 'hh'):
                return prettyJson({
                    'Desired digit': 5,
                    'Current digit': 4,
                    'Sync threshold': 50,
                    'Sync digit': 15,
                    'IR threshold': 100,
                    'IR turn-on': 10,
                    'IR debounce': 100
                })
            if (type == 'mm'):
                return prettyJson({
                    'Desired digit': 42,
                    'Current digit': 31,
                    'Sync threshold': 75,
                    'Sync digit': 31,
                    'IR threshold': 150,
                    'IR turn-on': 8,
                    'IR debounce': 120
                })
            return 'Invalid type'
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-parameter', methods=['GET'])
    def setParameter():
        try:
            type = request.args.get('type')
            parameter = request.args.get('parameter')
            value = request.args.get('value')
            text = 'SplitFlap ' + type + ': Setting parameter ' + parameter + ' to ' + value
            print(text)
            return prettyJson({'status':text})
        except Exception as e:
            print(e)
            return 'Invalid parameters'
