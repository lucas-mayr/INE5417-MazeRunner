import psycopg2 as db

class LeaderBoard:
	def __init__(self, dbname, user, password, host='localhost', size=10):
		self.size = size
		self.conn = db.connect(dbname=dbname, user=user, password=password, host=host)
		self.cursor = self.conn.cursor()
		self.rank = ''
		self.__load_file()



	def __load_file(self):
		try:
			self.cursor.execute("SELECT * FROM LEADERBOARD;")
		except Exception as e:
			print(e)
			self.conn.rollback()
			self.clear_rankings()
		self.rank = self.prepare_list(self.cursor.fetchall())

	def clear_rankings(self):
		try:
			self.cursor.execute('DROP TABLE LEADERBOARD;')
		except Exception as e:
			self.conn.rollback()
			print(e)

		self.cursor.execute('CREATE TABLE LEADERBOARD (id serial PRIMARY KEY,name text, points integer);')
		for i in range(self.size):
			self.cursor.execute('INSERT INTO LEADERBOARD (name, points) VALUES (%s, %s);',("AAA", 0))
		self.conn.commit()
		self.__load_file()

	def rankings(self):
		return self.rank

	def prepare_list(self, lista):
		return [(nome, points) for _,nome,points in lista]


	def add_player(self, stats):
		for i, stat in enumerate(self.rank):
			if stats[1] > stat[1]:
				self.rank.insert(i, stats)
				self.rank.pop()
				self.update_rankings(self.rank)
				break

	def update_rankings(self, new_rankings):
		for i, content in enumerate(new_rankings):
			self.cursor.execute('UPDATE LEADERBOARD SET name=(%s), points=(%s) WHERE id=(%s);',(content[0], content[1], i+1))
		self.conn.commit()
		self.__load_file()


	def check_ranking(self, points):
		return points > self.rank[-1][1]


if __name__ == '__main__':
	l = LeaderBoard("MazeRunner", "postgres", "postgres")
	print(l.rankings())
	l.add_player(["ASS", 123])
	print(l.rankings())
	# pri = lambda : print("\n".join(map(str, l.rankings())))