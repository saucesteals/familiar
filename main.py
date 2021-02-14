from src import FamiliarBot
from dotenv import load_dotenv
import discord, os
load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CUSTOM_DISCORD_PREFIX = os.getenv("DISCORD_BOT_PREFIX")
OPENAI_ENGINE = os.getenv("OPENAI_ENGINE")

client = FamiliarBot(command_prefix=CUSTOM_DISCORD_PREFIX.strip() if CUSTOM_DISCORD_PREFIX else "!", 
                     intents=discord.Intents.all(), 
                     openai_api_key=OPENAI_API_KEY.strip(), 
                     openai_engine=OPENAI_ENGINE.strip(),
                     logging=True,
                    )

client.run(DISCORD_BOT_TOKEN)