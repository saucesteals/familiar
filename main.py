from src import FamiliarBot
from dotenv import load_dotenv
import discord, os
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = FamiliarBot(command_prefix="!", intents=discord.Intents.all(), openai_api_key=OPENAI_API_KEY)
client.run(DISCORD_BOT_TOKEN)