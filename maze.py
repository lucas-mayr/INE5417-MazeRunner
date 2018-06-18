import os

from random import choice
from timeit import default_timer


class Maze:
    def __init__(self, side, name='Default'):
        self.name = name
        self.side = side
        self.size = side * side
        self.start = 1
        self.exit = None
        self.maze = self.template_maze()
        self.pathing = None

    def copy_array(self):
        return [i for i in self.maze]

    def template_maze(self):
        self.maze = [None] * (self.side * self.side)
        for i in range(self.side):
            for j in range(self.side):
                if i % self.side == 0 or i % self.side == (
                        self.side - 1) or j % self.side == (self.side - 1) or j == 0:
                    self.maze[i + j * self.side] = 0
        return self.maze

    def check_bounds(self, ind, offset):
        ans = (ind + offset > 0)
        ans = ans and (ind + offset < self.side * self.side)
        return ans

    def print_maze(self):
        print("|-" * self.side + "|")
        for i, slot in enumerate(self.maze):
            print(slot, end=' ') if slot is not None else print('X', end=' ')
            if (i + 1) % (self.side) == 0:
                print("")
        print("|-" * self.side + "|")

    def print_solution(self):
        if not self.pathing:
            return
        print("|-" * self.side + "|")
        for i, slot in enumerate(self.pathing):
            print(slot, end=' ')
            if (i + 1) % (self.side) == 0:
                print("")
        print("|-" * self.side + "|")

    def check_end(self, position):
        return position == self.exit

    def generate_new_maze(self, name=None):
        self.maze = self.template_maze()
        actual_name = name or self.name

        start_time = default_timer()

        maze_next = set([self.start])
        maze_temp = set()

        progress = 0
        try:
            while None in self.maze:
                if not maze_temp:
                    slot = choice(list(maze_next))
                else:
                    slot = choice(list(maze_temp))

                maze_temp = set()
                ocurrences = 0
                # LEFT SLOT
                if self.check_bounds(
                        slot, -1) and slot % self.side > (slot - 1) % self.side:
                    if self.maze[slot - 1]:
                        ocurrences += 1
                    if self.maze[slot - 1] is None:
                        maze_temp.add(slot - 1)
                # RIGHT SLOT
                if self.check_bounds(
                        slot, +1) and slot % self.side < (slot + 1) % self.side:
                    if self.maze[slot + 1]:
                        ocurrences += 1
                    if self.maze[slot + 1] is None:
                        maze_temp.add(slot + 1)
                # UPPER SLOT
                if self.check_bounds(slot, -self.side):
                    if self.maze[slot - self.side]:
                        ocurrences += 1
                    if self.maze[slot - self.side] is None:
                        maze_temp.add(slot - self.side)
                # DOWN SLOT
                if self.check_bounds(slot, +self.side):
                    if self.maze[slot + self.side]:
                        ocurrences += 1
                    if self.maze[slot + self.side] is None:
                        maze_temp.add(slot + self.side)

                self.maze[slot] = 1 if ocurrences < 2 else 0

                if self.maze[slot]:
                    maze_next = maze_next | maze_temp
                else:
                    maze_temp = set()

                maze_next.remove(slot)

                progress += 100
                
        except IndexError:
            for i, slot in enumerate(self.maze):
                if slot is None:
                    self.maze[i] = 0

        end = [i + (self.side * (self.side - 2)) for i,
               v in enumerate(self.maze[-self.side * 2:-self.side]) if v == 1][-1]
        self.maze[self.start] = 1
        self.maze[end + self.side] = 1
        self.exit = end + self.side
        elapsed_time = default_timer() - start_time

    def solve_maze(self):
        start_time = default_timer()
        maze_path = [self.start, self.start + self.side]
        dead_ends = []
        self.pathing = list(map(lambda x: x, self.maze))
        while maze_path[-1] != self.exit:
            slot = maze_path[-1]

            self.pathing[slot] = 2

            # TRY RIGHT
            if self.check_bounds(slot, +1) and slot % self.side < (slot + 1) % self.side and self.maze[slot + 1] and (
                    slot + 1) not in maze_path and (slot + 1) not in dead_ends:
                maze_path.append(slot + 1)
                continue
            # TRY DOWN
            if self.check_bounds(slot, +
                                 self.side) and (slot +
                                                 self.side) and self.maze[slot +
                                                                          self.side] and (slot +
                                                                                          self.side) not in maze_path and (slot +
                                                                                                                           self.side) not in dead_ends:
                maze_path.append(slot + self.side)
                continue
            # TRY LEFT
            if self.check_bounds(slot, -1) and slot % self.side > (slot - 1) % self.side and self.maze[slot - 1] and (
                    slot - 1) not in maze_path and (slot - 1) not in dead_ends:
                maze_path.append(slot - 1)
                continue
            # TRY UP
            if self.check_bounds(slot, -
                                 self.side) and (slot -
                                                 self.side) and self.maze[slot -
                                                                          self.side] and (slot -
                                                                                          self.side) not in maze_path and (slot -
                                                                                                                           self.side) not in dead_ends:
                maze_path.append(slot - self.side)
                continue

            dead_ends.append(maze_path.pop())

            self.pathing[slot] = 1

        self.pathing[self.exit] = 2
        self.pathing[self.start] = 2
        elapsed_time = default_timer() - start_time


if __name__ == "__main__":
    try:
        os.makedirs("Examples")
    except BaseException:
        pass
    EXAMPLE_MAZE = Maze(15, name=os.path.join('Examples', 'depth_first.bmp'))
    EXAMPLE_MAZE.generate_new_maze()
    EXAMPLE_MAZE.print_maze()
    EXAMPLE_MAZE.solve_maze()
