from flask import Flask, request, jsonify
from flask_socketio import SocketIO


from splitFlapBackend.tools.jsontools import prettyJson


def defineTagTesterRoutes(app : Flask, sio : SocketIO):

    @app.route('/post-tag-result', methods=['GET', 'POST'])
    def postTagResult():
        content = request.get_json(silent=True)
        return prettyJson({'status' : 'Tag Result Saved'})

    @app.route('/set-phase/<int:idx>', methods=['GET'])
    def setPhase(idx):
        sio.emit('phase', idx)
        return jsonify({'status' : 'Phase ' + str(idx) + ' received'})
