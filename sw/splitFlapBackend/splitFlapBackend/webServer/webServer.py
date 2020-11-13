import time

import clock as clock

from splitFlapBackend.weatherStation.weatherStation import weatherStation
from splitFlapBackend.webServer.routesClock import defineClockRoutes
from splitFlapBackend.webServer.routesOsInfo import defineOsInfoRoutes
from splitFlapBackend.webServer.routesWeatherStation import defineWeatherStationRoutes

from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS

def define_webserver(async_mode):
    if async_mode == 'eventlet':
        import eventlet

        # Monkey_Patch eventlet to support threads
        eventlet.monkey_patch()

    # Create Flask App
    app = Flask(__name__, static_folder='web', static_url_path='')
    # Enable CORS to Flask
    CORS(app)
    # Add SocketIO to app
    sio = SocketIO(app, async_mode=async_mode)
    # Enable CORS to SocketIO
    sio.init_app(app, cors_allowed_origins="*")

    return [app, sio]


def define_webroutes(app : Flask, sio : SocketIO, clk : clock, weather : weatherStation):
    defineClockRoutes(app, sio, clk)
    defineWeatherStationRoutes(app, sio, weather)
    defineOsInfoRoutes(app, sio , clk)

