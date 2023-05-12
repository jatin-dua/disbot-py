import discord
from discord.ext import commands
import utils.response

class GeneralCog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(name='ping')
    async def ping(self, ctx):
        await ctx.send("pong!")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Game("Chess"))
        print(f'We have logged in as {self.client.user}')
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author == self.client.user:
            return
        if 'hello' in message.content.lower():
            await message.channel.send(utils.response.get_random_greeting())

async def setup(client: commands.Bot):
    await client.add_cog(GeneralCog(client))
