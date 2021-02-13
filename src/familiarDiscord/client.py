import discord
from discord.ext import commands
from .cogs.conversate import Conversate
from .cogs.utils import Utils
from ..familiarOpenAI.conversations import Conversations

class FamiliarBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        openai_api_key = kwargs.get("openai_api_key")

        if not openai_api_key:
            raise Exception("No open_ai_key provided in client")

        self._add_cogs()

        self.conversations = Conversations(self, openai_api_key)

    def _add_cogs(self) -> None:
        self.add_cog(Conversate(self))
        self.add_cog(Utils(self))