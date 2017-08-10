# -*- coding: utf-8 -*-

import pygame
import random


WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
GREEN = (0, 0xff, 0)
RED = (0xff, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)

D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3

# 初始化
pygame.init()

WIDTH, HEIGHT = 500, 500

# 贪吃蛇小方块的宽度
CUBE_WIDTH = 20

# 计算屏幕的网格数，网格的大小就是小蛇每一节身体的大小
GRID_WIDTH_NUM, GRID_HEIGHT_NUM = WIDTH / CUBE_WIDTH, HEIGHT / CUBE_WIDTH

# 设置画布
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 设置标题
pygame.display.set_caption("贪吃蛇")


# 设置定时器
clock = pygame.time.Clock()
FPS = 30

running = True

# 设置计数器
counter = 0

# 设置出事运动方向为向左
direction = D_LEFT


# 每次小蛇身体加长的时候，我们就将身体的位置加到列表末尾
snake_body = []
snake_body.append((int(GRID_WIDTH_NUM / 2) * CUBE_WIDTH,
                   int(GRID_HEIGHT_NUM / 2) * CUBE_WIDTH))  # 添加贪吃蛇的“头”


# 画出网格线
def draw_grids():
    for i in range(GRID_WIDTH_NUM):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * CUBE_WIDTH, 0), (i * CUBE_WIDTH, HEIGHT))

    for i in range(GRID_HEIGHT_NUM):
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * CUBE_WIDTH), (WIDTH, i * CUBE_WIDTH))


# 打印身体的函数
def draw_body():
    for sb in snake_body:
        pygame.draw.rect(screen, WHITE, (sb[0], sb[1], CUBE_WIDTH, CUBE_WIDTH))

    # 将头部改成红色
    pygame.draw.rect(screen, RED,
                    (snake_body[0][0],
                     snake_body[0][1],
                     CUBE_WIDTH,
                     CUBE_WIDTH))



# 用于记录食物的位置
food_pos = None


# 随机产生一个事物
def generate_food():
    return (random.randint(0, GRID_WIDTH_NUM - 1),
            random.randint(0, GRID_HEIGHT_NUM - 1))


# 画出食物的主体
def draw_food():
    # print (food_pos)
    pygame.draw.rect(screen, GREEN,
                     (food_pos[0] * CUBE_WIDTH,
                      food_pos[1] * CUBE_WIDTH, CUBE_WIDTH, CUBE_WIDTH))


# 判断贪吃蛇是否吃到了事物，如果吃到了我们就加长小蛇的身体
def grow():
    if snake_body[0][0] == food_pos[0] * CUBE_WIDTH and\
            snake_body[0][1] == food_pos[1] * CUBE_WIDTH:
        return True

    return False

# import pdb; pdb.set_trace()
# 先产生一个食物
food_pos = generate_food()
draw_food()
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:      # 如果有按键被按下了
            # 判断按键类型
            if event.key == pygame.K_UP:
                direction = D_UP
            elif event.key == pygame.K_DOWN:
                direction = D_DOWN
            elif event.key == pygame.K_LEFT:
                direction = D_LEFT
            elif event.key == pygame.K_RIGHT:
                direction = D_RIGHT

    # 判断计数器是否符合要求，如果符合就移动方块位置，（调整方块位置）
    if counter % int(FPS / 12) == 0:
        # 这里需要保存一下尾部的位置，因为下文我们要更新这个位置
        # 在这种情况下如果小蛇迟到了食物，需要在尾部增长，那么我们
        # 就不知道添加到什么地方了～～
        last_pos = snake_body[-1]

        # 更新小蛇身体的位置
        for i in range(len(snake_body) - 1, 0, -1):
            snake_body[i] = snake_body[i - 1]

        # 改变头部的位置
        if direction == D_UP:
            snake_body[0] = (
                snake_body[0][0],
                snake_body[0][1] - CUBE_WIDTH)
        elif direction == D_DOWN:
            snake_body[0] = (
                snake_body[0][0],
                snake_body[0][1] + CUBE_WIDTH)
            # top += CUBE_WIDTH
        elif direction == D_LEFT:
            snake_body[0] = (
                snake_body[0][0] - CUBE_WIDTH,
                snake_body[0][1])
            # left -= CUBE_WIDTH
        elif direction == D_RIGHT:
            snake_body[0] = (
                snake_body[0][0] + CUBE_WIDTH,
                snake_body[0][1])

        # 判断小蛇是否吃到了事物，吃到了就成长
        got_food = grow()

        # 如果吃到了事物我们就产生一个新的事物
        if got_food:
            food_pos = generate_food()
            snake_body.append(last_pos)

    screen.fill(BLACK)
    draw_grids()

    # 画小蛇的身体
    draw_body()

    # 画出食物
    draw_food()

    # 计数器加一
    counter += 1
    # pygame.draw.rect(screen, WHITE, (left, top, CUBE_WIDTH, CUBE_WIDTH))
    pygame.display.update()

pygame.quit()
