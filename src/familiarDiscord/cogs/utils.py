import asyncio
import discord
from discord.ext import commands
import time
import json
import random
from ...utils import history_to_str

class Utils(commands.Cog, name="Useful utilities for familiar"):
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

    @commands.command(aliases=["e"])
    async def export(self, ctx, member:discord.Member=None):
        """Export yours or another members current conversation history"""
        history = self.client.conversations.get_history(member if member else ctx.author)
        await ctx.reply(history_to_str(history, True))

    @commands.command(aliases=["t"])
    async def transfer(self, ctx, member:discord.Member):
        """Transfer someone's current conversation to yours"""
        history = self.client.conversations.get_history(member)
        self.client.conversations.set_history(ctx.author, history)
        await ctx.reply(f"Your new history:\n{history_to_str(history, True)}")

    def get_creation_embed(self, fake_history:dict) -> discord.Embed:
        embed = discord.Embed(color=0xFFF7F5, title="Respond with the next response (Prefix with a **-**)")
        embed.description = "Say **STOP** to stop and save until the last finished combination\n"
        embed.description += "Say **BACK** to go back to the previous step\n"
        embed.description += f"Example: `-{random.choice(['Hey!', 'How are you?', 'Whats up?'])}`\n"
        embed.description += history_to_str(fake_history, True)
        return embed

    async def get_next_create_message(self, ctx) -> discord.Message:
        return await self.client.wait_for('message', timeout=30.0, check=lambda message: message.author == ctx.author and \
                                                                    message.channel.id == ctx.channel.id and (message.content.startswith("-") \
                                                                    or message.content.lower() in ["stop", "back"])
                                                                
                                                                )


    @commands.command(aliases=["c"])
    async def create(self, ctx):
        """Create a sample conversation for me to base my responses off of"""
        history = []
        fake_history = []
        skip_human = False
        force_stop = False
        
        while len(history) <= 5:

            if not skip_human:
                fake_history.append({"human":""})
            
                msg = await ctx.reply(embed=self.get_creation_embed(fake_history))

                try:
                    human_message = await self.get_next_create_message(ctx)
                    await human_message.delete()
                except asyncio.TimeoutError:
                    force_stop = True

                await msg.delete()
                if force_stop or human_message.content.lower() == "stop":
                    break
                elif human_message.content.lower() == "back":
                    if fake_history:
                        if len(fake_history) > 1:
                            skip_human = True

                        del fake_history[len(fake_history) - 1]
                    
                    if history:
                        del history[len(history) - 1]
                    continue

                fake_history[len(fake_history)-1]["human"] = human_message.content[1:99]

            fake_history[len(fake_history)-1]["bot"] = ""

            msg = await ctx.reply(embed=self.get_creation_embed(fake_history))

            try:
                bot_message = await self.get_next_create_message(ctx)
                await bot_message.delete()
            except asyncio.TimeoutError:
                force_stop = True

            skip_human = False

            await msg.delete()
            if force_stop or bot_message.content.lower() == "stop":
                break
            elif bot_message.content.lower() == "back":
                
                if fake_history:
                    del fake_history[len(fake_history) - 1]

                if history:
                    del history[len(history) - 1]
                continue

            fake_history[len(fake_history)-1]["bot"] = bot_message.content[1:99]

            history.append(self.client.conversations._new_response(human_message.content[1:99], bot_message.content[1:99]))


        if history:
            self.client.conversations.set_history(ctx.author, history)
            await ctx.reply(f"Your new history:\n{history_to_str(history, True)}")

        else:
            await ctx.reply(f"Invalid or empty history:\n{history_to_str(history, True)}")