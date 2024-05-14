import discord
from discord.ext import commands
from discord.ext.commands import Context
import random
import aiohttp

class Web(commands.Cog, name="web"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        name="xkcd",
        description="Get an XKCD"
    )
    async def xkcd(self, context: Context) -> None:
        # Set to be in a range of 2919 because that is the current number of comics.
        # Might restructure this later to grab that number from the most current xkcd.

        currenturlxkcd = f"https://xkcd.com/info.0.json"

        async with aiohttp.ClientSession() as session:
            async with session.get(
                currenturlxkcd
            ) as request:
                if request.status == 200:
                    res = await request.json()
                    num = random.randrange(0, res["num"])

            randurlxkcd = f"https://xkcd.com/{str(num)}/info.0.json"    
            async with session.get(
                 randurlxkcd
            ) as request:
                if request.status == 200:
                    res = await request.json()
                    embed = discord.Embed(description=f"Here's a random XKCD!({randurlxkcd.strip('/info.0.json')})",
                                          title=res["title"],
                                          url=res["img"],
                                          color=0xD75BF4)
                    embed.set_image(url=res["img"])
                else:
                    embed = discord.Embed(
                        title="Error!",
                        description="There is something wrong with the API. Please try again later.",
                        color=0xE02B2B
                    )
                await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(Web(bot))