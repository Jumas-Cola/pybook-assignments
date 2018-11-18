import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        c_size = self.cell_size
        for cell in clist:
            if cell.state == 1:
                pygame.draw.rect(self.screen, pygame.Color('green'), [c_size*cell.col+1, c_size*cell.row+1, c_size-1, c_size-1])
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'), [c_size*cell.col+1, c_size*cell.row+1, c_size-1, c_size-1])

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        #cell_list = CellList(int(self.height/self.cell_size), int(self.width/self.cell_size), True)
        cell_list = CellList.from_file(filename = 'grid.txt')

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(cell_list)
            cell_list.update()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    #def is_alive(self):
    #    pass


class CellList:

    # iterator protocol
    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.clist = []
        if randomize == True:
            clist = [[Cell(i,j,random.randint(0,1)) for j in range(ncols)] for i in range(nrows)]
        else:
            clist = [[Cell(i,j) for j in range(ncols)] for i in range(nrows)]
        for i in clist:
            for j in i:
                self.clist.append(j)
        self.index = -1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index == len(self.clist)-1:
            self.index = -1
            raise StopIteration
        self.index = self.index + 1
        return self.clist[self.index]

    def get_neighbours(self, cell):
        neighbours = []
        neighbours_addrs = [
        (cell.row-1, cell.col-1),
        (cell.row-1, cell.col),
        (cell.row-1, cell.col+1),
        (cell.row, cell.col-1),
        (cell.row, cell.col+1),
        (cell.row+1, cell.col-1),
        (cell.row+1, cell.col),
        (cell.row+1, cell.col+1),
        ]
        neighbours = [i for i in self.clist if (i.row, i.col) in neighbours_addrs]
        return neighbours

    def update(self):
        new_clist = deepcopy(self)
        for cell in enumerate(self):
            lives_count = [i.state for i in self.get_neighbours(cell[1])].count(1)
            if (cell[1].state==1) and (2<=lives_count<=3):
                new_clist.clist[cell[0]].state = 1
            elif (cell[1].state==0) and (lives_count==3):
                new_clist.clist[cell[0]].state = 1
            else:
                new_clist.clist[cell[0]].state = 0
        self.clist = new_clist.clist
        return self

    def __str__(self):
        values = [i.state for i in self.clist]
        n = self.ncols
        return str([values[i:i+n] for i in [j for j in range(len(values)) if j % n == 0]]).replace('], ','],\n ')

    @classmethod
    def from_file(cls, filename):
        with open(filename) as file:
            file_list = [list(string[:-1]) for string in file]
        nrows = len(file_list)
        ncols = len(file_list[0])
        examp = CellList(nrows, ncols, True)
        cell_states = []
        for i in file_list:
            for j in i:
                cell_states.append(j)
        for cell in enumerate(examp):
            cell[1].state = int(cell_states[cell[0]])
        return examp



if __name__ == '__main__':
    game = GameOfLife(320,240,20)
    game.run()
