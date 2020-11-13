import pytz
from flask import Flask
from flask import request as flask_request
from flask_socketio import SocketIO

from splitFlapBackend.clock.clock import clock
from splitFlapBackend.osInfo.osInfoThread import getReport
from splitFlapBackend.tools.jsonTools import prettyJson
from splitFlapBackend.tools.timeTools import setTimeZone


def defineOsInfoRoutes(app : Flask, sio : SocketIO, clk : clock):

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')
        sio.emit('osInfo', prettyJson(getReport()))

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')


    @app.route('/set-timezone', methods=['POST'])
    def setTimezone():
        content = flask_request.get_json(silent=True)
        if (content != None):
            setTimeZone(content['nameValue'])
            clk.timezone = pytz.timezone(content['nameValue'])
        return prettyJson({'status' : 'Timezone modified!'})