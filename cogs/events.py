import discord
from discord.ext import commands
from cogs.moderation import MODERATOR

class EventHandlerCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.client.user:
            return
        
        await MODERATOR.check_message_flood(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        # Check if the member's account is less than a day old
        if (discord.utils.utcnow() - member.created_at).days < 1:
            # Kick the member from the server
            await member.kick(reason='New account.')
            # Notify the moderators that a suspicious account has joined
            mod_channel = self.client.get_channel(1234567890) # Replace with your moderation channel ID
            await mod_channel.send(f'Suspicious account {member.mention} has joined the server.')


async def setup(client: commands.Bot):
    await client.add_cog(EventHandlerCog(client))