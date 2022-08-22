# About Avail
Avail is a simple FOSS Discord bot based on Pycord and TinyDB for teams to make sure they have enough players to participate in an event.
Driven by the frustration from missing out on Low Ink August 2022 when two of my teammates dipped, I harnessed my Python programming skills to create the original version of Avail in under 24 hours.
Since then, I have added support for multiple guilds on one instance via TinyDB.

# How it works
- When Avail is added to a guild, it will automatically set the guild's owner as the Captain.
- Any user can @mention the bot and it will reply with an embed with two fields ("Available players" and "Required players") and a view with two buttons. ("I'm available" and "Cancel availability") Other users can add and remove their names to/from the "Available players" field by clicking the respective button. The "Required players" field displays how many more players are needed to fill out the roster, and updates as users add/remove themselves.
- When a roster fills up for the first time, the bot pings the Captain to notify them that enough players are available.

# Features
- Captains can set the team size and pass the baton to another user using the /config commands. The guild owner will always have access to these configuration features

# Setting up
Due to my extremely limited access to stable computing hardware and Internet bandwidth, I strongly encourage self-hosting Avail to help take the load off my poor little Dell Optiplex running the bot.
If you don't know how to set up your own Discord bot, there are plenty of tutorials you can find online.
You will need to create a secrets.json file in the same directory as the other files according to the following example:
```json
{
    "discord_bot_token": "nmyJ2wTM8q98uwnxzg3yBP2Z.ja9vvM.NWLqtKmQqGDthhS8jbVBbwSti7jMc5BFJmfrf8",
    "admin_user_id": 326762325363887583,
    "admin_console_guild": 953326896957368929
}
```
where `"discord_bot_token"` is your bot user's token from the [Discord Developer Portal](https://discord.com/developers/applications), `"admin_user_id"` is the admin's Discord user ID, and `"admin_console_guild"` is the guild (Discord server) in which the bot should add the admin commands.

# Potential new features
- Persistent Avail widgets
- Message context menu command with potential team size specification
- Language localizations
- Whatever else I haven't thought of
