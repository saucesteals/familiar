from discord.ext import commands
import discord

class Conversate(commands.Cog, name='Conversation Handlers'):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.command(aliases=["f"])
    async def reply(self, ctx, *, prompt:str):
        """Get a reply"""
        reply = self.client.conversations.get_response(ctx.author, prompt)

        await ctx.reply(reply)

    @commands.command(aliases=["r"])
    async def reset(self, ctx):
        """Reset your history"""
        self.client.conversations.reset_history(ctx.author)

        await ctx.reply("Successfully reset your history!")