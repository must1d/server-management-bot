from typing import List
from src.server_management.server_data import ServerData
from src.server_management.server_wrapper import ServerWrapper
from src.server_management.response import Response


class ServerCommandHandler:

    def __init__(self):
        self.server_wrapper = ServerWrapper()

    def handle_start_command(self, server_data: ServerData) -> Response:
        return self.server_wrapper.start_server(server_data=server_data)

    def handle_stop_command(self, server_data: ServerData) -> Response:
        return self.server_wrapper.stop_server(server_data=server_data)

    def handle_kill_command(self, server_data: ServerData) -> Response:
        return Response.error("Kill is currently not implemented")

    def handle_restart_command(self, server_data: ServerData) -> Response:
        return self.server_wrapper.restart_server(server_data=server_data)

    def handle_status_command(self, server_data: ServerData) -> Response:
        return self.server_wrapper.get_status_of_server(server_data=server_data)

    def handle_send_console_command_to_server(self, server_data: ServerData, command: str) -> Response:
        return self.server_wrapper.send_console_command(server_data=server_data, command=command)
    
    def handle_general_status_command(self, server_data: List[ServerData]) -> Response:
        return self.server_wrapper.get_status_of_all_servers(server_data=server_data)
