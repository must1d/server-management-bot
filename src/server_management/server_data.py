from dataclasses import dataclass


@dataclass
class ServerData:
    name: str
    start_script: str
    path_to_server: str
    stop_command: str

    @staticmethod
    def from_json(json_data):
        name = json_data["name"]
        start_script = json_data["start_script"]
        path_to_server = json_data["path_to_server"]
        stop_command = json_data["stop_command"]
        return ServerData(name, start_script, path_to_server, stop_command)
