import discord
from discord.ext import commands
from discord import app_commands

from src.resource_monitoring.resource_monitor import ResourceMonitor


class ResourceMonitorCommands(commands.Cog):

    def __init__(self) -> None:
        self.__resource_monitor = ResourceMonitor()

    @app_commands.command(name="resource-usage", description="Manage servers")
    async def resource_usage(self, interaction: discord.Interaction):
        cpu_plot, ram_plot = self.__resource_monitor.plot_resource_data_history()

        cpu_plot_file = discord.File(cpu_plot, filename="cpu_plot.png")
        ram_plot_file = discord.File(ram_plot, filename="ram_plot.png")

        cpu_embed = self.__create_image_embed(title="CPU Usage", discord_image=cpu_plot_file)
        ram_embed = self.__create_image_embed(title="Memory Usage", discord_image=ram_plot_file)

        await interaction.response.send_message(embeds=[cpu_embed, ram_embed], files=[cpu_plot_file, ram_plot_file])

    def __create_image_embed(self, title, discord_image):
        embed = discord.Embed(title=title, color=0x00ff00)
        embed.set_image(url=f"attachment://{discord_image.filename}")
        return embed
