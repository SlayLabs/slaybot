import discord
import os
from discord.ext import commands
from datetime import timedelta

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="s!", intents=intents)

LOGO = "https://cdn.discordapp.com/attachments/1505141118021402736/1505141380014669925/slaylabs_logo.png?ex=6a098ba5&is=6a083a25&hm=505739c1479f314292841763d680540f00f620b240287be5ded682828b27c438&"

USDT_ADDRESS = os.environ.get("USDT_ADDRESS", "")
USDT_ETH_ADDRESS = os.environ.get("USDT_ETH_ADDRESS", "")
USDC_ETH_ADDRESS = os.environ.get("USDC_ETH_ADDRESS", "")
LTC_ADDRESS = os.environ.get("LTC_ADDRESS", "")
BTC_ADDRESS = os.environ.get("BTC_ADDRESS", "")
SOL_ADDRESS = os.environ.get("SOL_ADDRESS", "")
ETH_ADDRESS = os.environ.get("ETH_ADDRESS", "")

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
            description=f"Welcome {user.mention}! Describe what you need and we'll get back to you.\n\n💰 **Payment:** Crypto \n\nUse `s!close` to close this ticket.",
            color=0x6A0DAD
        )
        embed.set_thumbnail(url=LOGO)
        embed.set_footer(text="SlayLabs", icon_url=LOGO)
        admin_role = discord.utils.get(guild.roles, name="Admin")
        owner_role = discord.utils.get(guild.roles, name="Owner")
        mentions = " ".join(r.mention for r in [admin_role, owner_role] if r)
        await channel.send(f"{mentions}", embed=embed)
        await interaction.response.send_message(f"✅ Ticket created: {channel.mention}", ephemeral=True)


@bot.event
async def on_ready():
    print(f"SlayBot is online as {bot.user}")
    bot.add_view(TicketButton())

@bot.command(name="services")
async def services(ctx):
    await ctx.message.delete()
    embed = discord.Embed(
        title="⚡ SlayLabs — Packages",
        description="Everything you need to get your PC running at full potential.",
        color=0x6A0DAD
    )
    embed.set_thumbnail(url=LOGO)
    embed.add_field(name="🔹 BIOS Only — $15", value="• Full BIOS tuning & configuration", inline=True)
    embed.add_field(name="🔹 Windows Tweak — $15", value="• Custom OS installation\n• Full Windows optimization", inline=True)
    embed.add_field(name="🔹 Advanced — $25", value="• Everything in Windows Tweak\n• Gatekept delay optimization\n• Fortnite specific tuning", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="🔹 Ultimate — $30", value="• Everything in Advanced\n• Full BIOS tuning", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="\u200b", value="\u200b", inline=True)
    embed.add_field(name="⚠️ Requirements", value="• Read ToS before opening a ticket\n• Fresh Windows install preferred\n• Must have a USB drive for OS installation", inline=False)
    embed.add_field(name="ℹ️ How it works", value="1. Click Create Ticket below\n2. Pick your package\n3. Send payment proof\n4. We get started", inline=False)
    embed.set_footer(text="SlayLabs • Open a ticket to get started", icon_url=LOGO)
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

@bot.command(name="tos")
async def tos(ctx):
    embed = discord.Embed(
        title="📋 SlayLabs — Terms of Service",
        description="Hey! Before we get started, just a few things to keep in mind. Pretty standard stuff, won't take long 👇",
        color=0x6A0DAD
    )
    embed.set_thumbnail(url=LOGO)
    embed.add_field(name="💸 No Refunds", value="All sales are final. Once you've paid, we get to work — no refunds after that.", inline=False)
    embed.add_field(name="⚖️ No Chargebacks", value="Please don't dispute payments. If something goes wrong, just talk to us — we'll sort it out. Chargebacks get you blacklisted permanently.", inline=False)
    embed.add_field(name="🖥️ Results May Vary", value="We're optimizing your PC, not performing magic. Results depend on your hardware and setup — we'll always do our best though.", inline=False)
    embed.add_field(name="⚠️ We're Not Liable", value="We're not responsible for any issues that come up after the service. Back up your data before we start — just to be safe.", inline=False)
    embed.add_field(name="🔒 Keep It to Yourself", value="Our tweaks are for you only. Don't share, resell, or redistribute them. Not cool and could get you banned.", inline=False)
    embed.add_field(name="✅ Just Be Honest", value="Make sure you own the payment method you're using. That's all we ask.", inline=False)
    embed.add_field(name="👍 That's It!", value="By paying, you're agreeing to all of the above. If you've got questions, just ask us in a ticket before buying.", inline=False)
    embed.set_footer(text="SlayLabs • We appreciate your trust 🙏", icon_url=LOGO)
    await ctx.send(embed=embed)

