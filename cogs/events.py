import discord
from discord.ext import commands
import utils.response

SPAM_LIMIT = 4

class EventHandlerCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.message_counts = {}

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.client.user:
            return
        
        author_id = message.author.id
        self.message_counts[author_id] = self.message_counts.get(author_id, 0) + 1

        if self.message_counts[author_id] > SPAM_LIMIT:
            # TODO: Store number of warns of each user and take action on them.
            await message.reply(f"{message.author.mention} Please refrain from flooding the channel with messages.")

        if 'hello' in message.content.lower():
            await message.channel.send(utils.response.get_random_greeting())
    
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