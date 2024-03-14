import subprocess
from typing import List
import libtmux

import time
from src.server_management.response import Response
from src.server_management.server_data import ServerData

DEFAULT_TIMEOUT = 60


def wait_until(predicate, timeout=DEFAULT_TIMEOUT, period=1):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if predicate():
            return True
        time.sleep(period)
    return False


def check_if_server_alive(func):
    def wrapper(*args, **kwargs):
        self: ServerWrapper = args[0]
        if not self.is_tmux_installed:
            return Response.error("Tmux is not installed!")
        return func(*args, **kwargs)
    return wrapper


class ServerWrapper:

    def __init__(self):
        result = subprocess.run(['which', 'tmux'], stdout=subprocess.PIPE)
        self.__is_tmux_installed = result.returncode == 0

        self.__tmux_server = libtmux.Server()

    @property
    def is_tmux_installed(self):
        return self.__is_tmux_installed

    @check_if_server_alive
    def start_server(self, server_data: ServerData) -> Response:
        if self.__is_server_running(server_data):
            return Response.info("Server already running!")
        self.__tmux_server.new_session(
            session_name=server_data.name,
            start_directory=server_data.path_to_server,
            window_command=f"./{server_data.start_script}",
            attach=False
        )
        return Response.success("Started server")

    @check_if_server_alive
    def stop_server(self, server_data: ServerData) -> Response:
        if not self.__is_server_running(server_data):
            return Response.info("Server is not running!")
        session = self.__tmux_server.sessions.get(session_name=server_data.name)
        session.panes[0].send_keys(server_data.stop_command)
        if not wait_until(predicate=lambda: not self.__is_server_running(server_data)):
            return Response.error("Server was not stopped properly")
        return Response.success("Server stopped!")

    @check_if_server_alive
    def restart_server(self, server_data: ServerData) -> Response:
        if not self.__is_server_running(server_data):
            return Response.info("Server is not running!")
        self.stop_server(server_data=server_data)
        if self.__is_server_running(server_data):
            return Response.error("Server could not be stopped!")
        self.start_server(server_data=server_data)
        if self.__is_server_running(server_data):
            return Response.success("Server restarted!")
        return Response.error("Server could not be started!")

    @check_if_server_alive
    def get_status_of_server(self, server_data: ServerData) -> Response:
        if self.__is_server_running(server_data=server_data):
            return Response.info(f"Server {server_data.name} is running!")
        return Response.info(f"Server {server_data.name} is not running!")

    def __is_server_running(self, server_data: ServerData) -> bool:
        try:
            self.__tmux_server.sessions.get(session_name=server_data.name)
            return True
        except Exception:
            return False
        
    def get_status_of_all_servers(self, server_data: List[ServerData]) -> Response:
        response_descriptions = [self.get_status_of_server(server).description for server in server_data]
        descriptions_formatted = "\n".join(response_descriptions)
        return Response.info(descriptions_formatted)

    def send_console_command(self, server_data: ServerData, command: str):
        if not self.__is_server_running(server_data):
            return Response.info("Server is not running!")
        session = self.__tmux_server.sessions.get(session_name=server_data.name)
        pane = session.panes[0]
        pane.send_keys(command)
        time.sleep(1)
        response = pane.capture_pane()
        try:
            # TODO: fix duplicate takes first one
            index = response.index(command)
        except ValueError:
            index = -5
        return Response.success('\n'.join(response[index:]))
