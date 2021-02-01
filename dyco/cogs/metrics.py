import time
import logging

from aioprometheus import Service, Registry, Counter, Gauge, Summary, Histogram
from discord.ext import tasks, commands


class Metrics(commands.Cog):
    """
    Exports metrics in Prometheus exposition format via HTTP on port 42069.
    """

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.service = Service()
        self.registry = Registry()

        self.events = Counter("events", "Discord API event counts.")
        self.registry.register(self.events)

        self.latency = Histogram("latency", "Discord API latency.")

        self.serve.start()  # pylint: disable=no-member
        self.update_latency.start()  # pylint: disable=no-member

    @tasks.loop()
    async def serve(self):
        self.service.start(port=42069)
        logging.info("Serving Prometheus metrics on: %s", self.service.metrics_url)

    @tasks.loop(minutes=1)
    async def update_latency(self):
        self.latency.observe({"seconds"}, self.bot.latency)

    @update_latency.before_loop
    async def before_update_latency(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.serve.cancel()  # pylint: disable=no-member
        self.update_latency.cancel()  # pylint: disable=no-member

    @commands.Cog.listener()
    async def on_connect(self):
        self.events.inc({"type": "connect"})

    @commands.Cog.listener()
    async def on_shard_connect(self, shard_id):
        self.events.inc({"type": f"shard_connect_{shard_id}"})

    @commands.Cog.listener()
    async def on_disconnect(self):
        self.events.inc({"type": "disconnect"})

    @commands.Cog.listener()
    async def on_shard_disconnect(self, shard_id):
        self.events.inc({"type": f"shard_disconnect_{shard_id}"})

    @commands.Cog.listener()
    async def on_ready(self):
        self.events.inc({"type": "ready"})

    @commands.Cog.listener()
    async def on_shard_ready(self, shard_id):
        self.events.inc({"type": f"shard_ready_{shard_id}"})

    @commands.Cog.listener()
    async def on_resumed(self):
        self.events.inc({"type": "resumed"})

    @commands.Cog.listener()
    async def on_shard_resumed(self, shard_id):
        self.events.inc({"type": f"shard_resumed_{shard_id}"})

    @commands.Cog.listener()
    async def on_error(self, event, *_):
        self.events.inc({"type": "error"})
        self.events.inc({"type": f"error_{event}"})

    @commands.Cog.listener()
    async def on_socket_raw_receive(self, *_):
        self.events.inc({"type": "socket_raw_receive"})

    @commands.Cog.listener()
    async def on_socket_raw_send(self, *_):
        self.events.inc({"type": "socket_raw_send"})

    @commands.Cog.listener()
    async def on_typing(self, *_):
        self.events.inc({"type": "typing"})

    @commands.Cog.listener()
    async def on_message(self, *_):
        self.events.inc({"type": "message"})

    @commands.Cog.listener()
    async def on_message_delete(self, *_):
        self.events.inc({"type": "message_delete"})

    @commands.Cog.listener()
    async def on_bulk_message_delete(self, *_):
        self.events.inc({"type": "bulk_message_delete"})

    @commands.Cog.listener()
    async def on_raw_message_delete(self, *_):
        self.events.inc({"type": "raw_message_delete"})

    @commands.Cog.listener()
    async def on_raw_bulk_message_delete(self, *_):
        self.events.inc({"type": "raw_bulk_message_delete"})

    @commands.Cog.listener()
    async def on_message_edit(self, *_):
        self.events.inc({"type": "message_edit"})

    @commands.Cog.listener()
    async def on_raw_message_edit(self, *_):
        self.events.inc({"type": "raw_message_edit"})

    @commands.Cog.listener()
    async def on_reaction_add(self, *_):
        self.events.inc({"type": "reaction_add"})

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, *_):
        self.events.inc({"type": "raw_reaction_add"})

    @commands.Cog.listener()
    async def on_reaction_remove(self, *_):
        self.events.inc({"type": "reaction_remove"})

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, *_):
        self.events.inc({"type": "raw_reaction_remove"})

    @commands.Cog.listener()
    async def on_reaction_clear(self, *_):
        self.events.inc({"type": "reaction_clear"})

    @commands.Cog.listener()
    async def on_raw_reaction_clear(self, *_):
        self.events.inc({"type": "raw_reaction_clear"})

    @commands.Cog.listener()
    async def on_reaction_clear_emoji(self, *_):
        self.events.inc({"type": "reaction_clear_emoji"})

    @commands.Cog.listener()
    async def on_raw_reaction_clear_emoji(self, *_):
        self.events.inc({"type": "raw_reaction_clear_emoji"})

    @commands.Cog.listener()
    async def on_private_channel_delete(self, *_):
        self.events.inc({"type": "private_channel_delete"})

    @commands.Cog.listener()
    async def on_private_channel_create(self, *_):
        self.events.inc({"type": "private_channel_create"})

    @commands.Cog.listener()
    async def on_private_channel_update(self, *_):
        self.events.inc({"type": "private_channel_update"})

    @commands.Cog.listener()
    async def on_private_channel_pins_update(self, *_):
        self.events.inc({"type": "private_channel_pins_update"})

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, *_):
        self.events.inc({"type": "guild_channel_delete"})

    @commands.Cog.listener()
    async def on_guild_channel_create(self, *_):
        self.events.inc({"type": "guild_channel_create"})

    @commands.Cog.listener()
    async def on_guild_channel_update(self, *_):
        self.events.inc({"type": "guild_channel_update"})

    @commands.Cog.listener()
    async def on_guild_channel_pins_update(self, *_):
        self.events.inc({"type": "guild_channel_pins_update"})

    @commands.Cog.listener()
    async def on_guild_channel_integrations_update(self, *_):
        self.events.inc({"type": "guild_channel_integrations_update"})

    @commands.Cog.listener()
    async def on_webhooks_update(self, *_):
        self.events.inc({"type": "webhooks_update"})

    @commands.Cog.listener()
    async def on_member_join(self, *_):
        self.events.inc({"type": "member_join"})

    @commands.Cog.listener()
    async def on_member_remove(self, *_):
        self.events.inc({"type": "member_remove"})

    @commands.Cog.listener()
    async def on_member_update(self, *_):
        self.events.inc({"type": "member_update"})

    @commands.Cog.listener()
    async def on_user_update(self, *_):
        self.events.inc({"type": "user_update"})

    @commands.Cog.listener()
    async def on_guild_join(self, *_):
        self.events.inc({"type": "guild_join"})

    @commands.Cog.listener()
    async def on_guild_remove(self, *_):
        self.events.inc({"type": "guild_remove"})

    @commands.Cog.listener()
    async def on_guild_update(self, *_):
        self.events.inc({"type": "guild_update"})

    @commands.Cog.listener()
    async def on_guild_role_create(self, *_):
        self.events.inc({"type": "guild_role_create"})

    @commands.Cog.listener()
    async def on_guild_role_delete(self, *_):
        self.events.inc({"type": "guild_role_delete"})

    @commands.Cog.listener()
    async def on_guild_role_update(self, *_):
        self.events.inc({"type": "guild_role_update"})

    @commands.Cog.listener()
    async def on_guild_emojis_update(self, *_):
        self.events.inc({"type": "guild_emojis_update"})

    @commands.Cog.listener()
    async def on_guild_available(self, *_):
        self.events.inc({"type": "guild_available"})

    @commands.Cog.listener()
    async def on_guild_unavailable(self, *_):
        self.events.inc({"type": "guild_unavailable"})

    @commands.Cog.listener()
    async def on_voice_state_update(self, *_):
        self.events.inc({"type": "voice_state_update"})

    @commands.Cog.listener()
    async def on_member_ban(self, *_):
        self.events.inc({"type": "member_ban"})

    @commands.Cog.listener()
    async def on_member_unban(self, *_):
        self.events.inc({"type": "member_unban"})

    @commands.Cog.listener()
    async def on_invite_create(self, *_):
        self.events.inc({"type": "invite_create"})

    @commands.Cog.listener()
    async def on_invite_delete(self, *_):
        self.events.inc({"type": "invite_delete"})

    @commands.Cog.listener()
    async def on_group_join(self, *_):
        self.events.inc({"type": "group_join"})

    @commands.Cog.listener()
    async def on_group_remove(self, *_):
        self.events.inc({"type": "group_remove"})

    @commands.Cog.listener()
    async def on_relationship_add(self, *_):
        self.events.inc({"type": "relationship_add"})

    @commands.Cog.listener()
    async def on_relationship_remove(self, *_):
        self.events.inc({"type": "relationship_remove"})

    @commands.Cog.listener()
    async def on_relationship_update(self, *_):
        self.events.inc({"type": "relationship_update"})
