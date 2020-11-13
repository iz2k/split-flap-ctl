#!/usr/bin/env python3
import argparse

from splitFlapBackend.clock.clockThread import clockThread
from splitFlapBackend.osInfo.osInfoThread import osInfoThread
from splitFlapBackend.tools.ipTools import getHostname, getIP
from splitFlapBackend.weatherStation.weatherStation import weatherStation
from splitFlapBackend.webServer.webServer import define_webserver, define_webroutes


def main():

    debug=False
    async_mode='eventlet' # threading | eventlet

    # Parse arguments
    parser = argparse.ArgumentParser(description="iz2k's split-clock controller.")

    parser.add_argument("-port", default='8081', help=" port used for web server")

    args = parser.parse_args()

    # Define threads
    osinfoTh = osInfoThread()
    clockTh = clockThread()
    weather = weatherStation()

    # Define WebServer
    [app, sio] = define_webserver(async_mode=async_mode)

    define_webroutes(app, sio, clockTh.clock, weather)

    # Pass SIO to threads
    osinfoTh.set_sio(sio)
    clockTh.set_sio(sio)

    try:
        # Start threads
        osinfoTh.start()
        clockTh.start()

        # Start Webserver (blocks this thread until server quits)
        print('Starting Web Server:')
        print('\t\thttp://' + getHostname() + ':' + str(args.port))
        print('\t\thttp://' + getIP() + ':' + str(args.port))
        sio.run(app, port=args.port, host='0.0.0.0', debug=debug)

        # When server ends, stop threads
        osinfoTh.stop()
        clockTh.stop()

        # Print Goodby msg
        print('Exiting R102-DB-CTL...')

    except KeyboardInterrupt:
        # Stop threads
        osinfoTh.stop()
        clockTh.stop()


# If executed as main, call main
if __name__ == "__main__":
    main()
