import discord
import random
from discord import Intents
from discord.ext import commands, tasks
from discord.ext.commands import Context
import os

from dotenv import load_dotenv

intents = Intents.default()
intents.message_content = True
#bot=discord.Client(intents=intents)

class DiscordBot(commands.Bot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix="!",
            intents=intents,
            help_command=None
        )

    async def load_cogs(self) -> None:
        """
        Loaded when the bot starts to load in cogs 
        """
        for file in os.listdir(f"{os.path.realpath(os.path.dirname(__file__))}/cogs"):
            if file.endswith(".py"):
                extension = file[:-3]
                try:
                    await self.load_extension(f"cogs.{extension}")
                    print(f"Loaded extenstion '{extension}'")
                except Exception as e:
                    print(f"Failed to load extension {extension}\n{e}")

    @tasks.loop(minutes=1.0)
    async def status_task(self):
        status = ["gone fishing...Do Not Disturb", "at a beach somewhere.", "not working."]
        await self.change_presence(activity=discord.Game(random.choice(status)))

    @status_task.before_loop
    async def before_status_task(self):
        await self.wait_until_ready()

    async def setup_hook(self) -> None:
        """
        Tasks to be done when bot first loads.
        """
        #Event listener for when the bot comes online
        print(f"Logged in as {self.user.name}")
        guild_count = 0
        for guild in bot.guilds:
            print(f"- {guild.id} (name: {guild.name})")

        guild_count += 1

        print("Python-bot is in " + str(guild_count) + " servers.")
        
        await self.load_cogs()
        await bot.tree.sync()
        self.status_task.start()

    async def on_message(self, message: discord.Message) -> None:
        if message.author == self.user or message.author.bot:
            return
        await self.process_commands(message)

load_dotenv()

# Loaded from the dotenv module.
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

bot = DiscordBot()
bot.run(DISCORD_TOKEN)
