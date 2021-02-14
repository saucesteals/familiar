import os
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from ...utils import cleanse_prompt

reply_cooldown = os.getenv("REPLY_COOLDOWN")
reply_cooldown = int(reply_cooldown.strip()) if reply_cooldown else 3

class Conversate(commands.Cog, name='Conversation Handlers'):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.cooldown(rate=1, per=reply_cooldown, type=BucketType.user)
    @commands.command(aliases=["f"])
    async def reply(self, ctx, *, prompt:str):
        """Get a reply"""
        async with ctx.channel.typing():
            try:
                reply = self.client.conversations.get_response(ctx.author, cleanse_prompt(prompt, ctx.message))
                return await ctx.reply(reply)
            except Exception as error:
                self.client.logger.error("At reply command: " + str(error))
                await ctx.reply("Oops, something went wrong!")

    @commands.command(aliases=["r"])
    async def reset(self, ctx):
        """Reset your history"""
        self.client.conversations.reset_history(ctx.author)

        await ctx.reply("Successfully reset your history!")