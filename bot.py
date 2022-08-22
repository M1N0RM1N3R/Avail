import sys
from tinydb import TinyDB, Query
import time
from typing import Dict, List
import discord
import json
import pickle

from classes import Confirm, Event

secrets: dict = json.loads(open("secrets.json").read())
captains_db = TinyDB('captains_db.json')
bot: discord.Bot = discord.Bot(
    intents=discord.Intents(messages=True, guilds=True))
version = "2208.1"


@bot.event
async def on_ready():
    global login_time
    print("✅ %s is ready and online!" % bot.user)
    login_time = time.time()


@bot.slash_command()
async def ping(
    ctx: discord.ApplicationContext,
):
    await ctx.send_response(f"Pong! Latency is {bot.latency} seconds. I've been active since <t:{int(login_time)}>. Version: {version}", ephemeral=True)


@bot.slash_command()
async def help(
    ctx: discord.ApplicationContext
):
    await ctx.send_response(f'''How to use Avail:
- Simply mention me in a message and I will reply with an Avail widget.
- When an Avail widget is created, you can join the widget by clicking the "I'm available" button.
- When enough players join, I will ping the current Captain (<@{captains_db.get(Query().guild == ctx.guild.id)['captain']}>) to let them know.
- Something come up? You can remove yourself from a widget by clicking the "Cancel availability" button.
  - If a player cancels after enough players have joined, I will not re-ping the Captain when enough players join again.
Made with ❤️ by <@547203725668646912>''', ephemeral=True)

config = discord.SlashCommandGroup(
    name="config", description="Per-guild configuration commands")


@config.command(name="captain", description="Set the Captain for this guild.")
async def set_captain(
    ctx: discord.ApplicationContext,
    new_captain: discord.Option(discord.Member, "The user to set as Captain"),
):
    try:
        try:
            captain = captains_db.get(Query().guild == ctx.guild_id)['captain']
        except TypeError:
            captain = None
        if ctx.author == ctx.guild.owner or ctx.author.id == captain:
            captains_db.upsert({'guild': ctx.guild.id,
                                'captain': new_captain.id},
                               Query().guild == ctx.guild_id)
            await ctx.send_response(f"✅ Captain set to <@{new_captain.id}>", ephemeral=True)
        else:
            await ctx.send_response(f"⛔ Only the guild owner or current Captain is allowed to set the Captain.")

    except Exception as e:
        await ctx.send_response(f"⚠️ An internal error has occurred: {str(e)}", ephemeral=True)
        raise e


@config.command(name="team_size", description="Set the number of players that need to join a widget.")
async def set_team_size(
    ctx: discord.ApplicationContext,
    team_size: discord.Option(
        int, "The number of players that need to join a widget", min_value=1)
):
    try:
        try:
            captain = captains_db.get(Query().guild == ctx.guild_id)['captain']
        except TypeError:
            captain = None
        if ctx.author.id == ctx.guild.owner_id or ctx.author_id == captain:
            captains_db.upsert(
                {'guild': ctx.guild_id, 'team_size': team_size}, Query().guild == ctx.guild.id)
            await ctx.send_response(f"✅ Team size set to {team_size}", ephemeral=True)
        else:
            await ctx.send_response(f"⛔ Only the guild owner or current Captain is allowed to set the team size.")
    except Exception as e:
        await ctx.send_response(f"An internal error has occurred: {str(e)}", ephemeral=True)
        raise e


admin = discord.SlashCommandGroup(
    name="admin", description="Administative commands", guild_ids=[secrets["admin_console_guild"]])


@admin.command(name="announce", description="Make an announcement to all guilds the bot is installed in.")
async def admin_announce(
    ctx: discord.ApplicationContext,
    message: discord.Option(str, "The message to broadcast")
):
    view = Confirm()
    if ctx.author.id == secrets['admin_user_id']:
        await ctx.send_response(f"""Are you sure you want to announce this to all guilds this bot is installed in?
>>> {message}""", view=view)
        await view.wait()
        if view.value is None:
            await ctx.send_followup("Confirmation timed out.")
        elif view.value:
            await ctx.send_followup("Broadcasting announcement...")
            successes = 0
            for guild in bot.guilds:
                try:
                    await guild.system_channel.send(f"""**An announcement from <@{secrets['admin_user_id']}>:**
>>> {message}""")
                except discord.Forbidden:
                    for channel in guild.text_channels:
                        try:
                            await channel.send(f"""**An announcement from <@{secrets['admin_user_id']}>:**
>>> {message}""")
                        except discord.Forbidden:
                            pass

                        else:
                            successes += 1
                            break
                else:
                    successes += 1
            await ctx.send_followup(f"Broadcasted message to {successes} of {len(bot.guilds)} guilds.")
        else:
            await ctx.send_followup("Cancelled.")
    else:
        await ctx.send_response("⛔ You do not have permission to use administrative commands.")


@admin.command(guild_ids=[secrets['admin_console_guild']])
async def guild_owner(ctx: discord.ApplicationContext, guild_id: str):
    await ctx.send_response(bot.get_guild(int(guild_id)).owner_id)


@bot.event
async def on_message(message: discord.Message):
    try:
        if message.author.id == bot.user.id:  # Don't reply to your own message!
            return
        if bot.user not in message.mentions:  # Only reply to messages which mention the bot
            return
        event: Event = Event(required_players=captains_db.get(
            Query().guild == message.guild.id)['team_size'])
        event.message = await message.reply("📢 Okay, who's available?", view=event.view, embed=event.to_embed())

    except Exception as e:
        await message.reply(f"⚠️ An internal error has occurred: {str(e)}")
        raise e


@bot.event
async def on_guild_join(guild: discord.Guild):
    captains_db.upsert({'guild': guild.id,
                        'captain': guild.owner_id,
                        'team_size': 4},
                       Query().guild == guild.id)
    message = f"""Thanks for trying out Avail! I'm a free and open-source bot that enables teams to get RSVPs for tournaments and other events!
Use /help for more information about me. Since <@{guild.owner_id}> is the owner of this guild, they have been set as the Captain by default.
The guild owner or current Captain can change settings like re-assigning the Captain or setting the team size for their guild with the /config commands.
Found a bug? Want to help me improve? Or just curious about how I work? Check out my GitHub repo at https://github.com/M1N0RM1N3R/Avail
"""
    try:
        await guild.system_channel.send(message)
    except discord.Forbidden:
        for channel in guild.text_channels:
            try:
                channel.send(message)
            except discord.Forbidden:
                pass
            else:
                break

bot.add_application_command(config)
bot.add_application_command(admin)
bot.run(secrets['discord_bot_token'])
