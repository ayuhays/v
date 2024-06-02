import os
import discord
from discord.ext import tasks, commands

status = discord.Status.online  # online/dnd/idle

GUILD_ID = os.getenv("GUILD_ID")
CHANNEL_ID = os.getenv("CHANNEL_ID")
SELF_MUTE = True
SELF_DEAF = True

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    print("[ERROR] Please add a token inside Secrets.")
    exit()

intents = discord.Intents.default()
intents.voice_states = True
intents.presences = True

bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command('help')


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    await joiner()


async def joiner():
    guild = bot.get_guild(int(GUILD_ID))
    if not guild:
        print("[ERROR] Bot is not in the specified guild.")
        return

    channel = guild.get_channel(int(CHANNEL_ID))
    if not channel:
        print("[ERROR] Channel not found.")
        return

    voice_client = await channel.connect()
    await voice_client.disconnect()


@tasks.loop(seconds=30)
async def keep_running():
    await joiner()


@bot.event
async def on_disconnect():
    await bot.close()


@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error in {event}: {args[0]}')
    await bot.close()


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass  # Ignore CommandNotFound errors


keep_running.start()
bot.run(TOKEN)
