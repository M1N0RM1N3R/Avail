import json
from typing import List
import discord
from tinydb import TinyDB, Query

secrets = json.loads(open('secrets.json', 'r').read())
captains_db = TinyDB('captains_db.json')

class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value
    # to `True` and stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
    async def confirm_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Confirming", ephemeral=True)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`.
    @discord.ui.button(label="Cancel", style=discord.ButtonStyle.grey)
    async def cancel_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.response.send_message("Cancelling", ephemeral=True)
        self.value = False
        self.stop()

class AvailabilityButtons(discord.ui.View):
    def __init__(self, parent: 'Event'):
        super().__init__(timeout=None)
        self.parent_event: 'Event' = parent
    
    @discord.ui.button(label="I'm available", style=discord.ButtonStyle.primary, emoji="✅")
    async def add_available(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id not in self.parent_event.available_players:
            self.parent_event.available_players.append(interaction.user.id)
            discord.embed = self.parent_event.to_embed()
            await interaction.message.edit(embed=discord.embed)
            await interaction.response.send_message("✅ Marked as available.", ephemeral=True)
            if len(self.parent_event.available_players) >= self.parent_event.required_players and not self.parent_event.already_pinged_captain:
                await interaction.message.reply(f"Hey <@{captains_db.get(Query().guild == interaction.guild_id)['captain']}>! This event has enough available players!")
                self.parent_event.already_pinged_captain = True
        else:
            await interaction.response.send_message("❌ You are already marked as available.", ephemeral=True)
    
    @discord.ui.button(label="Cancel availability", style=discord.ButtonStyle.gray, emoji="❌")
    async def remove_available(self, button: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user.id in self.parent_event.available_players:
            self.parent_event.available_players.remove(interaction.user.id)
            discord.embed = self.parent_event.to_embed()
            await interaction.message.edit(embed=discord.embed)
            await interaction.response.send_message("✅ Unmarked as available.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ You are not marked as available.", ephemeral=True)

class Event:
    def __init__(self, **kwargs):
        self.available_players: List[int] = kwargs.pop('available_players', [])
        self.required_players: int = kwargs.pop('required_players', 1)
        self.view = kwargs.pop('view', AvailabilityButtons(self))
        self.already_pinged_captain = kwargs.pop('already_pinged_captain', False)
    
    def to_embed(self) -> discord.Embed:
        embed: discord.Embed = discord.Embed()
        needed_players = max(self.required_players - len(self.available_players), 0)
        for k, v in {
            'Available players': ", ".join([f"<@{p}>" for p in self.available_players]) if self.available_players else "None",
            'Required players': f"{needed_players} more player{'s' if needed_players != 1 else ''} needed",
        }.items():
            embed.add_field(name=k, value=v, inline=False)
        return embed