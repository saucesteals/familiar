from discord.ext import commands
import time

class Utils(commands.Cog, name="Getting familiar ready"):
    def __init__(self, client:commands.Bot):
        self.client = client
    

    @commands.Cog.listener()
    async def on_ready(self):
        print("Logged into Discord as", str(self.client.user))

    @commands.command()
    async def ping(self, ctx):
        """Get the bot's ping"""
        initial_time = time.time()
        msg = await ctx.send("Calculating...")
        await msg.edit(content=f":ping_pong: Pong! {time.time() - initial_time:.2f}ms")