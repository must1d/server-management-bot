import matplotlib.pyplot as plt
import numpy as np
import io

from typing import Callable

plt.style.use("seaborn-v0_8-dark")

for param in ["figure.facecolor", "axes.facecolor", "savefig.facecolor"]:
    plt.rcParams[param] = "#212946"

for param in ["text.color", "axes.labelcolor", "xtick.color", "ytick.color"]:
    plt.rcParams[param] = "0.9"


class ResourceUsagePlotter:

    COLORS = [
        "#08F7FE",  # teal/cyan
        "#FE53BB",  # pink
        "#F5D300",  # yellow
        "#00ff41",  # matrix green
        "#08F7FE",  # teal/cyan
    ]

    def __init__(self, time_interval):
        self.time_interval = time_interval

    def plot(self, values_for_each_plot, label_for_each_plot: Callable, min_y=0, max_y=100) -> io.BytesIO:
        number_of_data_points = len(values_for_each_plot[0])

        time_scale = self.__get_time_scale(number_of_data_points=number_of_data_points)

        for i, cpu_usage_history in enumerate(values_for_each_plot):
            color = ResourceUsagePlotter.COLORS[i % len(ResourceUsagePlotter.COLORS)]
            self.__plot_line_with_glow(plt=plt, x=time_scale, y=cpu_usage_history, color=color, label=label_for_each_plot(i))

        plt.xlim(time_scale[0], time_scale[-1])
        plt.ylim(min_y - 1, max_y + 1)
        plt.grid(color='#2A3459')
        plt.legend(prop={'size': 12})

        data_stream = io.BytesIO()

        plt.savefig(data_stream, format='png', bbox_inches="tight", dpi=300)
        plt.close()

        data_stream.seek(0)
        return data_stream

    def __plot_line_with_glow(self, plt, x, y, color, label):
        plt.plot(x, y, marker='o', markersize=1, linewidth=0.5, color=color, label=label)
        for n in range(1, 11):
            plt.plot(x, y, marker='o', markersize=1, linewidth=1+1.05*n, color=color, alpha=0.03)

    def __get_time_scale(self, number_of_data_points):
        left_time = -number_of_data_points * self.time_interval + self.time_interval
        right_time = 0
        return np.arange(left_time, right_time + self.time_interval, self.time_interval)
