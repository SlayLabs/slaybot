import discord
import os
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="s!", intents=intents)

LOGO = "https://cdn.discordapp.com/attachments/1505141118021402736/1505141380014669925/slaylabs_logo.png?ex=6a098ba5&is=6a083a25&hm=505739c1479f314292841763d680540f00f620b240287be5ded682828b27c438&"

class TicketButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Create Ticket", style=discord.ButtonStyle.primary, custom_id="create_ticket")
    async def create_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        existing = discord.utils.get(guild.text_channels, name=f"ticket-{user.name.lower()}")
        if existing:
            await interaction.response.send_message(f"❌ You already have an open ticket: {existing.mention}", ephemeral=True)
            return

        admin_role = discord.utils.get(guild.roles, name="Admin")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
            guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True),
        }
        if admin_role:
            overwrites[admin_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name.lower()}",
            overwrites=overwrites
        )

        embed = discord.Embed(
            title="🎫 Ticket Opened",
            description=f"Welcome {user.mention}! Describe what you need and we'll get back to you.\n\nUse `s!close` to close this ticket.",
            color=0x6A0DAD
        )
        embed.set_thumbnail(url=LOGO)
        embed.set_footer(text="SlayLabs", icon_url=LOGO)
        await channel.send(embed=embed)
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)


@bot.event
async def on_ready():
    print(f"SlayBot is online as {bot.user}")
    bot.add_view(TicketButton())

@bot.command(name="services")
async def services(ctx):
    embed = discord.Embed(
        title="⚡ SlayLabs — PC Optimization",
        description="Premium Windows tweaking and optimization services.\nClick the button below to open a ticket.",
        color=0x6A0DAD
    )
    embed.set_thumbnail(url=LOGO)
    embed.add_field(name="📦 Packages", value=(
        "🔹 Windows Tweak — $10\n"
        "🔹 Advanced — $25\n"
        "🔹 Ultimate — $30\n"
        "🔹 BIOS Only — $15"
    ), inline=False)
    embed.add_field(name="ℹ️ How it works", value=(
        "1. Click Create Ticket below\n"
        "2. Pick your package\n"
        "3. Send payment proof\n"
        "4. We get started"
    ), inline=False)
    embed.add_field(name="⚠️ Important", value="Keep everything in one ticket. We will respond.", inline=False)
    embed.set_footer(text="SlayLabs", icon_url=LOGO)
    await ctx.send(embed=embed, view=TicketButton())

@bot.command(name="close")
async def close_ticket(ctx):
    if not ctx.channel.name.startswith("ticket-"):
        await ctx.send("❌ This is not a ticket channel.")
        return
    await ctx.send("🔒 Closing ticket...")
    await ctx.channel.delete()

@bot.command(name="embed")
async def send_embed(ctx, title: str, *, description: str):
    embed = discord.Embed(
        title=title,
        description=description,
        color=0x6A0DAD
    )
    embed.set_thumbnail(url=LOGO)
    embed.set_footer(text="SlayLabs", icon_url=LOGO)
    await ctx.send(embed=embed)

@bot.command(name="timeout")
@commands.has_permissions(moderate_members=True)
async def timeout_user(ctx, user: discord.Member, minutes: int, *, reason: str = "No reason provided"):
    duration = discord.utils.utcnow() + timedelta(minutes=minutes)
    await user.timeout(duration, reason=reason)
    await ctx.send(f"✅ {user.mention} timed out for {minutes} minutes. Reason: {reason}")

@timeout_user.error
async def timeout_error(ctx, error):
    await ctx.send("❌ You don't have permission to timeout members.")

bot.run(os.environ["TOKEN"])
