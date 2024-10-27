import os
import json
import asyncio
import discord
from discord.ext import commands
from discord.ui import Button, View
from dhooks import Webhook, Embed
import requests

with open("config.json", "r") as f:
    config = json.load(f)

bot = commands.Bot(command_prefix=";", intents=discord.Intents.all())

category_id = config["role-access-category"]
vanity = config["vanity"]
sellersrole = config["role-id"]
utoken = config["user-token"]
fixed_channel_id = config["fixed-channel-id"]
message_id = config.get("message-id")  

async def send_logs(url: str, embed: bool, content: str):
    webhook = Webhook(url=url)
    if embed:
        embed = Embed(title="New Log", description=content)
        webhook.send(embed=embed)
    else:
        webhook.send(content=content)

class RoleButton(Button):
    def __init__(self, role_id, category_id):
        super().__init__(label="🎉 Click Me to Get Role", style=discord.ButtonStyle.primary, custom_id="role_button")
        self.role_id = role_id
        self.category_id = category_id

    async def callback(self, interaction: discord.Interaction):
        member = interaction.user
        guild = interaction.guild
        category = discord.utils.get(guild.categories, id=self.category_id)
        if category is None:
            await interaction.response.send_message("Category not found.", ephemeral=True)
            return
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),  
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),
        }

        for role in guild.roles:
            if role.permissions.administrator:
                overwrites[role] = discord.PermissionOverwrite(read_messages=True, send_messages=True)
        channel = await category.create_text_channel(f"{member.name}-role", overwrites=overwrites)
        await interaction.response.send_message(f"Channel {channel.mention} created!", ephemeral=True)

        headers = {"Authorization": f"{utoken}", "Content-Type": "application/json"}
        try:
            r = requests.get(f'https://discord.com/api/v9/users/{member.id}/profile', headers=headers)
            r.raise_for_status()
            profile = r.json()
        except requests.RequestException as e:
            await channel.send(f"Error fetching profile: {e}")
            await channel.delete()
            return

        bio = profile.get("user_profile", {}).get("bio", "")
        if vanity in bio:
            role = discord.utils.get(guild.roles, id=self.role_id)
            if role:
                await member.add_roles(role)
                await send_logs(config["role-webhook"], True, f"{member.mention} assigned seller role.")
                await channel.send(f"{member.mention}, you have been given the seller role.")
            else:
                await channel.send("Failed to assign role. Role not found.")
        else:
            await channel.send(f"{member.mention}, your bio doesn't contain the required vanity `{vanity}`.")
        await asyncio.sleep(5)
        await channel.delete()

class RoleView(View):
    def __init__(self, role_id, category_id):
        super().__init__(timeout=None)  
        self.add_item(RoleButton(role_id, category_id))


async def check_and_send_role_message():
    channel = bot.get_channel(fixed_channel_id)
    if not channel:
        print(f"Fixed channel with ID {fixed_channel_id} not found.")
        return

    if message_id:
        try:
            msg = await channel.fetch_message(message_id)
            if msg:
                print(f"Message with button already exists (ID: {message_id})")
                return
        except discord.NotFound:
            pass  

    embed = discord.Embed(
        title="Get Your Role!",
        description="Click the button below to get your seller role!",
        color=discord.Color.blue()
    )

    sellers_role_id = config["role-id"]
    view = RoleView(sellers_role_id, category_id)
    msg = await channel.send(embed=embed, view=view)

    config["message-id"] = msg.id
    with open("config.json", "w") as f:
        json.dump(config, f, indent=4)
    print(f"Message sent with ID: {msg.id}")

@bot.event
async def on_ready():
    await check_and_send_role_message()
    sellers_role_id = config["role-id"]
    bot.add_view(RoleView(sellers_role_id, category_id))  
    print(f"Logged in as {bot.user}")


bot.run(config["bot-token"])
