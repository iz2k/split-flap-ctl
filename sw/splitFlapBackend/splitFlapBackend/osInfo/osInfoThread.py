from datetime import datetime, timedelta
import time
from queue import Queue
from threading import Thread

from flask_socketio import SocketIO

from splitFlapBackend.osInfo.osInfo import osInfo
from splitFlapBackend.tools.jsontools import prettyJson


class osInfoThread(Thread):

    queue = Queue()
    sio : SocketIO = None
    osInfoCtl = None
    report = None

    def __init__(self):
        Thread.__init__(self)
        self.osInfoCtl = osInfo()
        self.report = self.osInfoCtl.getReport()

    def start(self):
        self.emit()
        Thread.start(self)

    def stop(self):
        if self.is_alive():
            self.queue.put(['quit', 0])
            self.join()
            print('thread exit cleanly')

    def set_sio(self, sio : SocketIO):
        self.sio = sio

    def run(self):

        last_update = datetime.now()

        # Main loop
        run_app=True
        while(run_app):
            # Check if msg in queue
            while not self.queue.empty():
                [db_os_q_msg, db_os_q_data] = self.queue.get()
                if db_os_q_msg == 'quit':
                    run_app=False

            now = datetime.now()
            next_update = last_update + timedelta(0,10)
            if now > next_update:
                last_update = now
                self.report = self.osInfoCtl.getReport()
                self.emit()

            time.sleep(0.01)

    def emit(self):
        print('osInfo: ' + str(self.report))
        self.sio.emit('networking', prettyJson(self.report))
