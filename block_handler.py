import time

class BlockHandler():
	def __init__(self, blockchain):
		self.blocks_to_process = []

	def add_to_process(self, block):
		stoped_server = len(self.blocks_to_process) <= 0
		self.blocks_to_process.append(block)

		if stoped_server:
			self.process()

	def process(self):
		while len(self.blocks_to_process) > 0:
			block = self.blocks_to_process.pop(0)
			print(block)
			time.sleep(0.5)

b_handler = BlockHandler()