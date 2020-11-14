import json
from urllib import request

from splitFlapBackend.tools.jsonTools import writeJsonFile, readJsonFile, prettyJson


class WeatherStation:

    config = {}
    report = {}

    def __init__(self):
        self.loadConfig()
        self.printConfig()
        self.updateWeatherReport()

    def saveConfig(self):
        writeJsonFile('cfgWeather.json', self.config)

    def loadConfig(self):
        self.config = readJsonFile('cfgWeather.json')
        if self.config == {}:
            self.createDefaultConfig()

    def printConfig(self):
        print('Weather Station Config:')
        print(prettyJson(self.config))

    def createDefaultConfig(self):
        self.config = {
            'openWeatherApi': '***REMOVED***',
            'geocodeApi': '',
            'location': '',
            'longitude': 0,
            'latitude': 0
                       }
        self.saveConfig()

    def updateParam(self, param, value):
        self.config[param]=value
        self.saveConfig()

    def updateWeatherReport(self):
        url = 'https://api.openweathermap.org/data/2.5/onecall?'
        url = url + 'lat=' + self.config['latitude'] + '&'
        url = url + 'lon=' + self.config['longitude'] + '&'
        url = url + 'exclude=minutely&'
        url = url + 'units=metric&'
        url = url + 'lang=es&'
        url = url + 'appid=' + self.config['openWeatherApi']

        with request.urlopen(url) as con:
            self.report = json.loads(con.read().decode())
        print('Weather Station Report Update:')
        print(prettyJson(
            {
                'location' : self.config['location'],
                'temperature' : str(self.report['current']['temp']) + 'C',
                'pressure' : str(self.report['current']['pressure']) + 'mbar',
                'humidity' : str(self.report['current']['humidity']) + '%',
                'weather' : self.report['current']['weather'][0]['description']
            }
        ))
        return self.report