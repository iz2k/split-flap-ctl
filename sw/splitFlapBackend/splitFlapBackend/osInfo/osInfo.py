import os
import shutil
import socket
import urllib
from time import strftime, gmtime

from babel.localtime import get_localzone


class osInfo:

    def getReport(self):
        # Get hostname and IP
        hostname = self.getHostname()
        ip = self.getIP()

        # Get internet connection status
        internet = self.getInternet()

        # Get FS space
        stat = shutil.disk_usage(os.getcwd())
        fs_total_GB = "%.2f" % (stat.total/1024/1024/1024)
        fs_free_GB = "%.2f" % (stat.free/1024/1024/1024)

        # Get TimeZone
        timezone = self.getTimeZone()

        hostinfo =  {
            'hostname' : hostname,
            'ip' : ip,
            'internet' : internet,
            'fs_total_GB' : fs_total_GB,
            'fs_free_GB' : fs_free_GB,
            'timezone' : timezone
        }
        return hostinfo

    def getHostname(self):
        return socket.gethostname()

    def getIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def getInternet(self, url='http://google.com', timeout=3):
        try:
            urllib.request.urlopen(url, timeout=timeout)
            return True
        except Exception as e:
            print(e)
            return False

    def getTimeZone(self):
        tdiff = strftime("%z", gmtime())
        return str(get_localzone()) + ' (' + tdiff[:3] + ':' + tdiff[3:] + ')'
