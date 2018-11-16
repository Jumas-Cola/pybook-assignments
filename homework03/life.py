import pygame
from pygame.locals import *
import random


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

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        # Создание списка клеток
        clist = self.cell_list(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_cell_list(clist)
            clist = self.update_cell_list(clist)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.

        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        if randomize == True:
            self.clist = [[random.randint(0,1) for j in range(int(self.width/self.cell_size))] for i in range(int(self.height/self.cell_size))]
        else:
            self.clist = [[0 for j in range(int(self.width/self.cell_size))] for i in range(int(self.height/self.cell_size))]
        return self.clist

    def draw_cell_list(self, clist):
        """ Отображение списка клеток

        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        c_size = self.cell_size
        for row in range(len(clist)):
            for col in range(len(clist[row])):
                if clist[row][col] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), [c_size*col+1, c_size*row+1, c_size-1, c_size-1])
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), [c_size*col+1, c_size*row+1, c_size-1, c_size-1])

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки

        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = [
        (cell[0]-1, cell[1]-1),
        (cell[0]-1, cell[1]),
        (cell[0]-1, cell[1]+1),
        (cell[0], cell[1]-1),
        (cell[0], cell[1]+1),
        (cell[0]+1, cell[1]-1),
        (cell[0]+1, cell[1]),
        (cell[0]+1, cell[1]+1),
        ]
        neighbours = [i for i in neighbours if 0<=i[0]<int(self.height/self.cell_size) and 0<=i[1]<int(self.width/self.cell_size)]
        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.

        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.

        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = []
        for row in range(len(cell_list)):
            new_sub_clist = []
            for col in range(len(cell_list[row])):
                neighbours = game.get_neighbours((row,col))
                lives_deads = [cell_list[neighbour[0]][neighbour[1]] for neighbour in neighbours]
                if (cell_list[row][col]==1) and (2<=lives_deads.count(1)<=3):
                    new_sub_clist.append(1)
                elif (cell_list[row][col]==0) and (lives_deads.count(1)==3):
                    new_sub_clist.append(1)
                else:
                    new_sub_clist.append(0)
            new_clist.append(new_sub_clist)
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(1280,650,10)
    game.run()
