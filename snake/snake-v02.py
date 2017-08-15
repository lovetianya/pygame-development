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

HARD_LEVEL = list(range(4, int(FPS/2), 2))
hardness = HARD_LEVEL[0]

D_LEFT, D_RIGHT, D_UP, D_DOWN = 0, 1, 2, 3

# 初始化
pygame.init()

# 要想载入音乐，必须要初始化 mixer
pygame.mixer.init()

WIDTH, HEIGHT = 500, 500
SCREEN_WIDTH = WIDTH + 200

# 贪吃蛇小方块的宽度
CUBE_WIDTH = 20

# 计算屏幕的网格数，网格的大小就是小蛇每一节身体的大小
GRID_WIDTH_NUM, GRID_HEIGHT_NUM = int(WIDTH / CUBE_WIDTH),\
                                  int(HEIGHT / CUBE_WIDTH)

# 设置画布
screen = pygame.display.set_mode((SCREEN_WIDTH, HEIGHT))

# 设置标题
pygame.display.set_caption("贪吃蛇")


# 设置游戏的根目录为当前文件夹
base_folder = os.path.dirname(__file__)

# 这里需要在当前目录下创建一个名为music的目录，并且在里面存放名为back.mp3的背景音乐
music_folder = os.path.join(base_folder, 'music')

# 背景音乐
back_music = pygame.mixer.music.load(os.path.join(music_folder, 'back.mp3'))

# 小蛇吃食物的音乐
bite_sound = pygame.mixer.Sound(os.path.join(music_folder, 'armor-light.wav'))

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

# 设置计数器
counter = 0


# 画出网格线
def draw_grids():
    for i in range(GRID_WIDTH_NUM):
        pygame.draw.line(screen, LINE_COLOR,
                         (i * CUBE_WIDTH, 0), (i * CUBE_WIDTH, HEIGHT))

    for i in range(GRID_HEIGHT_NUM):
        pygame.draw.line(screen, LINE_COLOR,
                         (0, i * CUBE_WIDTH), (WIDTH, i * CUBE_WIDTH))

    pygame.draw.line(screen, WHITE,
                     (WIDTH, 0), (WIDTH, HEIGHT))


# 打印身体的函数
def draw_body(status):
    for sb in status.snake_body[1:]:
        screen.blit(food, sb)

    if status.direction == D_LEFT:
        rot = 0
    elif status.direction == D_RIGHT:
        rot = 180
    elif status.direction == D_UP:
        rot = 270
    elif status.direction == D_DOWN:
        rot = 90
    new_head_img = pygame.transform.rotate(snake_head_img, rot)
    head = pygame.transform.scale(new_head_img, (CUBE_WIDTH, CUBE_WIDTH))
    screen.blit(head, status.snake_body[0])


# 随机产生一个事物
def generate_food(status=None):
    while True:
        pos = (random.randint(0, GRID_WIDTH_NUM - 1),
               random.randint(0, GRID_HEIGHT_NUM - 1))

        if status is None:
            return pos

        # 如果当前位置没有小蛇的身体，我们就跳出循环，返回食物的位置
        if not (pos[0] * CUBE_WIDTH, pos[1] * CUBE_WIDTH) in status.snake_body:
            return pos


# 画出食物的主体
def draw_food(statis):
    screen.blit(food, (status.food_pos[0] * CUBE_WIDTH,
                      status.food_pos[1] * CUBE_WIDTH, CUBE_WIDTH, CUBE_WIDTH))


# 判断贪吃蛇是否吃到了事物，如果吃到了我们就加长小蛇的身体
def grow(status):
    if status.snake_body[0][0] == status.food_pos[0] * CUBE_WIDTH and\
            status.snake_body[0][1] == status.food_pos[1] * CUBE_WIDTH:
        # 每次吃到食物，就播放音效
        bite_sound.play()
        return True

    return False


class GameStatus():
    def __init__(self):
        self.reset_game_status()

    # 重置所有的状态为初始态
    def reset_game_status(self):
        self.food_pos = generate_food()
        self.direction = D_LEFT
        self.game_is_over = True
        self.running = True
        self.hardness = HARD_LEVEL[0]
        self.score = 0

        # 每次小蛇身体加长的时候，我们就将身体的位置加到列表末尾
        self.snake_body = [(int(GRID_WIDTH_NUM / 2) * CUBE_WIDTH,
                            int(GRID_HEIGHT_NUM / 2) * CUBE_WIDTH)]


