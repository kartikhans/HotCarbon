import psutil
from datetime import datetime, timedelta
from dateutil import parser
from time import sleep
import atexit
import subprocess
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

filename = os.environ.get('METRIC_FILE')

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def read_metric(start_time, end_time):
    if start_time or end_time:
        start_time = parser.parse(start_time)
        end_time = parser.parse(end_time)
    count, utilization, energy = 0, 0, 0
    f = open(filename, "r")
    lines = f.readlines()
    for line in lines:
        line = line.split(",")
        timestamp = line[2][13:-1]
        if start_time <= parser.parse(timestamp) <= end_time:
            count += 1
            utilization += float(line[0][:-1].split(" ")[2])
            energy += float(line[1].split(" ")[3])
    return dict(avg_utilization=str(utilization / count) + '%', avg_energy=str(energy / count) + 'mW')


class CaptureSystemMetric:
    def __init__(self, time=10000):
        self.end_time = datetime.now() + timedelta(minutes=time)
        self.f = open(filename, "w")
        atexit.register(self.close_file)

    def close_file(self):
        self.f.close()

    def start(self):
        while datetime.now() <= self.end_time:
            sleep(1)
            energy = subprocess.run(
                "sudo powermetrics -i 1 -n 1 --samplers cpu_power -a --hide-cpu-duty-cycle | grep 'CPU Power'",
                shell=True, check=True, capture_output=True)
            self.f.write(
                "CPU Usage: {}%, {}, timestamp - {}\n".format(get_cpu_usage(), str(energy.stdout), datetime.now()))


if __name__ == '__main__':
    x = CaptureSystemMetric(time=1)
    x.start()
