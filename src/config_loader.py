import json

from src.server_management.server_data import ServerData
from pathlib import Path


class Config:
    instance_obj = None

    def __init__(self):
        config = self.__read_config()
        self.__token = config["token"]
        self.__guild_ids = config["guilds"]
        self.__servers = [ServerData.from_json(json_server) for json_server in config["servers"]]

    @classmethod
    def instance(cls):
        if cls.instance_obj is None:
            cls.instance_obj = Config()
        return cls.instance_obj

    @property
    def token(self):
        return self.__token

    @property
    def guild_ids(self):
        return self.__guild_ids

    @property
    def servers(self):
        return self.__servers

    def __read_config(self):
        root_dir = Path(__file__).resolve().parent
        config_path = root_dir.parent / "config.json"
        with open(config_path, "r") as file:
            config = json.load(file)
        return config
