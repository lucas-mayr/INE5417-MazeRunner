import pygame
from depth_first_gen import depth_first_gen
from random import choice
from sys import exit
import time

COLORS = { 
	0 : (0, 0, 0),
	1 : (255, 255, 255),
	2 : (150, 150, 0),
	3 : (255, 0, 0),
	4 : (0, 255, 0),
	5 : (0, 0, 255)
	}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (150, 150, 0)

class PyManMain:

	def __init__(self, width=800,height=800, _size=10):
		pygame.init()
		self.font = pygame.font.SysFont(None, 32)
		self.clock = pygame.time.Clock()
		self._size = _size
		self.offset = 100
		self.width = width
		self.height = height
		self.screen = pygame.display.set_mode((self.width, self.height + self.offset))
		self.screen.fill(BLACK)


	def MainLoop(self):
		start_time = time.time()
		_directions = {
			pygame.K_UP : -self._size,
			pygame.K_DOWN : self._size,
			pygame.K_RIGHT : 1,
			pygame.K_LEFT : -1
			}
		grid = depth_first_gen(self._size-2)
		path = [i for i, v in enumerate(grid) if v == 1]
		current = path[0]
		_end = path[-1]
		while 1:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					exit(0)
				elif event.type == pygame.KEYDOWN:
					if current == _end:
						self._size += 10
						_directions = {
							pygame.K_UP : -self._size,
							pygame.K_DOWN : self._size,
							pygame.K_RIGHT : 1,
							pygame.K_LEFT : -1
							}
						grid = depth_first_gen(self._size-2)
						path = [i for i, v in enumerate(grid) if v == 1]
						current = path[0]
						_end = path[-1]
						self.screen.fill(BLACK)
						print(self._size)
					elif event.key == pygame.K_SPACE:
						grid[current] = 5

					else:
						try:
							next_current = current + _directions[event.key]
							if grid[next_current] != 0:
								grid[next_current] = 4
								grid[current] = 3 if grid[current] != 5 else 5
								current = next_current
						except Exception as err:
							print(err)

			for column in range(self._size):
				for row in range(self._size):
					color = COLORS[grid[self._size*column + row]]
					pygame.draw.rect(self.screen, color, 
					[(self.width//self._size) * row,
					(self.height//self._size) * column + self.offset,
					(self.width//self._size - 1), 
					(self.height//self._size - 1)])


			pygame.draw.rect(self.screen, BLACK, (0,0,self.width,self.offset))
			clock_text = self.font.render(time.strftime("%H:%M:%S",time.localtime()), 1, (255,255,255))
			points_text = self.font.render("{}".format(int(time.time() - start_time)), 1, (255,255,255))
			self.clock.tick(60)
			self.screen.blit(clock_text, (0,0))
			self.screen.blit(points_text, (0,20))
			pygame.display.flip()



if __name__ == "__main__":
	PyManMain().MainLoop()