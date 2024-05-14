import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class Moderation(commands.Cog, name="moderation"):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.hybrid_command(
            name="purge",
            description="Delete a number of messages."
    )
    async def purge(self, context: Context, amount: int):
        await context.send("Deleting messages...")
        purged_messages = await context.channel.purge(limit=amount + 1)
        embed = discord.Embed(
            description=f"**{context.author}** cleared **{len(purged_messages)-1}** messages.",
            color=0xBEFEFE
        )
        await context.channel.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Moderation(bot))