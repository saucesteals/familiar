from discord.ext import commands
import time
import json

class Utils(commands.Cog, name="Getting familiar ready"):
    def __init__(self, client:commands.Bot):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        self.client.logger.info("Logged into Discord as " + str(self.client.user))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CommandOnCooldown):
            return await ctx.reply(f"Slow down {ctx.author.name}! Please try again in {error.retry_after:.2f}s")
        elif isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
            return await ctx.send_help(ctx.command)
        elif isinstance(error, commands.CheckFailure):
            return await ctx.reply("Not allowed")
        raise error
    
    @commands.command()
    async def ping(self, ctx):
        """Get the bot's ping"""
        initial_time = time.time()
        msg = await ctx.send("Calculating...")
        await msg.edit(content=f":ping_pong: Pong! {time.time() - initial_time:.2f}ms")

    @commands.command()
    async def export(self, ctx):
        """Export your current conversation history"""
        history = self.client.conversations.get_history(ctx.author)
        await ctx.reply(f"```json\n{json.dumps(history, indent=4)}```")