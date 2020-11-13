import datetime

from flask import Flask, request
from flask_socketio import SocketIO

from splitFlapBackend.clock.clock import clock
from splitFlapBackend.tools.jsonTools import prettyJson
from splitFlapBackend.tools.timeTools import getDateTime


def defineWeatherRoutes(app : Flask, sio : SocketIO, clk : clock):

    @app.route('/get-geocodeapi', methods=['GET'])
    def getGeocodeApi():
        return prettyJson({'api': 'e0a2f8d0-2589-11eb-8316-3f4e0cc0daa9'})
