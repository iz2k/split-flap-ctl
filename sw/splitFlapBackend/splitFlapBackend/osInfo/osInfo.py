import os
import shutil
import socket
import subprocess
import sys
import urllib
from time import strftime, gmtime

from babel.localtime import get_localzone


class osInfo:

    def getReport(self):
        # Get hostname and IP
        hostname = self.getHostname()
        ip = self.getIP()

        # Get internet connection status
        internet = self.getInternetCommandLine()

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

    def getTimeZone(self):
        tdiff = strftime("%z", gmtime())
        return str(get_localzone()) + ' (' + tdiff[:3] + ':' + tdiff[3:] + ')'

    def getInternetUrllib(self, url='http://google.com', timeout=3):
        try:
            urllib.request.urlopen(url, timeout=timeout)
            return True
        except Exception as e:
            print(e)
            return False

    def getInternetCommandLine(self):
        if (sys.platform == 'win32'):
            ping_cmd = 'ping -n 1 8.8.8.8'
            cmd = subprocess.Popen(ping_cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
            myStdout = cmd.stdout.read()
            if "TTL=" in str(myStdout):
                return True
            else:
                return False
        else:
            ping_cmd = 'ping -c 1 8.8.8.8'
            cmd = subprocess.Popen(ping_cmd.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            cmd.communicate()
            if cmd.returncode == 0:
                return True
            else:
                return False