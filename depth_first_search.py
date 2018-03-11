from math import sqrt
from random_traversal import generate_random_traversal
from depth_first_gen import depth_first_gen
from timeit import default_timer
from enum import Enum 

from maze_tools import load_maze, print_maze, check_bounds, paint_solution_manhattan, zoom_bitmaze

def depth_first_search(path):
	start_time = default_timer()
	maze, (width, heigth) = load_maze(path)
	start = maze[:width].index(1)
	finish = maze[-width:].index(1)+(width*(heigth-1))
	maze_path = [start, start+width]
	dead_ends = []
	print_path = 1
	print("This may take a while...")
	pathing = list(map(lambda x : x, maze))
	while maze_path[-1] != finish:
		a = maze_path[-1]

		pathing[a] = 2

		# TRY RIGHT
		if check_bounds(a, +1, width) and a%width < (a+1)%width and maze[a+1] and (a+1) not in maze_path and (a+1) not in dead_ends:
			maze_path.append(a+1)
			continue
		# TRY DOWN
		if check_bounds(a, +width, width) and (a+width) and maze[a+width] and (a+width) not in maze_path and (a+width) not in dead_ends:
			maze_path.append(a+width)
			continue
		# TRY LEFT
		if check_bounds(a, -1, width) and a%width > (a-1)%width and maze[a-1] and (a-1) not in maze_path and (a-1) not in dead_ends:
			maze_path.append(a-1)
			continue
		# TRY UP
		if check_bounds(a, -width, width) and (a-width) and maze[a-width] and (a-width) not in maze_path and (a-width) not in dead_ends:
			maze_path.append(a-width)
			continue
		
		dead_ends.append(maze_path.pop())
		
		pathing[a] = 1

	pathing[finish] = 2
	pathing[start] = 2
	elapsed_time = default_timer() - start_time
	#print_maze(pathing, width)
	#print(maze_path)
	print("Maze path length : {}".format(len(maze_path)))
	print("Elapsed time solving maze : {}".format(elapsed_time))
	paint_solution_manhattan(pathing, width, heigth, 30, path, n_colors=len(maze_path))
	zoom_bitmaze(path, 30)


if __name__ == '__main__' :
	import os
	try:
		os.makedirs('depth_first_search_examples')
	except:
		pass
	print('Random Traversal Maze')
	traversal_path = os.path.join('depth_first_search_examples', 'search_random_traversal.bmp')
	depth_first_gen_path = os.path.join('depth_first_search_examples', 'search_depth_first_gen.bmp')
	generate_random_traversal(50, paint=True, name=traversal_path)
	depth_first_search(traversal_path)
	print('\nDepth First Maze')
	depth_first_gen(50, paint=True, name=depth_first_gen_path)
	depth_first_search(depth_first_gen_path)