import discord
from discord.ext import commands
import json
from discord.ext.commands import MissingPermissions

bot = commands.Bot(command_prefix="your_prefix", help_command=None, intents=discord.Intents.all())

cogs = ['modmail']

for c in cogs:
    bot.load_extension(c)


@bot.event
async def on_ready():
    print("BOT READY")


@bot.command()
@commands.has_permissions(manage_channels=True, manage_messages=True)
async def get_data(ctx):
    with open("ModMail_file.json", "r") as f:
        data = json.load(f)
    json_ = json.dumps(data, indent=4)

    await ctx.send(f"```json\n{json_}```")


@get_data.error
async def get_data_error(ctx, error):
    if isinstance(error, MissingPermissions):
        await ctx.send("You're not allowed to use this", delete_after=5)
    else:
        raise error



bot.run('TOKEN')
