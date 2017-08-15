# -*- coding: utf-8 -*-

import pygame
import random
import os


WHITE = (0xff, 0xff, 0xff)
BLACK = (0, 0, 0)
GREEN = (0, 0xff, 0)
RED = (0xff, 0, 0)
LINE_COLOR = (0x33, 0x33, 0x33)
FPS = 30

HARD_LEVEL = list(range(2, int(FPS/2), 2))
hardness = HARD_LEVEL[0]

D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3

# 初始化
pygame.init()

# 要想载入音乐，必须要初始化 mixer
pygame.mixer.init()

WIDTH, HEIGHT = 500, 500

# 贪吃蛇小方块的宽度
CUBE_WIDTH = 20

# 计算屏幕的网格数，网格的大小就是小蛇每一节身体的大小
GRID_WIDTH_NUM, GRID_HEIGHT_NUM = int(WIDTH / CUBE_WIDTH),\
                                  int(HEIGHT / CUBE_WIDTH)

# 设置画布
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# 设置标题
pygame.display.set_caption("贪吃蛇")


# 设置游戏的根目录为当前文件夹
base_folder = os.path.dirname(__file__)

# 这里需要在当前目录下创建一个名为music的目录，并且在里面存放名为back.mp3的背景音乐
music_folder = os.path.join(base_folder, 'music')

# 背景音乐
back_music = pygame.mixer.music.load(os.path.join(music_folder, 'back.mp3'))

# 小蛇吃食物的音乐
bite_dound = pygame.mixer.Sound(os.path.join(music_folder, 'armor-light.wav'))

# 图片
img_folder = os.path.join(base_folder, 'images')
back_img = pygame.image.load(os.path.join(img_folder, 'back.png'))
snake_head_img = pygame.image.load(os.path.join(img_folder, 'head.png'))
snake_head_img.set_colorkey(BLACK)
food_img = pygame.image.load(os.path.join(img_folder, 'orb2.png'))

# 调整图片的大小，和屏幕一样大
background = pygame.transform.scale(back_img, (WIDTH, HEIGHT))

food = pygame.transform.scale(food_img, (CUBE_WIDTH, CUBE_WIDTH))


# 设置一下音量大小，防止过大
pygame.mixer.music.set_volume(0.4)

# 设置音乐循环次数 -1 表示无限循环
pygame.mixer.music.play(loops=-1)


# 设置定时器
clock = pygame.time.Clock()

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
def draw_body(direction=D_LEFT):
    for sb in snake_body[1:]:
        screen.blit(food, sb)

    if direction == D_LEFT:
        rot = 0
    elif direction == D_RIGHT:
        rot = 180
    elif direction == D_UP:
        rot = 270
    elif direction == D_DOWN:
        rot = 90
    new_head_img = pygame.transform.rotate(snake_head_img, rot)
    head = pygame.transform.scale(new_head_img, (CUBE_WIDTH, CUBE_WIDTH))
    screen.blit(head, snake_body[0])



# 用于记录食物的位置
food_pos = None


# 随机产生一个事物
def generate_food():
    while True:
        pos = (random.randint(0, GRID_WIDTH_NUM - 1),
               random.randint(0, GRID_HEIGHT_NUM - 1))

        # 如果当前位置没有小蛇的身体，我们就跳出循环，返回食物的位置
        if not (pos[0] * CUBE_WIDTH, pos[1] * CUBE_WIDTH) in snake_body:
            return pos


# 画出食物的主体
def draw_food():
    screen.blit(food, (food_pos[0] * CUBE_WIDTH,
                      food_pos[1] * CUBE_WIDTH, CUBE_WIDTH, CUBE_WIDTH))


# 判断贪吃蛇是否吃到了事物，如果吃到了我们就加长小蛇的身体
def grow():
    if snake_body[0][0] == food_pos[0] * CUBE_WIDTH and\
            snake_body[0][1] == food_pos[1] * CUBE_WIDTH:
        # 每次吃到食物，就播放音效
        bite_dound.play()
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
    if counter % int(FPS / hardness) == 0:
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

        # 限制小蛇的活动范围
        if snake_body[0][0] < 0 or snake_body[0][0] >= WIDTH or\
                snake_body[0][1] < 0 or snake_body[0][1] >= HEIGHT:
            # 超出屏幕之外游戏结束
            running = False

        # 限制小蛇不能碰到自己的身体
        for sb in snake_body[1: ]:
            # 身体的其他部位如果和蛇头（snake_body[0]）重合就死亡
            if sb == snake_body[0]:
                running = False

        # 判断小蛇是否吃到了事物，吃到了就成长
        got_food = grow()

        # 如果吃到了事物我们就产生一个新的事物
        if got_food:
            food_pos = generate_food()
            snake_body.append(last_pos)
            hardness = HARD_LEVEL[min(int(len(snake_body) / 10),
                                      len(HARD_LEVEL) - 1)]

    # screen.fill(BLACK)
    screen.blit(background, (0, 0))
    draw_grids()

    # 画小蛇的身体
    draw_body(direction)

    # 画出食物
    draw_food()

    # 计数器加一
    counter += 1
    pygame.display.update()

pygame.quit()
