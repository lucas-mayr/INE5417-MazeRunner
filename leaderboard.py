import json

class LeaderBoard:
	def __init__(self, path, size=10):
		self.size = size
		self.path = path

		try:
			self.__load_file()
		except Exception:
			self.clear_rankings()

	def __load_file(self):
		with open(self.path, 'r') as file:
			temp = json.load(file)
		return temp

	def clear_rankings(self):
		self.update_rankings([["***", 0]]*self.size)

	def rankings(self):
		return self.__load_file()

	def add_player(self, stats):
		leader_board = self.__load_file()
		for i, stat in enumerate(leader_board):
			if stats[1] > stat[1]:
				leader_board.insert(i, stats)
				leader_board.pop()
				self.update_rankings(leader_board)
				break

	def update_rankings(self, content):
		with open(self.path, 'w') as file:
	 		temp = json.dump(content, file)


	def check_ranking(self, points):
		with open(self.path, 'r') as file:
			temp = json.load(file)
		return points > temp[-1][1]


if __name__ == '__main__':
	l = LeaderBoard("test.json", 2)
	pri = lambda : print("\n".join(map(str, l.rankings())))