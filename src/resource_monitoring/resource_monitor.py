from dataclasses import dataclass
import psutil
import copy
import io

from threading import Thread, Lock
from collections import deque
from typing import List, Tuple

from src.resource_monitoring.resource_usage_plotter import ResourceUsagePlotter


@dataclass
class ResourceDataHistory:
    cpu_cores_usage: List[deque]
    ram_usage: deque


class ResourceMonitor:
    TIME_INTERVAL = 3
    NUMBER_MEASUREMENTS = 61

    def __init__(self):
        self.plotter = ResourceUsagePlotter(time_interval=ResourceMonitor.TIME_INTERVAL)

        self.cpu_count = psutil.cpu_count()
        self.system_memory = psutil.virtual_memory().total / 10**6

        self.__resource_data_history = ResourceDataHistory(
            cpu_cores_usage=[deque([], maxlen=ResourceMonitor.NUMBER_MEASUREMENTS) for _ in range(self.cpu_count)],
            ram_usage=deque([], maxlen=ResourceMonitor.NUMBER_MEASUREMENTS)
        )

        self.__lock = Lock()

        self.__monitor_thread = Thread(target=self.__monitor_thread)
        self.__monitor_thread.start()

    def plot_resource_data_history(self) -> Tuple[io.BytesIO]:
        with self.__lock:
            resource_data_history = copy.deepcopy(self.__resource_data_history)

        cpu_cores_usage = resource_data_history.cpu_cores_usage
        ram_usage = resource_data_history.ram_usage

        cpu_plot = self.plotter.plot(values_for_each_plot=cpu_cores_usage, label_for_each_plot=lambda i: f"CPU{i} Usage")
        ram_plot = self.plotter.plot(values_for_each_plot=[ram_usage], label_for_each_plot=lambda i: "Memory Usage", max_y=self.system_memory)

        return cpu_plot, ram_plot

    def stop():
        # TODO: Implement a stop method
        pass

    def __monitor_thread(self):
        while True:
            cpu_cores_usage = psutil.cpu_percent(interval=ResourceMonitor.TIME_INTERVAL, percpu=True)
            ram_usage = psutil.virtual_memory().used / 10**6
            with self.__lock:
                self.__resource_data_history.ram_usage.append(ram_usage)
                for i, cpu_core_usage in enumerate(cpu_cores_usage):
                    self.__resource_data_history.cpu_cores_usage[i].append(cpu_core_usage)
