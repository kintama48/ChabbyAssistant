import datetime
import json
import os
import platform
import sys

import discord
from discord.ext import commands
from discord.ext.commands import Bot

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)

intents = discord.Intents.default()
intents.members = True
bot = Bot(command_prefix=config["bot_prefix"], intents=intents)
epoch = datetime.datetime.utcfromtimestamp(0)
custom_invites = {}


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    print(f"Discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")


bot.remove_command("help")
if __name__ == "__main__":  # loading the features of the bot
    for file in os.listdir("./cogs"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{extension}")
                print(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                print(f"Failed to load extension {extension}\n{exception}")


@bot.event
async def on_member_join(member):
    await member.send(embed=discord.Embed(
        title=f"Hi <@!{member.id}>! Welcome to Sparks Server  (āUā)/ ",
        description="We are so glad to have you in our community ",
        color=0x036bfc,
        timestamp=datetime.datetime.now()
    ))


@bot.event
async def on_command_completion(ctx):  # command executed successfully
    fullCommandName = ctx.command.qualified_name
    split = fullCommandName.split(" ")
    executedCommand = str(split[0])
    print(
        f"Executed {executedCommand} command in {ctx.guild.name} (ID: {ctx.message.guild.id}) by {ctx.message.author} (ID: {ctx.message.author.id})")


@bot.event
async def on_command_error(context, error):
    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = discord.Embed(
            title="Please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0x8233FF
        )
        await context.send(embed=embed)
    # elif isinstance(error, commands.MissingPermissions):
    #     embed = discord.Embed(
    #         title="Error!",
    #         description="You are missing the permission `" + ", ".join(
    #             error.missing_perms) + "` to execute this command!",
    #         color=0xFF3387
    #     )
    #     await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xFF5733
        )
        await context.send(embed=embed)
    raise error


bot.run(config["token"])
