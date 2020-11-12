import time
from datetime import timedelta
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapBackend.clock.clock import clock
from splitFlapBackend.tools.timeTools import getTimeZoneAwareNow


class clockThread(Thread):

    queue = Queue()
    sio : SocketIO = None
    clock = clock()

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def run(self):

        last_update = getTimeZoneAwareNow(self.clock.timezone)

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [db_os_q_msg, db_os_q_data] = self.queue.get()
                if db_os_q_msg == 'quit':
                    run_app=False

            if (self.clock.mode == 'clock'):
                now = getTimeZoneAwareNow(self.clock.timezone)
                next_update = last_update + timedelta(0, 1)
                if now > next_update:
                    last_update = now
                    self.clock.hh.setDigit(now.hour)
                    self.clock.mm.setDigit(now.minute)

            time.sleep(1)
