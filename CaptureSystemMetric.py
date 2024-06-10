import psutil
from datetime import datetime, timedelta
from dateutil import parser
from time import sleep
import atexit
import subprocess
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

filename = os.environ.get("METRIC_FILE")


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
    return dict(
        avg_utilization=str(utilization / count) + "%",
        avg_energy=str(energy / count) + "mW",
    )


# def read_metric(file_name, start_time, end_time):
#     count, utilization, energy = 0, 0, 0
#     if start_time or end_time:
#         start_time = parser.parse(start_time)
#         end_time = parser.parse(end_time)
#
#     f = open(file_name, "r")
#     lines = f.readlines()
#
#     for i in range(0, len(lines), 11):
#         timestamp = parser.parse(lines[i])
#         if start_time <= timestamp <= end_time:
#             temp_energy = 0
#             for j in range(1, 11):
#                 line = lines[i + j]
#                 line_data = line.split(";")[-1].split(" ")
#                 new_line_data = []
#                 for d in line_data:
#                     if d != '' and d != '\n':
#                         new_line_data.append(d)
#                 if new_line_data[1] == 'W':
#                     temp_energy += float(new_line_data[0])*1000
#                 elif new_line_data[1] == 'µW':
#                     temp_energy += float(new_line_data[0])/1000
#                 else:
#                     temp_energy += float(new_line_data[0])
#             energy += temp_energy/10
#     return dict(avg_energy=str(energy) + ' mW', total_energy=str((energy*(end_time - start_time).seconds)/1000) + ' W')
#


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
                shell=True,
                check=True,
                capture_output=True,
            )
            self.f.write(
                "CPU Usage: {}%, {}, timestamp - {}\n".format(
                    get_cpu_usage(), str(energy.stdout), datetime.now()
                )
            )


if __name__ == "__main__":
    x = CaptureSystemMetric(time=4)
    x.start()
