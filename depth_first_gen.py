import os

from sys import argv
from random import randint, choice
from timeit import default_timer

from maze_tools import template_maze, check_bounds

def depth_first_gen(_side, prints=False, paint=False, name='Default'):
	start_time = default_timer()
	side = _side+2
	size = side*side
	maze = template_maze(side)
	progress = 0;
	start = side+1
	maze_next = set([start])
	maze_temp = set()

	try:
		while None in maze:
			if not maze_temp:
				a = choice(list(maze_next))
			else:
				a = choice(list(maze_temp))

			maze_temp = set()
			b = 0
			# LEFT SLOT
			if check_bounds(a, -1, side) and a%side > (a-1)%side:
				if maze[a - 1]:
					b += 1
				if maze[a - 1] is None :
					maze_temp.add(a-1)
			# RIGHT SLOT
			if check_bounds(a, +1, side) and a%side < (a+1)%side:
				if maze[a + 1]:
					b += 1
				if maze[a +  1] is None :
					maze_temp.add(a+1)
			# UPPER SLOT
			if check_bounds(a, -side, side):
				if maze[a - side]:
					b += 1
				if maze[a - side] is None :
					maze_temp.add(a-side)
			# DOWN SLOT
			if check_bounds(a, +side, side):
				if maze[a + side]:
					b += 1
				if maze[a + side] is None :
					maze_temp.add(a+side)

			#maze[a] = 1 if b < 2 else choice([0]*50 + [1]) #Chance of multiple Paths
			maze[a] = 1 if b < 2 else 0

			from maze_tools import print_maze

			if maze[a]:
				maze_next = maze_next | maze_temp
			else:
				maze_temp = set()
			
			maze_next.remove(a)


			progress += 100
			print("Generating maze...",progress//size, "%\r", end='')

			#print_maze(maze, side)

			#input(">> Next\n")
	except IndexError:
			for i, slot in enumerate(maze):
				if slot is None:
					maze[i]  = 0
	#print_maze(maze, side)
	print("Generating maze... 100%")
	
	end = [i+(side*(side-2)) for i, v in enumerate(maze[-side*2:-side]) if v == 1][-1]
	maze[start-side] = 1
	maze[end+side] = 1
	elapsed_time = default_timer() - start_time

	print("Elapsed time generating maze : {}".format(elapsed_time))

	if paint:
		from maze_tools import paint_maze
		paint_maze(maze, side, name)
	if prints:
		from maze_tools import print_maze
		print_maze(maze, side)

	return maze


if __name__ == "__main__" :
	try:
		os.makedirs("Examples")
	except:
		pass
	depth_first_gen(15, name=os.path.join('Examples','depth_first.bmp'), paint=True)
	from maze_tools import zoom_bitmaze
	zoom_bitmaze(os.path.join('Examples','depth_first.bmp'), 20)