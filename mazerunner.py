from sys import exit
import time
import string
import pygame


from PIL import Image, ImageDraw
from colour import Color

import maze
import leaderboard

COLORS = {
    0: (0, 0, 0),
    1: (255, 255, 255),
    2: (150, 150, 0),
    4: (255, 0, 0),
    3: (0, 255, 0),
    5: (0, 0, 255)
}

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (150, 150, 0)


class PyManMain:

    def __init__(self, width=480, height=480, _size=10, leader_size=10):
        pygame.init()
        self.leaderboard = leaderboard.LeaderBoard('test.json', leader_size)
        self.font = pygame.font.SysFont(None, 28)
        self.clock = pygame.time.Clock()
        self._size = _size
        self.offset = 100
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode(
            (self.width, self.height + self.offset))
        self.screen.fill(BLACK)
        self.maze = maze.Maze(self._size)
        self.maze.generate_new_maze()

    def resize(self, width, height, size):
        self.__init__(width, height, size)

    def qualify_sceen(self, points):
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.height+self.offset))
        letter_offset = 0
        letter_qt = 0
        letters = string.ascii_uppercase
        cont = 0
        blip_cont = 1

        welcome_text = "HALL OF FAME"
        instruction_text = "Use the Up/Down keyboard keys"
        blip = "_"

        letter = letters[cont].ljust(3)
        minus_text = str(points)

        exit_text = "Press Enter to save"

        welcome_text_font = self.font.render(welcome_text, 1, (255, 255, 255))
        instruction_text_font = self.font.render(instruction_text, 1, (255, 255, 255))
        blip_font = self.font.render(blip, 1, (255, 255, 255))
        letter_font = self.font.render(letter, 1, (255, 255, 255))
        minus_text_font = self.font.render(minus_text, 1, (255, 255, 255))
        exit_text_font = self.font.render(exit_text, 1, (255, 255, 255))


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
                        cont = (cont+1)%len(letters)
                        letter = (letter[:letter_qt] + letters[cont]).ljust(3)
                        letter_font = self.font.render(
                            letter, 1, (255, 255, 255))
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
                        cont = (cont-1)%len(letters)
                        letter = (letter[:letter_qt] + letters[cont]).ljust(3)
                        letter_font = self.font.render(
                            letter, 1, (255, 255, 255))
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                    elif event.key == pygame.K_RETURN:
                        if letter_qt == 2:
                            self.leaderboard.add_player([letter, points])
                            return
                        else:
                            letter_qt += 1
                            cont = 0
                            letter = (letter[:letter_qt] + letters[0]).ljust(3)
                            letter_font = self.font.render(
                            letter, 1, (255, 255, 255))
                            pygame.draw.rect(
                                self.screen, BLACK, (0, 0, self.width, self.height + self.offset))

            self.screen.blit(
                welcome_text_font, ((self.width - self.font.size(welcome_text)[0]) / 2, 20))
            self.screen.blit(
                instruction_text_font, ((self.width - self.font.size(instruction_text)[0]) / 2, self.font.size(welcome_text)[1]+100))
            blip_font = self.font.render(blip, 1, (255,255,255)) if blip_cont < 30 else self.font.render(blip, 1, (0,0,0))
            blip_cont = (blip_cont+1)%60
            self.screen.blit(
                blip_font,
                (((self.width -
                  self.font.size("A")[0]) /
                 4)+(letter_qt*self.font.size("A")[0]),
                 ((self.height +
                   self.offset) -
                  self.font.size("A")[1])/2))
            self.screen.blit(
                letter_font,
                ((self.width -
                  self.font.size("A")[0]) /
                 4,
                 ((self.height +
                   self.offset) -
                  self.font.size("A")[1])/2))
            self.screen.blit(
                minus_text_font,
                (3 * (self.width -
                  self.font.size(minus_text)[0]) /
                 4,
                 ((self.height +
                   self.offset) -
                  self.font.size(minus_text)[1]) /
                    2))
            self.screen.blit(
                exit_text_font,
                ((self.width - self.font.size(exit_text)[0]) / 2,
                 ((self.height + self.offset) - self.font.size(exit_text)[1])))

            self.clock.tick(60)
            pygame.display.flip()


    def solve_screen(self):
        welcome_text = "Solving the maze..."

        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.offset))
        
        welcome_text_font = self.font.render(welcome_text, 1, (255, 255, 255))
        self.screen.blit(
                welcome_text_font, ((self.width - self.font.size(welcome_text)[0]) / 2, 20))
        pygame.display.flip()

         
        self.maze.solve_maze()
        self.paint_solution_manhattan(10, "default")


    def leaderboard_screen(self):
        font2 = pygame.font.SysFont('monospace', 28)
        BACKGROUNDS = []
        for colour in list(Color('red').range_to(Color("blue"), self.leaderboard.size)):
            BACKGROUNDS.append([int(c*255) for c in colour.rgb])

        welcome_text = "HALL OF FAME"
        exit_text = "Press Enter to return"
        
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.offset))
        
        welcome_text_font = self.font.render(welcome_text, 1, (255, 255, 255))
        exit_text_font = self.font.render(exit_text, 1, (255, 255, 255))
        
        self.screen.blit(
                welcome_text_font, ((self.width - self.font.size(welcome_text)[0]) / 2, 20))
        self.screen.blit(
                exit_text_font,
                ((self.width - self.font.size(exit_text)[0]) / 2,
                 ((self.height + self.offset) - font2.size(exit_text)[1])))
        
        ranks = self.leaderboard.rankings()
        for ind, stats in enumerate(ranks):
            name, point = str(stats[0]), str(stats[1])

            stats_text = "{:02d} | {} | {}".format(ind+1, name, point)
            pygame.draw.rect(self.screen, BACKGROUNDS[ind], (0, 80 + font2.size(stats_text)[1]*ind, self.width, font2.size(stats_text)[1]))
            stats_text_font = font2.render(stats_text, 1, (0, 0, 0))
            self.screen.blit(
                stats_text_font, ((self.width - font2.size(stats_text)[0]) / 2, 80 + font2.size(stats_text)[1]*ind))

        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return


    def main_loop(self):
        start_time = time.time()
        _directions = {
            pygame.K_UP: -self._size,
            pygame.K_DOWN: self._size,
            pygame.K_RIGHT: 1,
            pygame.K_LEFT: -1
        }

        cleared = 0
        grid = self.maze.copy_array()

        current = self.maze.start
        _end = self.maze.exit

        solve_text = " SOLVE "
        points_text = "{}".format((self._size//10)/(int(time.time() - start_time + 1)))

        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.offset))
        

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if pos[0] in range(
                            5,
                            5 +
                            self.font.size(solve_text)[0]) and pos[1] in range(
                            5 +
                            self.font.size(points_text)[1],
                            5 +
                            self.font.size(points_text)[1] +
                            self.font.size(solve_text)[1]):
                        self.qualify_sceen(points)
                        self.solve_screen()
                        self.__init__(self.width, self.height, 10)
                        return
                elif event.type == pygame.KEYDOWN:
                    if self.maze.check_end(current):
                        cleared += 1
                        placement = points
                        print(cleared, placement)
                        self._size += 10
                        _directions = {
                            pygame.K_UP: -self._size,
                            pygame.K_DOWN: self._size,
                            pygame.K_RIGHT: 1,
                            pygame.K_LEFT: -1
                        }
                        self.maze = maze.Maze(self._size)
                        self.maze.generate_new_maze()

                        grid = self.maze.copy_array()

                        current = self.maze.start
                        _end = self.maze.exit
                        self.screen.fill(BLACK)
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
                    color = COLORS[grid[self._size * column + row]]
                    pygame.draw.rect(self.screen, color,
                                     [(self.width / self._size) * row,
                                      (self.height / self._size) * column + self.offset,
                                         (self.width / self._size - 1),
                                         (self.height / self._size - 1)])

            points = ((self._size//2)**2) - (int(time.time() - start_time))
            points_text = "{}".format(points)

            pygame.draw.rect(
                self.screen, BLACK, (0, 0, self.width, self.offset))
            points_text_font = self.font.render(
                points_text, 1, (255, 255, 255))
            self.screen.blit(points_text_font, (5, 0))
            solve_text_font = self.font.render(
                solve_text, 1, (255, 255, 255), RED)
            self.screen.blit(
                solve_text_font, (5, 5 + self.font.size(points_text)[1]))

            self.clock.tick(60)
            pygame.display.flip()

    def start_menu(self):

        pygame.draw.rect(
            self.screen,
            BLACK,
            (0,
             0,
             self.width,
             self.height +
             self.offset))

        welcome_text = "WELCOME TO MAZE BLITZ"
        settings_text = "Press 'S' for Settings"
        start_text = "'Enter' to start playing"

        welcome_text_font = self.font.render(welcome_text, 1, (255, 255, 255))
        settings_text_font = self.font.render(
            settings_text, 1, (255, 255, 255))
        start_text_font = self.font.render(start_text, 1, (255, 255, 255))

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                        self.settings_menu()
                    elif event.key == pygame.K_RETURN:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                        self.main_loop()
                    elif event.key == pygame.K_l:
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                        self.leaderboard_screen()

            pygame.draw.rect(
                self.screen,
                BLACK,
                (0,
                 0,
                 self.width,
                 self.height +
                 self.offset))
            self.screen.blit(
                welcome_text_font, ((self.width - self.font.size(welcome_text)[0]) / 2, 20))
            self.screen.blit(
                settings_text_font,
                ((self.width - self.font.size(settings_text)[0]) / 2,
                 ((self.height + self.offset) - self.font.size(settings_text)[1]) / 4))
            self.screen.blit(
                start_text_font,
                ((self.width - self.font.size(start_text)[0]) / 2,
                 ((self.height + self.offset) - self.font.size(start_text)[1]) / 2))
            self.clock.tick(60)
            pygame.display.flip()

    def settings_menu(self):
        size_ = self._size
        pygame.draw.rect(self.screen, BLACK, (0, 0, self.width, self.height+self.offset))

        welcome_text = "Adjust Initial Level"
        instruction_text = "Use the Up/Down keyboard keys"
        plus_text = "^"
        minus_text = "v"
        level_text = "1"
        exit_text = "Press Enter to save and return"

        welcome_text_font = self.font.render(welcome_text, 1, (255, 255, 255))
        instruction_text_font = self.font.render(instruction_text, 1, (255, 255, 255))
        plus_text_font = self.font.render(plus_text, 1, (255, 255, 255))
        minus_text_font = self.font.render(minus_text, 1, (255, 255, 255))
        level_text_font = self.font.render(level_text, 1, (255, 255, 255))
        exit_text_font = self.font.render(exit_text, 1, (255, 255, 255))


        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP or event.key == pygame.K_RIGHT:
                        level_text = str(int(level_text) + 1)
                        level_text_font = self.font.render(
                            level_text, 1, (255, 255, 255))
                        size_ = int(level_text) * 10
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_LEFT:
                        level_text = str(max(1, int(level_text) - 1))
                        level_text_font = self.font.render(
                            level_text, 1, (255, 255, 255))
                        size_ = int(level_text) * 10
                        pygame.draw.rect(
                            self.screen, BLACK, (0, 0, self.width, self.height + self.offset))
                    elif event.key == pygame.K_RETURN:
                        self.resize(self.width, self.height, size_)
                        return

            self.screen.blit(
                welcome_text_font, ((self.width - self.font.size(welcome_text)[0]) / 2, 20))
            self.screen.blit(
                instruction_text_font, ((self.width - self.font.size(instruction_text)[0]) / 2, self.font.size(welcome_text)[1]+100))
            self.screen.blit(
                plus_text_font,
                ((self.width -
                  self.font.size(plus_text)[0]) /
                 2,
                 ((self.height +
                   self.offset) -
                  self.font.size(plus_text)[1]) /
                    2 -
                    self.font.size(level_text)[1]))
            self.screen.blit(
                minus_text_font,
                ((self.width -
                  self.font.size(minus_text)[0]) /
                 2,
                 ((self.height +
                   self.offset) -
                  self.font.size(minus_text)[1]) /
                    2 +
                    self.font.size(level_text)[1]))
            self.screen.blit(
                level_text_font,
                ((self.width - self.font.size(level_text)[0]) / 2,
                 ((self.height + self.offset) - self.font.size(level_text)[1]) / 2))
            self.screen.blit(
                exit_text_font,
                ((self.width - self.font.size(exit_text)[0]) / 2,
                 ((self.height + self.offset) - self.font.size(exit_text)[1])))

            self.clock.tick(60)
            pygame.display.flip()

    def draw_polygon(self, draw, ind, block_size, color):
        draw.polygon([(ind % self._size) * block_size,
                      (ind // self._size) * block_size,
                      (ind % self._size) * block_size + block_size,
                      (ind // self._size) * block_size,
                      (ind % self._size) * block_size + block_size,
                      (ind // self._size) * block_size + block_size,
                      (ind % self._size) * block_size,
                      (ind // self._size) * block_size + block_size],
                     fill=(color))

    def paint_solution_manhattan(self, block_size, path, n_colors=100):
        start_time = time.time()
        # size = self._size * self._size
        img = Image.new(
            'RGB',
            (self._size *
             block_size,
             self._size *
             block_size),
            color=(
                0,
                0,
                0))
        draw = ImageDraw.Draw(img)
        colors = []
        for color in list(Color('blue').range_to(Color("red"), n_colors)):
            colors.append([int(c * 255) for c in color.rgb])
        for color in list(Color('red').range_to(Color("blue"), n_colors)):
            colors.append([int(c * 255) for c in color.rgb])
        # for color in list(Color('green').range_to(Color("blue"), n_colors)):
        #   colors.append([int(c*255) for c in color.rgb])
        _maze = self.maze.pathing
        # progress = 0
        col = 0
        start = self.maze.start
        # end = self.maze.exit
        ind = start
        for width in range(self._size):
            for height in range(self._size):
                if _maze[width + self._size * height] == 1:
                    draw.polygon([width * block_size,
                                  height * block_size,
                                  width * block_size + block_size,
                                  height * block_size,
                                  width * block_size + block_size,
                                  height * block_size + block_size,
                                  width * block_size,
                                  height * block_size + block_size],
                                 fill=(255, 255, 255))
        while True:
            # LEFT SLOT
            if self.maze.check_bounds(
                    ind, -1) and ind % self._size > (ind - 1) % self._size and _maze[ind - 1] == 2:
                self.draw_polygon(draw, ind, block_size, tuple(colors[col]))
                _maze[ind] = -1
                ind = ind - 1
                col = (col + 1) % len(colors)
                continue

            # RIGHT SLOT
            if self.maze.check_bounds(
                    ind, +1) and ind % self._size < (ind + 1) % self._size and _maze[ind + 1] == 2:
                self.draw_polygon(draw, ind, block_size, tuple(colors[col]))

                _maze[ind] = -1
                ind = ind + 1
                col = (col + 1) % len(colors)
                continue

            # UPPER SLOT
            if self.maze.check_bounds(
                    ind, -self._size) and _maze[ind - self._size] == 2:
                self.draw_polygon(draw, ind, block_size, tuple(colors[col]))

                _maze[ind] = -1
                ind = ind - self._size
                col = (col + 1) % len(colors)
                continue

            # DOWN SLOT
            if self.maze.check_bounds(
                    ind, +self._size) and _maze[ind + self._size] == 2:
                self.draw_polygon(draw, ind, block_size, tuple(colors[col]))

                _maze[ind] = -1
                ind = ind + self._size
                col = (col + 1) % len(colors)
                continue

            self.draw_polygon(draw, ind, block_size, tuple(colors[col]))

            break

        print("Painting solution... 100%")
        img.save("{}_solution.bmp".format(path), quality=100, subsampling=0)
        elapsed_time = time.time() - start_time
        print("Elapsed time painting solution : {}".format(elapsed_time))


if __name__ == "__main__":
    PyManMain().start_menu()
    # PyManMain().leaderboard_screen()
