import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from splitFlapBackend.tools.timeTools import getTimeZoneAwareNow
from splitFlapBackend.weatherStation.weatherStation import WeatherStation


class WeatherStationThread(Thread):

    queue = Queue()
    weatherStation = WeatherStation()

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def run(self):

        self.report = self.weatherStation.updateWeatherReport()
        last_update = getTimeZoneAwareNow(self.clock.timezone)

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [db_os_q_msg, db_os_q_data] = self.queue.get()
                if db_os_q_msg == 'quit':
                    run_app=False

            now = getTimeZoneAwareNow(self.clock.timezone)
            next_update = last_update + timedelta(minutes=15)
            if now > next_update:
                last_update = now
                self.report = self.weatherStation.updateWeatherReport()

            time.sleep(1)
