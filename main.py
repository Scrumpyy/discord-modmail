import os
from dotenv import load_dotenv
load_dotenv()

from nextcord.ext.commands import Bot
from nextcord.ext import commands
from nextcord import (
    AllowedMentions,
    Intents,
    Status,
    Activity,
    MemberCacheFlags
)

import asyncio
import logging
import json
import config

logger = logging.basicConfig(
    format='[%(asctime)s] %(process)d-%(levelname)s : %(message)s', 
    datefmt='%d-%b-%y %H:%M:%S', 
    filename=f'discord-modmail_{config.PROJECT_NICKNAME}.log', 
    level=logging.WARNING
)

intents = Intents.none()
intents.guilds = True
intents.members = True
intents.messages = True

async def determine_prefix(bot, message):
    return config.PREFIX

bot = commands.Bot(
    status=Status.online, 
    activity=Activity(name=config.STATUS, type=1),
    allowed_mentions=AllowedMentions(everyone=False, users=True, roles=False),
    member_cache_flags=MemberCacheFlags(voice=False, joined=False),
    command_prefix=determine_prefix, 
    case_insensitive=True,
    chunk_guilds_at_startup=False,
    strip_after_prefix=True,
    help_command=None,
    max_messages=2500,
    intents=intents,
    heartbeat_timeout=20.0
)

@bot.command()
@commands.has_any_role(config.BOT_COMMANDER_ROLE_ID)
async def reload(ctx, module: str):
    try:
        bot.reload_extension(f"cogs.{module}")
        return await ctx.reply(f"`🔁` | `cogs.{module}` was successfully reloaded!")
    except commands.ExtensionNotLoaded as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` could not be reloaded as it was never loaded!\n```py\n{error}```")
    except commands.ExtensionNotFound as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` is not a valid cog!\n```py\n{error}```")
    except commands.NoEntryPointError as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` is missing a setup function & can't be reloaded!!\n```py\n{error}```")
    except Exception as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` encountered an error while being reloaded!\n```py\n{error}```")

@bot.command()
@commands.has_any_role(config.BOT_COMMANDER_ROLE_ID)
async def unload(ctx, module: str):
    try:
        bot.unload_extension(f"cogs.{module}")
        return await ctx.reply(f"`📤` | `cogs.{module}` was successfully unloaded!")
    except commands.ExtensionNotFound as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` is not a valid cog!\n```py\n{error}```")
    except commands.ExtensionNotLoaded as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` cannot be unloaded as it was never loaded!\n```py\n{error}```")
    except Exception as error: 
        return await ctx.reply(f"`⚠️` | `cogs.{module}` encountered an error while being unloaded!\n```py\n{error}```")

@bot.command()
@commands.has_any_role(config.BOT_COMMANDER_ROLE_ID)
async def load(ctx, module: str):
    try:
        bot.load_extension(f"cogs.{module}")
        return await ctx.reply(f"`📥` | `cogs.{module}` was successfully loaded!")
    except commands.ExtensionNotFound as error: 
        return await ctx.reply(f"`⚠️` | `cogs.{module}` is not a valid cog!\n```py\n{error}```")
    except commands.ExtensionAlreadyLoaded as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` has already been loaded!\n```py\n{error}```")
    except commands.NoEntryPointError as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` is missing a setup function & can't be loaded!\n```py\n{error}```")
    except Exception as error:
        return await ctx.reply(f"`⚠️` | `cogs.{module}` encountered an error while being loaded!\n```py\n{error}```")

@bot.listener('on_command_error')
async def on_command_error_handler(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.message.add_reaction("⏰")
        return await ctx.reply(f"`⏰` | You're on cooldown. | Try again in **{int(error.retry_after)}s**.", delete_after=error.retry_after if error.retry_after <= 60 else None)
    elif isinstance(error, commands.MissingPermissions):
        return await ctx.reply(f"`🧦` | You're lacking the following permission `{list(error.missing_perms)[0]}`.")
    elif isinstance(error, commands.MissingRequiredArgument):
        return await ctx.reply("`🚨` | You're missing a required argument!")
    elif isinstance(error, commands.TooManyArguments):
        return await ctx.reply("`🚨` | You've given me too many arguments!")
    elif isinstance(error, commands.BadArgument):
        return await ctx.reply("`🚨` | I'm not sure what one of your arguments is!")
    elif not isinstance(error, commands.CommandNotFound):
        return logging.error(error)

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        logging.info(f"Successfully loaded in 'cogs.{filename[:-3]}'")
    elif os.path.isfile(filename):
        logging.warning(f"Unable to load in 'cogs.{filename[:-3]}'")

bot.run(os.getenv('TOKEN'))