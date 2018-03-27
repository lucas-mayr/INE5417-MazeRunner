import os

from random import choice
from timeit import default_timer
 
class Maze:
	def __init__(self, side, name='Default'):
		self.name = name
		self.side = side
		self.size = side*side
		self.start = 1
		self.exit = None
		self.maze = self.template_maze()
		self.pathing = None

	def copy_array(self):
		return [i for i in self.maze]

	def template_maze(self):
		self.maze = [None]*(self.side*self.side)
		for i in range(self.side):
			for j in range(self.side):
				if i%self.side == 0 or i%self.side == (self.side-1) or j%self.side == (self.side-1) or j == 0:
					self.maze[i + j*self.side] = 0
		return self.maze

	def check_bounds(self, ind, offset):
		line = ind//self.side
		ans = (ind+offset > 0)
		ans = ans and (ind+offset < self.side*self.side)
		return ans

	def print_maze(self):
		print("|-"*self.side + "|")
		for i, slot in enumerate(self.maze):
			print(slot, end=' ')
			if ((i+1)%(self.side) == 0):
				print("")
		print("|-"*self.side + "|")

	def print_solution(self):
		if not self.pathing:
			return
		print("|-"*self.side + "|")
		for i, slot in enumerate(self.pathing):
			print(slot, end=' ')
			if ((i+1)%(self.side) == 0):
				print("")
		print("|-"*self.side + "|")

	def check_end(self, position):
		return position == self.exit

	def generate_new_maze(self, name=None):
		actual_name = name or self.name 

		start_time = default_timer()

		maze_next = set([self.start])
		maze_temp = set()

		progress = 0;
		try:
			while None in self.maze:
				if not maze_temp:
					a = choice(list(maze_next))
				else:
					a = choice(list(maze_temp))

				maze_temp = set()
				b = 0
				# LEFT SLOT
				if self.check_bounds(a, -1) and a%self.side > (a-1)%self.side:
					if self.maze[a - 1]:
						b += 1
					if self.maze[a - 1] is None :
						maze_temp.add(a-1)
				# RIGHT SLOT
				if self.check_bounds(a, +1) and a%self.side < (a+1)%self.side:
					if self.maze[a + 1]:
						b += 1
					if self.maze[a +  1] is None :
						maze_temp.add(a+1)
				# UPPER SLOT
				if self.check_bounds(a, -self.side):
					if self.maze[a - self.side]:
						b += 1
					if self.maze[a - self.side] is None :
						maze_temp.add(a-self.side)
				# DOWN SLOT
				if self.check_bounds(a, +self.side):
					if self.maze[a + self.side]:
						b += 1
					if self.maze[a + self.side] is None :
						maze_temp.add(a+self.side)

				self.maze[a] = 1 if b < 2 else 0

				if self.maze[a]:
					maze_next = maze_next | maze_temp
				else:
					maze_temp = set()
				
				maze_next.remove(a)


				progress += 100
				print("Generating Maze...",progress//self.size, "%\r", end='')

		except IndexError:
				for i, slot in enumerate(self.maze):
					if slot is None:
						self.maze[i]  = 0
		print("Generating Maze... 100%")
		
		end = [i+(self.side*(self.side-2)) for i, v in enumerate(self.maze[-self.side*2:-self.side]) if v == 1][-1]
		self.maze[self.start] = 1
		self.maze[end+self.side] = 1
		self.exit = end+self.side
		elapsed_time = default_timer() - start_time

		print("Elapsed time generating Maze : {}".format(elapsed_time))

	def solve_maze(self):
		start_time = default_timer()
		maze_path = [self.start, self.start+self.side]
		dead_ends = []
		print("Solving Maze\nThis may take a while...")
		self.pathing = list(map(lambda x : x, self.maze))
		while maze_path[-1] != self.exit:
			a = maze_path[-1]

			self.pathing[a] = 2

			# TRY RIGHT
			if self.check_bounds(a, +1) and a%self.side < (a+1)%self.side and self.maze[a+1] and (a+1) not in maze_path and (a+1) not in dead_ends:
				maze_path.append(a+1)
				continue
			# TRY DOWN
			if self.check_bounds(a, +self.side) and (a+self.side) and self.maze[a+self.side] and (a+self.side) not in maze_path and (a+self.side) not in dead_ends:
				maze_path.append(a+self.side)
				continue
			# TRY LEFT
			if self.check_bounds(a, -1) and a%self.side > (a-1)%self.side and self.maze[a-1] and (a-1) not in maze_path and (a-1) not in dead_ends:
				maze_path.append(a-1)
				continue
			# TRY UP
			if self.check_bounds(a, -self.side) and (a-self.side) and self.maze[a-self.side] and (a-self.side) not in maze_path and (a-self.side) not in dead_ends:
				maze_path.append(a-self.side)
				continue
			
			dead_ends.append(maze_path.pop())
			
			self.pathing[a] = 1

		self.pathing[self.exit] = 2
		self.pathing[self.start] = 2
		elapsed_time = default_timer() - start_time

		print("maze path length : {}".format(len(maze_path)))
		print("Elapsed time solving maze : {}".format(elapsed_time))

if __name__ == "__main__" :
	try:
		os.makedirs("Examples")
	except:
		pass
	example_maze = Maze(15, name=os.path.join('Examples','depth_first.bmp'))
	example_maze.generate_new_maze()
	example_maze.print_maze()
	example_maze.solve_maze()