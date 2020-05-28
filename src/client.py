import discord
import asyncio
import feedparser
import pprint
from utils.json_reader import *

class HomestuckUpdater(discord.Client):

	def __init__(self):
		super(HomestuckUpdater, self).__init__()

		self.jsonHandle = JsonReader()

		self.version = "ver 0.03"

		self.channel = []
		self.updating = True
		self.role = None

		self.url = self.jsonHandle.getUrl()
		self.data = self.jsonHandle.getData()
		self.passw = self.jsonHandle.getPass()

		self.embed = self.get_embed()

	def get_embed(self):
		embd = discord.Embed(title="Newest Update", description=self.data['l_update_name'] + " ==> " + self.data['l_update_url'], color=0x0000FF)
		embd.add_field(name="Last Update: ", value=self.data['l_update_time'], inline=False)
		embd.add_field(name="Number of pages: ", value=str(int(self.data['l_update_last']) - int(self.data['l_update_start']) + 1), inline=False)
		return embd

	@asyncio.coroutine
	def on_ready(self):
		print('Logged in as:')
		print(self.user.name)
		print(self.user.id)

	@asyncio.coroutine
	def background_loop(self):
		while (not self.is_closed()) and self.updating:
			try:

				feed = feedparser.parse(self.url)
				sorted_entries = sorted(feed['entries'], key=lambda entry: int(entry['title']),  reverse=True)

				if (feed['bozo'] == 1):
					print(feed['bozo_exception'])

				if (int(sorted_entries[0]['title']) != int(self.data['l_update_last'])):
					self.data['l_update_start'] = str(int(self.data['l_update_last']) + 1)
					first_page_loc = 0 + (int(sorted_entries[0]['title']) - int(self.data['l_update_start']))

					self.data['l_update_time'] = sorted_entries[first_page_loc]['published']
					self.data['l_update_name'] = sorted_entries[first_page_loc]['summary']
					self.data['l_update_url'] = sorted_entries[first_page_loc]['link']
					self.data['l_update_last'] = sorted_entries[0]['title']

					self.jsonHandle.writeData(self.data)

					self.embed = self.get_embed()

					#yield from self.msg.delete()
					for mchannel in self.channel:
						yield from mchannel.send("New Homestuck Content! " + str(self.role), embed=self.embed)

			except Exception as e:
				print("Unable to access feed: ")
				print(e)

			yield from asyncio.sleep(1800)

	@asyncio.coroutine
	def on_message(self, message):
		if self.user.mentioned_in(message):
			commands = message.content.split(' ')

			if (commands[1] == self.passw):
				yield from message.delete()
				if (commands[2] == "init"):
					self.channel.append(message.channel)
					self.role = message.guild.default_role
					try:
						if (commands[3] == "out"):
							yield from message.channel.send("New Homestuck Content! " + str(self.role), embed=self.embed)
					except Exception as e:
						pass
					asyncio.ensure_future(self.background_loop())
