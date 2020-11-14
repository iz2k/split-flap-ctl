#!/usr/bin/env python3
import argparse
import time

from splitFlapBackend.clock.clockThread import clockThread
from splitFlapBackend.osInfo.osInfoThread import osInfoThread
from splitFlapBackend.weatherStation.weatherStationThread import WeatherStationThread
from splitFlapBackend.webServer.webServer import webServerThread


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(description="iz2k's split-clock controller.")

    parser.add_argument("-port", default='8081', help=" port used for web server")

    args = parser.parse_args()

    # Define threads
    webserverTh = webServerThread(log=False)
    osInfoTh = osInfoThread()
    clockTh = clockThread()
    weatherStationThread = WeatherStationThread()

    webserverTh.define_webroutes(clockTh.clock, weatherStationThread.weatherStation)

    # Pass SIO to threads
    osInfoTh.set_sio(webserverTh.sio)
    clockTh.set_sio(webserverTh.sio)

    try:
        # Start threads
        osInfoTh.start()
        clockTh.start()
        webserverTh.start(port=args.port, host='0.0.0.0', debug=False, use_reloader=False)

        while (webserverTh.isRunning):
            time.sleep(0.1)


        # When server ends, stop threads
        osInfoTh.stop()
        clockTh.stop()

        # Print Goodby msg
        print('Exiting R102-DB-CTL...')

    except KeyboardInterrupt:
        # Stop threads
        osInfoTh.stop()
        clockTh.stop()


# If executed as main, call main
if __name__ == "__main__":
    main()
