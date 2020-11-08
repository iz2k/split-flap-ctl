from flask_socketio import SocketIO

from splitFlapBackend.osInfo import osInfoThread


def defineWebsocketEvents(sio : SocketIO, osinfo: osInfoThread):

    @sio.on('connect')
    def onconnect_event():
        print('Client connected!')
        osinfo.emit()

    @sio.on('disconnect')
    def ondisconnect_event():
        print('Client disconnected!')

    # Custom event
    @sio.on('handshake')
    def handle_my_custom_event(data):
        print('Handshake received: ' + str(data))
        print('Sending greeting.')
        sio.emit('handshake', 'Hello there from Flask!')
