from src.discord_bot import DiscordBot
from src.config_loader import Config

if __name__ == "__main__":
    config = Config.instance()

    bot = DiscordBot(
        guild_ids=config.guild_ids,
        servers=config.servers
    )

    bot.run(token=config.token)
