from flask_socketio import SocketIO

from splitFlapBackend.osInfo import osInfoThread


def defineOsInfoRoutes(sio : SocketIO, osinfo: osInfoThread):

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')
        osinfo.emit()

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')

