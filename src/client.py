import discord
import asyncio

class HomestuckUpdater(discord.Client):

	def __init__(self):
		super(HomestuckUpdater, self).__init__()
		self.channel = None
		self.msg = None
		self.currNum = 0
		self.updating = True

	@asyncio.coroutine
	def on_ready(self):
		print('Logged in as:')
		print(self.user.name)
		print(self.user.id)

	@asyncio.coroutine
	def background_loop(self):
		while (not self.is_closed()) and self.updating:
			self.currNum += 1
			yield from self.msg.edit(content = str(self.currNum))
			yield from asyncio.sleep(1)

	@asyncio.coroutine
	def on_message(self, message):
		if self.user.mentioned_in(message):
			yield from message.delete()
			if message.content.split(' ')[1] == "init":
				self.channel = message.channel
				self.msg = yield from self.channel.send("0")
				asyncio.ensure_future(self.background_loop())
			elif message.content.split(' ')[1] == "clear":
				self.updating = False
				yield from self.msg.delete()
				self.msg = None
			elif message.content.split(' ')[1] == "start":
				if (self.updating == False):
					if (self.msg == None):
						self.msg = yield from self.channel.send("0")
					self.updating = True
					asyncio.ensure_future(self.background_loop())
			elif message.content.split(' ')[1] == "stop":
				self.updating = False
