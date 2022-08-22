# About Avail
Avail is a simple FOSS Discord bot based on Pycord and TinyDB for teams to make sure they have enough players to participate in an event.
Driven by the frustration from missing out on Low Ink August 2022 when two of my teammates dipped, I harnessed my Python programming skills to create the original version of Avail in under 24 hours.
Since then, I have added support for multiple guilds on one instance via TinyDB.

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
