from flask import Flask
from flask import request as flask_request
from flask_socketio import SocketIO

from splitFlapBackend.tools.jsonTools import prettyJson
from splitFlapBackend.weatherStation.weatherStation import WeatherStation


def defineWeatherStationRoutes(app : Flask, sio : SocketIO, weather : WeatherStation):

    @app.route('/get-weather-config', methods=['GET'])
    def getWeatherConfig():
        return prettyJson(weather.config)

    # /url?arg1=xxxx&arg2=yyy
    @app.route('/set-weather-config', methods=['GET'])
    def setWeatherConfig():
        try:
            # Get arguments
            for parameter in flask_request.args:
                value = flask_request.args.get(parameter)
                # Update parameter
                weather.updateParam(parameter,value)
            weather.printConfig()
            weather.updateWeatherReport()
            return prettyJson(weather.config)
        except Exception as e:
            print(e)
            return 'Invalid parameters'

    @app.route('/get-weather', methods=['GET'])
    def getWeather():
        return prettyJson(weather.report)
