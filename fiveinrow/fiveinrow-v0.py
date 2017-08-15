# -*- coding: utf-8 -*-
# 导入我们需要用到的包
import pygame
import os

# 初始化我们的pygame
pygame.init()

# 初始化mixer （因为下文我们需要用到音乐）
pygame.mixer.init()

# 设置我们的屏幕大小和标题

# 定义一些颜色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 720
GRID_WIDTH = WIDTH // 20
HEIGHT = 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("五子棋")

# 设置一个定时器，用于固定时间刷新屏幕，而不是一直不停的刷新，浪费CPU资源
FPS = 30
clock = pygame.time.Clock()

# 加载背景图片
base_folder = os.path.dirname(__file__)
img_folder = os.path.join(base_folder, 'images')
background_img = pygame.image.load(os.path.join(img_folder, 'back.png')).convert()


# 画出棋盘
def draw_background(surf):
    # 加载背景图片
    surf.blit(background_img, (0, 0))

    # 画网格线，棋盘为 19行 19列的
    # 1. 画出边框，这里 GRID_WIDTH = WIDTH // 20
    rect_lines = [
        ((GRID_WIDTH, GRID_WIDTH), (GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((GRID_WIDTH, GRID_WIDTH), (WIDTH - GRID_WIDTH, GRID_WIDTH)),
        ((GRID_WIDTH, HEIGHT - GRID_WIDTH),
            (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
        ((WIDTH - GRID_WIDTH, GRID_WIDTH),
            (WIDTH - GRID_WIDTH, HEIGHT - GRID_WIDTH)),
    ]
    for line in rect_lines:
        pygame.draw.line(surf, BLACK, line[0], line[1], 2)

    # 画出中间的网格线
    for i in range(17):
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH * (2 + i), GRID_WIDTH),
                         (GRID_WIDTH * (2 + i), HEIGHT - GRID_WIDTH))
        pygame.draw.line(surf, BLACK,
                         (GRID_WIDTH, GRID_WIDTH * (2 + i)),
                         (HEIGHT - GRID_WIDTH, GRID_WIDTH * (2 + i)))

    # 画出棋盘中的五个点，围棋棋盘上为9个点，这里我们只画5个
    circle_center = [
        (GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, GRID_WIDTH * 4),
        (WIDTH - GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
        (GRID_WIDTH * 4, HEIGHT - GRID_WIDTH * 4),
        (GRID_WIDTH * 10, GRID_WIDTH * 10)
    ]
    for cc in circle_center:
        pygame.draw.circle(surf, BLACK, cc, 5)


running = True
while running:
    # 设置屏幕刷新频率
    clock.tick(FPS)

    # 处理不同事件
    for event in pygame.event.get():
        # 检查是否关闭窗口
        if event.type == pygame.QUIT:
            running = False

    # 画出棋盘
    draw_background(screen)

    # 刷新屏幕
    pygame.display.flip()