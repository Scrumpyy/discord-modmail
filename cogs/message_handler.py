from nextcord.ext import commands

class ModMailMessageHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(ModMailMessageHandler(bot))