@bot.command(name="purge")
@commands.has_permissions(manage_messages=True)
async def purge(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"✅ Deleted {amount} messages.")
    await msg.delete(delay=3)

@purge.error
async def purge_error(ctx, error):
    await ctx.send("❌ You don't have permission to purge messages.")

@bot.command(name="paid")
@commands.has_permissions(manage_roles=True)
async def paid(ctx, user: discord.Member):
    role = discord.utils.get(ctx.guild.roles, name="Customer")
    if not role:
        await ctx.send("❌ Customer role not found. Make sure it's named exactly `Customer`.")
        return
    await user.add_roles(role)
    embed = discord.Embed(
        title="✅ Payment Confirmed",
        description=f"{user.mention} has been granted the **Customer** role. Welcome to SlayLabs!",
        color=0x6A0DAD
    )
    embed.set_footer(text="SlayLabs", icon_url=LOGO)
    await ctx.send(embed=embed)

@paid.error
async def paid_error(ctx, error):
    await ctx.send("❌ You don't have permission to use this command.")

@bot.command(name="rules")
async def rules(ctx):
    embed = discord.Embed(
        title="📋 Server Rules",
        description="Keep it chill and we'll all have a good time. Just a few things to keep in mind 👇",
        color=0x6A0DAD
    )
    embed.set_thumbnail(url=LOGO)
    embed.add_field(name="1️⃣ Be Cool", value="Treat everyone with respect. No toxicity, hate speech, or drama. We're all here for the same thing.", inline=False)
    embed.add_field(name="2️⃣ No Spam", value="Don't flood the chat with messages or random links. Keep it relevant.", inline=False)
    embed.add_field(name="3️⃣ No Self-Promo", value="Don't advertise your own stuff here without asking staff first.", inline=False)
    embed.add_field(name="4️⃣ Right Channels", value="Post in the right place. It keeps things clean for everyone.", inline=False)
    embed.add_field(name="5️⃣ Follow Discord's Rules", value="Discord's ToS applies here too. Keep that in mind.", inline=False)
    embed.add_field(name="6️⃣ No Scamming", value="Any scam attempts = instant ban. No exceptions.", inline=False)
    embed.add_field(name="7️⃣ Stay on Topic", value="This server is about PC optimization. Keep convos related to that.", inline=False)
    embed.set_footer(text="Break the rules and you're out. Simple 🤷 • SlayLabs", icon_url=LOGO)
    await ctx.send(embed=embed)

@timeout_user.error
async def timeout_error(ctx, error):
    await ctx.send("❌ You don't have permission to timeout members.")

@bot.check
async def admin_only(ctx):
    return ctx.author.guild_permissions.administrator

@bot.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles, name="Member")
    if role:
        await member.add_roles(role)

@bot.command(name="pay")
async def pay(ctx):
    embed = discord.Embed(
        title="💰 Payment Methods — SlayLabs",
        description="Send payment to any of the addresses below. Make sure to use the correct network!",
        color=0x6A0DAD
    )
    embed.add_field(name="USDT (TRC-20) ⭐ Recommended", value=f"`{USDT_ADDRESS}`", inline=False)
    embed.add_field(name="USDT (ETH Network)", value=f"`{USDT_ETH_ADDRESS}`", inline=False)
    embed.add_field(name="USDC (ETH Network)", value=f"`{USDC_ETH_ADDRESS}`", inline=False)
    embed.add_field(name="LTC — Litecoin", value=f"`{LTC_ADDRESS}`", inline=False)
    embed.add_field(name="BTC — Bitcoin", value=f"`{BTC_ADDRESS}`", inline=False)
    embed.add_field(name="SOL — Solana", value=f"`{SOL_ADDRESS}`", inline=False)
    embed.add_field(name="ETH — Ethereum", value=f"`{ETH_ADDRESS}`", inline=False)
    embed.set_footer(text="SlayLabs • After paying, send proof in this ticket.", icon_url=LOGO)
    await ctx.send(embed=embed)

bot.run(os.environ["TOKEN"])
