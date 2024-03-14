from discord.ext import commands
from discord import app_commands
from enum import Enum
from typing import List
import discord

from src.server_management.server_command_handler import ServerCommandHandler
from src.server_management.server_data import ServerData
from src.config_loader import Config
from src.server_management.response import Response


class ServerAction(Enum):

    def __init__(self, command, handler):
        self.command = command
        self.handler = handler

    Start = "start", ServerCommandHandler.handle_start_command
    Stop = "stop", ServerCommandHandler.handle_stop_command
    Restart = "restart", ServerCommandHandler.handle_restart_command
    Status = "status", ServerCommandHandler.handle_status_command
    Kill = "kill", ServerCommandHandler.handle_kill_command


class ServerCommands(commands.Cog):

    def __init__(self, servers: List[ServerData]) -> None:
        self.__server_command_handler = ServerCommandHandler()
        self.__servers = servers

    @app_commands.command(name="server", description="Manage servers")
    @app_commands.describe(action="Select action for server to perform.")
    @app_commands.describe(game="Select server to perform action on.")
    @app_commands.choices(game=[app_commands.Choice(name=server.name, value=server.name) for server in Config.instance().servers])
    async def server(self, interaction: discord.Interaction, action: ServerAction, game: app_commands.Choice[str]) -> None:
        server_data = next(filter(lambda element: element.name == game.value, self.__servers))

        embed = await self.__send_initial_message(description=f"{action.name} {game.value}", interaction=interaction)

        response = self.__try_to_perform_action(action=action, server_data=server_data)

        await self.__update_sent_message_with_result(response=response, embed=embed, interaction=interaction)

    @app_commands.command(name="console-command", description="Manage servers")
    @app_commands.describe(game="Select server to perform action on.")
    @app_commands.choices(game=[app_commands.Choice(name=server.name, value=server.name) for server in Config.instance().servers])
    async def console_command(self, interaction: discord.Interaction, game: app_commands.Choice[str], command: str) -> None:
        server_data = next(filter(lambda element: element.name == game.value, self.__servers))

        embed = await self.__send_initial_message(description=f"Sending command '{command}' to server '{game.value}'", interaction=interaction)

        response = self.__try_to_send_console_command(command=command, server_data=server_data)

        await self.__update_sent_message_with_result(response=response, embed=embed, interaction=interaction)

    @app_commands.command(name="status", description="Check status of each server")
    async def status(self, interaction: discord.Interaction) -> None:
        embed = await self.__send_initial_message(description=f"Checking status of each server", interaction=interaction)
        response = self.__try_to_send_status_requests()
        await self.__update_sent_message_with_result(response=response, embed=embed, interaction=interaction)

    async def __send_initial_message(self, description: str, interaction: discord.Interaction) -> discord.Embed:
        embed = discord.Embed(title="Server management", color=0xffff00)
        embed.add_field(name="Command", value=description, inline=False)
        await interaction.response.send_message(embed=embed)
        return embed

    def __try_to_perform_action(self, action: ServerAction, server_data: ServerData) -> Response:
        try:
            response = action.handler(self.__server_command_handler, server_data)
        except Exception as e:
            response = Response.error(f"Something went wrong: '{e}'")
        return response

    def __try_to_send_console_command(self, command: str, server_data: ServerData) -> Response:
        try:
            response = self.__server_command_handler.handle_send_console_command_to_server(server_data=server_data, command=command)
        except Exception as e:
            response = Response.error(f"Something went wrong: '{e}'")
        return response
    
    def __try_to_send_status_requests(self) -> Response:
        try:
            response = self.__server_command_handler.handle_general_status_command(self.__servers)
        except Exception as e:
            response = Response.error(f"Something went wrong: '{e}")
        return response

    async def __update_sent_message_with_result(self, response: Response, embed: discord.Embed, interaction: discord.Interaction) -> None:
        embed.color = response.status.color
        embed.add_field(name=response.status.name, value=response.description, inline=False)

        await interaction.edit_original_response(embed=embed)
