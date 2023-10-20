# -*- coding: utf-8 -*-
import random


# 初始化游戏面板
def start_game():
    matrix = [[0] * 4 for _ in range(4)]
    # 在随机位置生成两个初始数字2或4
    for _ in range(2):
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        matrix[row][col] = random.choice([2, 4])
    return matrix


# 打印游戏面板
def print_board(matrix):
    for row in matrix:
        print('\t'.join(str(num) for num in row))
        print()


# 判断游戏是否结束
def is_game_over(matrix):
    # 如果有空格或相邻两个数字相等，游戏未结束
    for row in matrix:
        if 0 in row:
            return False
        for i in range(3):
            if row[i] == row[i + 1]:
                return False
    for col in range(4):
        for i in range(3):
            if matrix[i][col] == matrix[i + 1][col]:
                return False
    return True


# 进行左移操作
def move_left(matrix):
    score = 0
    # 合并相邻且相等的数字
    for row in matrix:
        for i in range(3):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                score += row[i]
    # 再次进行左移，确保空格都在右侧
    for row in matrix:
        for _ in range(3):
            for i in range(3):
                if row[i] == 0:
                    row[i] = row[i + 1]
                    row[i + 1] = 0
    return matrix, score


# 进行游戏操作：上、下、左、右移动
def play_game(matrix, move):
    if move == 'up':
        # 上移操作等效于将矩阵逆时针旋转90度，进行左移，再次逆时针旋转90度
        matrix = rotate_matrix(matrix)
        matrix, score = move_left(matrix)
        matrix = rotate_matrix(matrix, 3)
        return matrix, score

    if move == 'down':
        # 下移操作等效于将矩阵顺时针旋转90度，进行左移，再次顺时针旋转90度
        matrix = rotate_matrix(matrix, 3)
        matrix, score = move_left(matrix)
        matrix = rotate_matrix(matrix)
        return matrix, score

    if move == 'left':
        matrix, score = move_left(matrix)
        return matrix, score

    if move == 'right':
        # 右移操作等效于将矩阵逆时针旋转180度，进行左移，再次逆时针旋转180度
        matrix = rotate_matrix(matrix, 2)
        matrix, score = move_left(matrix)
        matrix = rotate_matrix(matrix, 2)
        return matrix, score


# 逆时针旋转矩阵
def rotate_matrix(matrix, times=1):
    for _ in range(times):
        matrix = list(zip(*matrix[::-1]))
    return matrix


# 游戏主循环
def main():
    matrix = start_game()
    print_board(matrix)
    while not is_game_over(matrix):
        move = input('请输入移动方向（上：up，下：down，左：left，右：right）：')
        matrix, score = play_game(matrix, move)
        # 在空白处随机生成一个新数字
        row = random.randint(0, 3)
        col = random.randint(0, 3)
        while matrix[row][col] != 0:
            row = random.randint(0, 3)
            col = random.randint(0, 3)
        matrix[row][col] = random.choice([2, 4])
        print_board(matrix)
        print('当前得分：', score)
    print('游戏结束')


# 执行主循环
if __name__ == '__main__':
    main()