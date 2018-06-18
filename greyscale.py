import maze
from PIL import Image, ImageDraw
import time
from sys import argv

def print_maze(side, mymaze):
    print("|-" * side + "|")
    for i, slot in enumerate(mymaze):
        print(slot, end=' ') if slot is not None else print('X', end=' ')
        if (i + 1) % (side) == 0:
            print("")
    print("|-" * side + "|")

def draw_polygon(size, draw, ind, block_size, color):
        draw.polygon([(ind % size) * block_size,
                      (ind // size) * block_size,
                      (ind % size) * block_size + block_size,
                      (ind // size) * block_size,
                      (ind % size) * block_size + block_size,
                      (ind // size) * block_size + block_size,
                      (ind % size) * block_size,
                      (ind // size) * block_size + block_size],
                     fill=color)

def paint_solution_manhattan(array, size, block_size, path):
        start_time = time.time()
        img = Image.new(
            'L',
            (size * block_size,
             size * block_size),
            color=255)
        draw = ImageDraw.Draw(img)
        for i,v in enumerate(array):
            draw_polygon(size, draw, i, block_size, 255-v)
            print("Painting solution... {}%".format((i*100)//(len(array)+1)),end='\r')

        print("Painting solution... 100%")
        img.save("{}.bmp".format(path), quality=100, subsampling=0)
        elapsed_time = time.time() - start_time
        print("Elapsed time painting solution : {}".format(elapsed_time))

def main(side):
	maze_ = maze.Maze(side)
	mazeSum = [0]*(side*side)

	for i in range(255):
		maze_.generate_new_maze()
		maze_.solve_maze()
		mazeSum = [mazeSum[i] + (1 if v==2 else 0) for i,v in enumerate(maze_.pathing)]
		print("Working... {}%".format((i*100)//255),end='\r')
	print()

	#print_maze(SIDE, mazeSum)
	paint_solution_manhattan(mazeSum, side, 15, "grey_scale")


if __name__ == "__main__":
	try:
		main(int(argv[1]))
	except (ValueError, IndexError):
		print("Usage is: python3 {} line_size".format(argv[0]))
