from flask import Flask
from flask_socketio import SocketIO

from splitFlapBackend.osInfo.osInfoThread import getReport
from splitFlapBackend.tools.jsonTools import prettyJson


def defineInfoRoutes(app : Flask, sio : SocketIO):

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')
        sio.emit('osInfo', prettyJson(getReport()))

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')

