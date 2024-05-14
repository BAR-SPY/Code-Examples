import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import Context

class General(commands.Cog, name="general"):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.context_menu_user = app_commands.ContextMenu(
            name="Grab ID", callback=self.grab_id
        )
        self.bot.tree.add_command(self.context_menu_user)
        self.context_menu_message = app_commands.ContextMenu(
            name="Remove spoilers", callback=self.remove_spoilers
        )
        self.bot.tree.add_command(self.context_menu_message)

    #Message context menu command
    async def remove_spoilers(
            self, interaction: discord.Interaction, message: discord.Message
    ) -> None:
        """
        Removes spoilers from a message. Requires MESSAGE_CONTENT intent to 
        work properly.
        """
        spoiler_attachment = None
        for attachment in message.attachments:
            if attachment.is_spoiler():
                spoiler_attachment = attachment
                break
            embed = discord.Embed(
                title="Message without spoilers.",
                description=message.content.replace("||",""),
                color=0xBEBEFE,
            )
            if spoiler_attachment is not None:
                embed.set_image(url=attachment.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)

    # User context menu command
    async def grab_id(
            self, interaction: discord.Interaction, user: discord.User
    ) -> None:
        """
        Grabs the id of the user.
        """
        embed = discord.Embed(
            description=f"The ID of {user.mention} is `{user.id}`.",
            color=0xBEBEFE
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.hybrid_command(
        name="help",
        description="List all commands the bot has loaded."
    )
    async def help(self, context: Context) -> None:
        prefix = self.bot.command_prefix
        embed = discord.Embed(
            title="Help",
            description = "List of available commands: ",
            color=0xBEFEFE
        )
        for i in self.bot.cogs:
            if i == "owner" and not (await self.bot.is_owner(context.author)):
                continue
            cog = self.bot.get_cog(i.lower())
            commands = cog.get_commands()
            data = []
            for cmd in commands:
                description = cmd.description.partition("\n")[0]
                data.append(f"{prefix}{cmd.name} - {description}")
            help_text = "\n".join(data)
            embed.add_field(
                name=i.capitalize(), value=f"```{help_text}```", inline=False
            )
        await context.send(embed=embed)

async def setup(bot) -> None:
    await bot.add_cog(General(bot))