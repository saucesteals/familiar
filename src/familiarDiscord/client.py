import discord
from discord.ext import commands
import logging
from ..logger import CustomFormatter
from .cogs.conversate import Conversate
from .cogs.utils import Utils
from ..familiarOpenAI.conversations import Conversations


class FamiliarBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.persona_path = kwargs.get("persona_path")
        self.color = kwargs.get("color", 0xFFF7F5)

        openai_api_key = kwargs.get("openai_api_key")
        openai_engine = kwargs.get("openai_engine")

        if not openai_api_key:
            raise Exception("No open_ai_key provided in client")

        if not openai_engine:
            openai_engine = "davinci"

        self.logger = logging.getLogger("familiar")
        ch = logging.StreamHandler()
        ch.setFormatter(CustomFormatter())
        self.logger.addHandler(ch)

        if kwargs.get("logging"):
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.WARNING)
        
        self._add_cogs()

        self.conversations = Conversations(self, openai_api_key, openai_engine)

    def _add_cogs(self) -> None:
        self.add_cog(Conversate(self))
        self.add_cog(Utils(self))

    def get_embed(self, *args, **kwargs) -> discord.Embed:
        kwargs["color"] = self.color
        return discord.Embed(*args, **kwargs)
