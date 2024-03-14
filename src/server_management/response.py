from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    def __init__(self, code, color):
        self.code = code
        self.color = color

    Success = 0, 0x00ff00
    Error = 1, 0xff0000
    Info = 2, 0x53adcb


@dataclass
class Response:
    status: Status
    description: str

    @staticmethod
    def success(description: str):
        return Response(Status.Success, description)

    @staticmethod
    def error(description: str):
        return Response(Status.Error, description)

    @staticmethod
    def info(description: str):
        return Response(Status.Info, description)
