import discord
from discord.ext import commands
import json
from discord.ext.commands import MissingPermissions


class ModMail(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.file_name = "ModMail_file.json"
        with open(self.file_name, 'r') as f:
            self.modMail_data = json.load(f)

    @commands.Cog.listener()
    async def on_ready(self):

        if self.modMail_data == {}:
            self.modMail_data = {'channel': 0,
                                 'users': []}

            with open(self.file_name, 'w') as f:
                json.dump(self.modMail_data, f, indent=4)

            print('file was updated')

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.author == self.bot.user:
            return

        if self.modMail_data['channel']:
            if message.guild is None:
                if message.author.id not in self.modMail_data['users']:
                    channel = self.bot.get_channel(
                        self.modMail_data['channel']
                    )
                    attachments = '\n'.join(file.url for file in message.attachments)

                    await channel.send(f"**[{str(message.author)},"
                                       f" id: {message.author.id}]"
                                       f": ** {message.content}"
                                       f"\n{attachments}")
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True,
                              manage_channels=True)
    async def block_user(self, ctx,
                         member: discord.Member = None):

        if member is None:
            await ctx.send("Member wasn't mentioned",
                           delete_after=10)
            return

        self.modMail_data['users'].append(member.id)

        with open(self.file_name, 'w') as f:
            json.dump(self.modMail_data, f, indent=4)

        await ctx.send(f"Messages won't be received from {str(member)}", delete_after=3)

    @block_user.error
    async def block_user_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Required Permission to block a member:"
                           " `manage_channels` and `manage_messages`", delete_after=10)
        else:
            raise error

    @commands.command()
    @commands.has_permissions(manage_messages=True,
                              manage_channels=True)
    async def unblock_user(self, ctx,
                           member: discord.Member = None):
        if member is None:
            await ctx.send("Member wasn't mentioned",
                           delete_after=10)
            return

        if member.id not in self.modMail_data['users']:
            await ctx.send("User isn't blocked", delete_after=10)
            return

        self.modMail_data['users'].remove(member.id)

        with open(self.file_name, 'w') as f:
            json.dump(self.modMail_data, f, indent=4)

        await ctx.send("User was successfully unblocked",
                       delete_after=10)

    @unblock_user.error
    async def unblock_user_erro(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Required Permission to unblock a member:"
                           " `manage_channels` and `manage_messages`", delete_after=10)
        else:
            raise error

    @commands.command()
    @commands.has_permissions(manage_messages=True,
                              manage_channels=True)
    async def set(self, ctx, channel: discord.TextChannel = None):
        if channel is None:
            return await ctx.send("Provide the mod_mail channel", delete_after=10)

        self.modMail_data['channel'] = channel.id

        with open(self.file_name, 'w') as f:
            json.dump(self.modMail_data, f, indent=4)

        await ctx.send(f"Mod mail has been set"
                       f" in {channel.name}", delete_after=10)

    @set.error
    async def set_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Required Permission to set the mod mail:"
                           " `manage_channels` and `manage_messages`", delete_after=10)
        else:
            raise error

    @commands.command()
    @commands.has_permissions(manage_messages=True,
                              manage_channels=True)
    async def remove(self, ctx):
        self.modMail_data = {'channel': 0, 'users': []}

        with open(self.file_name, 'w') as f:
            json.dump(self.modMail_data, f, indent=4)

        await ctx.send("Mod mail was removed",
                       delete_after=5)

    @remove.error
    async def remove_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Required Permission to remove the mod mail:"
                           " `manage_channels` and `manage_messages`", delete_after=10)
        else:
            raise error

    @commands.command()
    @commands.has_permissions(manage_messages=True,
                              manage_channels=True)
    async def message_member(self, ctx,
                             member: discord.Member = None, *,
                             message: str = None):

        if member is None:
            return await ctx.send("Member wasn't mentioned", delete_after=10)

        if message is None:
            return await ctx.send("Message wasn't passed", delete_after=10)

        if not self.modMail_data['channel']:
            return await ctx.send("Mod mail is disabled", delete_after=10)

        if ctx.channel.id != self.modMail_data['channel']:
            return await ctx.send("Send the message in the chosen channel", delete_after=10)

        try:
            await member.send(f"**Staff: **{message}")
        except discord.Forbidden:
            await ctx.send("```diff\n-Something wrong occurred in sending the message```", delete_after=20)

    @message_member.error
    async def message_member_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("Required Permission to message a member:"
                           " `manage_channels` and `manage_messages`", delete_after=10)
        else:
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(ModMail(bot))
