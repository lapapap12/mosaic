"""Main entry point for the Mosaic Ceramics QQ bot."""

import logging

import botpy
from botpy.message import Message

from qq_bot.config import load_config
from qq_bot.handlers import HELP_TEXT, handle_command

logger = logging.getLogger(__name__)


class MosaicBot(botpy.Client):
    """QQ channel bot that serves Mosaic Ceramics decision analysis data."""

    async def on_ready(self):
        logger.info("Bot %s is ready.", self.robot.name)

    async def on_at_message_create(self, message: Message):
        """Handle messages that @mention the bot in a channel."""
        # Strip the @mention prefix to extract the command
        content = message.content.strip()
        # The SDK prepends the @mention; remove it to get the actual command
        if " " in content:
            content = content.split(None, 1)[1]
        else:
            content = "/help"

        response = handle_command(content)
        if response is None:
            response = HELP_TEXT

        await message.reply(content=response)


def main():
    """Load configuration and start the bot."""
    config = load_config()
    bot_cfg = config["bot"]

    intents = botpy.Intents(public_guild_messages=True)
    client = MosaicBot(intents=intents)
    client.run(appid=bot_cfg["appid"], secret=bot_cfg["secret"])


if __name__ == "__main__":
    main()
