import discord
import os
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"SlayBot is online as {bot.user}")
    await bot.tree.sync()

@bot.tree.command(name="embed", description="Send a custom embed")
async def send_embed(interaction: discord.Interaction, title: str, description: str):
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x6A0DAD
    )
    embed.set_footer(text="SlayLabs")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timeout", description="Timeout a user")
@discord.app_commands.checks.has_permissions(moderate_members=True)
async def timeout_user(interaction: discord.Interaction, user: discord.Member, minutes: int, reason: str = "No reason provided"):
    duration = discord.utils.utcnow() + timedelta(minutes=minutes)
    await user.timeout(duration, reason=reason)
    await interaction.response.send_message(f"✅ {user.mention} timed out for {minutes} minutes. Reason: {reason}")

@timeout_user.error
async def timeout_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("❌ You don't have permission to timeout members.", ephemeral=True)

bot.run(os.environ["TOKEN"])
