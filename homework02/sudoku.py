import time
import threading
import multiprocessing

def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    """
    Сгруппировать значения values в список, состоящий из списков по n элементов

    >>> group([1,2,3,4], 2)
    [[1, 2], [3, 4]]
    >>> group([1,2,3,4,5,6,7,8,9], 3)
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    """
    return [values[i:i+n] for i in [j for j in range(len(values)) if j % n == 0]]


def get_row(values, pos):
    """ Возвращает все значения для номера строки, указанной в pos

    >>> get_row([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '2', '.']
    >>> get_row([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (1, 0))
    ['4', '.', '6']
    >>> get_row([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (2, 0))
    ['.', '8', '9']
    """
    return values[pos[0]]


def get_col(values, pos):
    """ Возвращает все значения для номера столбца, указанного в pos

    >>> get_col([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']], (0, 0))
    ['1', '4', '7']
    >>> get_col([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']], (0, 1))
    ['2', '.', '8']
    >>> get_col([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']], (0, 2))
    ['3', '6', '9']
    """
    return [i[pos[1]] for i in values]


def get_block(values, pos):
    """ Возвращает все значения из квадрата, в который попадает позиция pos

    >>> grid = read_sudoku('puzzle1.txt')
    >>> get_block(grid, (0, 1))
    ['5', '3', '.', '6', '.', '.', '.', '9', '8']
    >>> get_block(grid, (4, 7))
    ['.', '.', '3', '.', '.', '1', '.', '.', '6']
    >>> get_block(grid, (8, 8))
    ['2', '8', '.', '.', '.', '5', '.', '7', '9']
    """
    row = (pos[0] // 3) * 3 + 3
    col = (pos[1] // 3) * 3 + 3
    res = []
    for l in [j[col-3 : col] for j in [i for i in values[row-3 : row]]]:
        for num in l:
            res.append(num)
    return res


def find_empty_positions(grid):
    """ Найти первую свободную позицию в пазле

    >>> find_empty_positions([['1', '2', '.'], ['4', '5', '6'], ['7', '8', '9']])
    (0, 2)
    >>> find_empty_positions([['1', '2', '3'], ['4', '.', '6'], ['7', '8', '9']])
    (1, 1)
    >>> find_empty_positions([['1', '2', '3'], ['4', '5', '6'], ['.', '8', '9']])
    (2, 0)
    """
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            if grid[row][col]=='.':
                return (row, col)


def find_possible_values(grid, pos):
    """ Вернуть множество возможных значения для указанной позиции

    >>> grid = read_sudoku('puzzle1.txt')
    >>> values = find_possible_values(grid, (0,2))
    >>> values == {'1', '2', '4'}
    True
    >>> values = find_possible_values(grid, (4,7))
    >>> values == {'2', '5', '9'}
    True
    """
    pos_val = set('123456789')
    pos_val-=set(get_row(grid, pos))
    pos_val-=set(get_col(grid, pos))
    pos_val-=set(get_block(grid, pos))
    return pos_val


def solve(grid):
    """ Решение пазла, заданного в grid """
    """ Как решать Судоку?
        1. Найти свободную позицию
        2. Найти все возможные значения, которые могут находиться на этой позиции
        3. Для каждого возможного значения:
            3.1. Поместить это значение на эту позицию
            3.2. Продолжить решать оставшуюся часть пазла

    >>> grid = read_sudoku('puzzle1.txt')
    >>> solve(grid)
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    empty = find_empty_positions(grid)
    if not empty:
        return grid
    else:
        pos_vals = find_possible_values(grid, empty)
        for pos_val in pos_vals:
            grid_1 = [[j for j in i] for i in grid]
            grid_1[empty[0]][empty[1]] = pos_val
            res = solve(grid_1)
            if res:
                return res


def check_solution(solution):
    """ Если решение solution верно, то вернуть True, в противном случае False """
    values = set('123456789')
    for i in range(9):
        if (set(get_row(solution, (i, 0))) != values):
            return False
        if (set(get_col(solution, (0, i))) != values):
            return False
        if (set(get_block(solution, (i//3*3, i%3*3))) != values):
            return False
    return True


def generate_sudoku(N):
    """ Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    sudoku = [['.' for i in range(9)] for j in range(9)]
    if N > 81:
        N = 81
    for i in range(N):
        index = (random.randint(0,8), random.randint(0,8))
        while sudoku[index[0]][index[1]] != '.':
            index = (random.randint(0,8), random.randint(0,8))
        sudoku[index[0]][index[1]] = random.choice('123456789')
    return sudoku


def run_solve(fname):
    grid = read_sudoku(fname)
    start = time.time()
    solve(grid)
    end = time.time()
    print(f'{fname}: {end-start}')


if __name__ == '__main__':
    # последовательное решение
    for fname in ['puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt']:
        grid = read_sudoku(fname)
        display(grid)
        start = time.time()
        solution = solve(grid)
        end = time.time()
        print(f'{fname}: {end-start}')
        display(solution)
    # многопоточное решение
    for fname in ('puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt'):
        t = threading.Thread(target=run_solve, args=(fname,))
        t.start()
    # параллельное решение
    for fname in ('puzzle1.txt', 'puzzle2.txt', 'puzzle3.txt'):
        p = multiprocessing.Process(target=run_solve, args=(fname,))
        p.start()
    # сравнение подходов
    N = 5
    for _ in range(N):
        t = threading.Thread(target=run_solve, args=('puzzle2.txt',))
        t.start()
    for _ in range(N):
        p = multiprocessing.Process(target=run_solve, args=('puzzle2.txt',))
        p.start()