def show_text(surf, text, size, x, y, color=WHITE):
    font_name = os.path.join(base_folder, 'font/font.ttc')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def show_welcome(screen):
    show_text(screen, u'欢乐贪吃蛇', 30, WIDTH / 2, HEIGHT / 2)
    show_text(screen, u'按任意键开始游戏', 20, WIDTH / 2, HEIGHT / 2 + 50)


def show_scores(screen, status):
    show_text(screen, u'级别: {}'.format(status.hardness), CUBE_WIDTH,
        WIDTH + CUBE_WIDTH * 3, CUBE_WIDTH * 4)

    show_text(screen, u'得分: {}'.format(status.score), CUBE_WIDTH,
        WIDTH + CUBE_WIDTH * 3, CUBE_WIDTH * 6)


# 定义一个类的实例，用于保存当前游戏状态
draw_grids()
pygame.display.update()
status = GameStatus()
while status.running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            status.running = False
        elif event.type == pygame.KEYDOWN:      # 如果有按键被按下了
            # 如果本局游戏已经结束（或者没有开始），那么按任意键开始游戏
            if status.game_is_over:
                # 重置游戏状态
                status.reset_game_status()
                status.game_is_over = False
                break

            # 判断按键类型
            if event.key == pygame.K_UP:
                status.direction = D_UP
            elif event.key == pygame.K_DOWN:
                status.direction = D_DOWN
            elif event.key == pygame.K_LEFT:
                status.direction = D_LEFT
            elif event.key == pygame.K_RIGHT:
                status.direction = D_RIGHT

    if status.game_is_over:
        show_welcome(screen)
        pygame.display.update()
        continue

    # 判断计数器是否符合要求，如果符合就移动方块位置，（调整方块位置）
    if counter % int(FPS / status.hardness) == 0:
        # 这里需要保存一下尾部的位置，因为下文我们要更新这个位置
        # 在这种情况下如果小蛇迟到了食物，需要在尾部增长，那么我们
        # 就不知道添加到什么地方了～～
        last_pos = status.snake_body[-1]

        # 更新小蛇身体的位置
        for i in range(len(status.snake_body) - 1, 0, -1):
            status.snake_body[i] = status.snake_body[i - 1]

        # 改变头部的位置
        if status.direction == D_UP:
            status.snake_body[0] = (
                status.snake_body[0][0],
                status.snake_body[0][1] - CUBE_WIDTH)
        elif status.direction == D_DOWN:
            status.snake_body[0] = (
                status.snake_body[0][0],
                status.snake_body[0][1] + CUBE_WIDTH)
        elif status.direction == D_LEFT:
            status.snake_body[0] = (
                status.snake_body[0][0] - CUBE_WIDTH,
                status.snake_body[0][1])
        elif status.direction == D_RIGHT:
            status.snake_body[0] = (
                status.snake_body[0][0] + CUBE_WIDTH,
                status.snake_body[0][1])

        # 限制小蛇的活动范围
        if status.snake_body[0][0] < 0 or status.snake_body[0][0] >= WIDTH or\
                status.snake_body[0][1] < 0 or status.snake_body[0][1] >= HEIGHT:
            # 超出屏幕之外游戏结束
            status.game_is_over = True
            show_text(screen, u'你挂了', 30, WIDTH / 2, HEIGHT / 2)
            pygame.display.update()
            pygame.time.delay(2000)

        # 限制小蛇不能碰到自己的身体
        for sb in status.snake_body[1: ]:
            # 身体的其他部位如果和蛇头（snake_body[0]）重合就死亡
            if sb == status.snake_body[0]:
                status.game_is_over = True
                show_text(screen, u'你挂了', 30, WIDTH / 2, HEIGHT / 2)
                pygame.display.update()
                pygame.time.delay(2000)

        # 判断小蛇是否吃到了事物，吃到了就成长
        got_food = grow(status)

        # 如果吃到了食物我们就产生一个新的食物
        if got_food:
            status.score += status.hardness
            status.food_pos = generate_food(status)
            status.snake_body.append(last_pos)
            status.hardness = HARD_LEVEL[min(int(len(status.snake_body) / 10),
                                      len(HARD_LEVEL) - 1)]

    # screen.fill(BLACK)
    pygame.draw.rect(screen, BLACK, (WIDTH, 0, SCREEN_WIDTH - WIDTH, HEIGHT))
    screen.blit(background, (0, 0))
    draw_grids()

    # 画小蛇的身体
    draw_body(status)

    # 画出食物
    draw_food(status)

    show_scores(screen, status)

    # 计数器加一
    counter += 1
    pygame.display.update()

pygame.quit()
