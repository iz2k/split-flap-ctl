import clock as clock

from splitFlapBackend.webServer.routesClock import defineClockRoutes
from splitFlapBackend.webServer.routesOsInfo import defineOsInfoRoutes
from splitFlapBackend.webServer.routesWeather import defineWeatherRoutes


def define_webserver(clk : clock, debug):
    if debug == False:
        import eventlet

        # Monkey_Patch eventlet to support threads
        eventlet.monkey_patch()

    from flask import Flask
    from flask_socketio import SocketIO
    from flask_cors import CORS

    # Create Flask App
    app = Flask(__name__, static_folder='web', static_url_path='')
    # Enable CORS to Flask
    CORS(app)
    # Add SocketIO to app
    if debug == True:
        sio = SocketIO(app, async_mode='threading')
    else:
        sio = SocketIO(app, async_mode='eventlet')
    # Enable CORS to SocketIO
    sio.init_app(app, cors_allowed_origins="*")

    defineClockRoutes(app, sio, clk)
    defineWeatherRoutes(app, sio, clk)
    defineOsInfoRoutes(app, sio , clk)

    return [app, sio]
