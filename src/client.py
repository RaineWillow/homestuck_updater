import discord
import asyncio
import feedparser

class HomestuckUpdater(discord.Client):

	def __init__(self, url, data):
		super(HomestuckUpdater, self).__init__()

		self.version = "ver 0.03"

		self.url = url
		self.channel = None
		self.msg = None
		self.updating = True
		self.data = data

		self.embed = discord.Embed(title="Newest Update", description=self.data['l_update_name'] + " ==> " + self.data['l_update_url'], color=0x0000FF)
		self.embed.add_field(name="Last Update: ", value=self.data['l_update_time'], inline=False)
		self.embed.add_field(name="Number of pages: ", value=str(int(self.data['l_update_last']) - int(self.data['l_update_start'])), inline=False)

	@asyncio.coroutine
	def on_ready(self):
		print('Logged in as:')
		print(self.user.name)
		print(self.user.id)

	@asyncio.coroutine
	def background_loop(self):
		while (not self.is_closed()) and self.updating:
			#feed = feedparser.parse(url)
			#sorted_entries = sorted(feed['entries'], key=lambda entry: int(entry[key]),  reverse=True)
			#yield from self.msg.edit(content="ver 0.03", embed=self.embed)
			yield from asyncio.sleep(5)

	@asyncio.coroutine
	def on_message(self, message):
		if self.user.mentioned_in(message):
			yield from message.delete()
			if message.content.split(' ')[1] == "init":
				self.channel = message.channel
				self.msg = yield from self.channel.send("ver 0.03", embed=self.embed)
				asyncio.ensure_future(self.background_loop())
