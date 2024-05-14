import discord
import os
import subprocess
from discord.ext import commands
from discord.ext.commands import Context

class Server(commands.Cog, name="server"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="sinfo",
        description="Get info about servers."
    )
    async def sinfo(self, context: Context) -> None:
        ips = [ "192.168.1.20", "192.168.1.27", "192.168.1.40", "192.168.1.90", "192.168.1.100", "192.168.1.188", "192.168.1.75" ]
        up = []
        down = []
        for i in ips:
            cmd = f"ping -c 1 {i} &>/dev/null"
            ping = subprocess.run(cmd, shell = True, executable="/bin/bash")

            embed = discord.Embed(
                title="Server Ping",
                description="Tests a suite of servers."
            )
            if ping.returncode == 0:
                up.append(i)
            else:
                down.append(i)

            
        for i in up:
            embed.add_field(name="Up", value=f"{i}")
        for i in down:
            embed.add_field(name="Down", value=f"{i}")

        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Server(bot))

    