from typing import List
import discord
from discord.ext import commands
from src.resource_monitoring.resource_monitor_commands import ResourceMonitorCommands
from src.server_management.server_commands import ServerCommands
from src.server_management.server_data import ServerData


class DiscordBot(commands.Bot):

    def __init__(self, guild_ids: List[int], servers: List[ServerData]):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

        self.synced_guilds = [discord.Object(guild_id) for guild_id in guild_ids]
        self.server_commands = ServerCommands(servers)
        self.resource_monitor_commands = ResourceMonitorCommands()

    async def on_ready(self) -> None:
        await self.add_cog(self.server_commands, guilds=self.synced_guilds)
        await self.add_cog(self.resource_monitor_commands, guilds=self.synced_guilds)
        # DO NOT REMOVE, REFRESHES SLASH COMMANDS AT RESTART
        for guild in self.synced_guilds:
            await self.tree.sync(guild=guild)
        print(f"Logged in as {self.user}")
