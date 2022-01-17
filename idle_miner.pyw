from ctypes import Structure, windll, c_uint, sizeof, byref
from time import sleep
import subprocess
import signal
import os
import sys


startupinfo = subprocess.STARTUPINFO()
startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW


class LASTINPUTINFO(Structure):
    _fields_ = [
        ('cbSize', c_uint),
        ('dwTime', c_uint),
    ]

def get_idle_duration():
    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = sizeof(lastInputInfo)
    windll.user32.GetLastInputInfo(byref(lastInputInfo))
    millis = windll.kernel32.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0


IDLE_THRESHOLD = 5 * 60  # 5m


class NamedPopen(subprocess.Popen):
     def __init__(self, *args, **kwargs):
         self.name = kwargs.pop('name', None)
         super().__init__(*args, **kwargs)


if __name__ == "__main__":
    process = None
    with open('output.log', 'wb', buffering=0) as log:
        log.write(f'Hi, I am process #{os.getpid()}\n'.encode('utf-8'))
        while(True):
            try:
                sleep(30)
                idle = get_idle_duration()
                if idle >= IDLE_THRESHOLD and process is None:
                    os.environ['GPU_MAX_ALLOC_PERCENT'] = '100'
                    os.environ['GPU_SINGLE_ALLOC_PERCENT'] = '100'
                    os.environ['GPU_MAX_HEAP_SIZE'] = '100'
                    os.environ['GPU_USE_SYNC_OBJECTS'] = '1'
                    process = NamedPopen([
                        'teamredminer.exe',
                        '-a', 'ethash',
                        '-o', 'POOL_URL',
                        '--eth_config=ETH_CONFIG',
                        '-u', 'ADDRESS'
                        ], name='teamredminer.exe', stdout=log, stderr=log, startupinfo=startupinfo)
                    sleep(5)
                else:
                    if idle < IDLE_THRESHOLD and process is not None:
                        try:
                            os.system("taskkill /F /im teamredminer.exe")
                            log.write(b'Sent close command\n')
                        except:
                            process.kill()
                        finally:
                            process = None

                    log.write(f'Idle for {idle}, starting in {IDLE_THRESHOLD - idle}...\n'.encode('utf-8'))
            except KeyboardInterrupt:
                sys.exit(0)
