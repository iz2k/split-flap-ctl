from splitFlapBackend.osInfo import osInfoThread
from splitFlapBackend.webServer.routes.clock import defineClockRoutes
from splitFlapBackend.webServer.routes.osInfo import defineOsInfoRoutes


def define_webserver(osinfo : osInfoThread, debug):
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

    defineClockRoutes(app, sio)

    defineOsInfoRoutes(sio , osinfo)

    return [app, sio]
