from flask_socketio import SocketIO

from splitFlapBackend.osInfo.osInfo import osInfo
from splitFlapBackend.tools.jsontools import prettyJson


def defineOsInfoRoutes(sio : SocketIO, osinfo: osInfo):

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')
        sio.emit('osInfo', prettyJson(osinfo.getReport()))

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')

