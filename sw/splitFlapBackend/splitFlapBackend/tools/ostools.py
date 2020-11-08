import shlex
import subprocess

def check_service_running(service):
    raw_cmd = 'systemctl is-active --quiet ' + service
    cmd = shlex.split(raw_cmd)
    out = subprocess.run(cmd, capture_output=True)
    if out.returncode == 0:
        return True
    else:
        return False

def start_service(service):
    print('Starting ' + service + ' service')
    raw_cmd = 'sudo service ' + service + ' start'
    cmd = shlex.split(raw_cmd)
    subprocess.run(cmd, capture_output=True)

def stop_service(service):
    print('Stopping ' + service + ' service')
    raw_cmd = 'sudo service ' + service + ' stop'
    cmd = shlex.split(raw_cmd)
    subprocess.run(cmd, capture_output=True)
