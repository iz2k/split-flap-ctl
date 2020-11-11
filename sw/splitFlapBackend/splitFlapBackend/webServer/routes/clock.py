import datetime

from flask import Flask
from flask_socketio import SocketIO

from splitFlapBackend.osInfo.osInfo import osInfo
from splitFlapBackend.tools.jsontools import prettyJson


def defineClockRoutes(app : Flask, sio : SocketIO, osinfo : osInfo):

    @app.route('/get-time', methods=['GET'])
    def setPhase():
        return prettyJson(osinfo.getDateTime())
