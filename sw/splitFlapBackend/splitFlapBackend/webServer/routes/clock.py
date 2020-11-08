import datetime

from flask import Flask, request, jsonify
from flask_socketio import SocketIO


from splitFlapBackend.tools.jsontools import prettyJson


def defineClockRoutes(app : Flask, sio : SocketIO):

    @app.route('/get-time', methods=['GET'])
    def setPhase():
        now = datetime.datetime.now()
        return prettyJson({'year' : now.year,
                           'month': now.month,
                           'month': now.month,
                           'day': now.day,
                           'hour': now.hour,
                           'minute': now.minute,
                           'second': now.second})
