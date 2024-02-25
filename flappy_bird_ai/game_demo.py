#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/4 17:45
# @Author  : lqh
# @python-version 3.10
# @File    : game_demo.py
# @Software: PyCharm
"""
from itertools import cycle
import sys
import pygame
import random


######################################## 定义变量
MAP_WIDTH = 360  # 地图大小
MAP_HEIGHT = 450
BIRD_WIDTH, BIRD_HEIGHT = 30, 25
PIPE_WIDTH = BIRD_WIDTH
FPS = 30  # 刷新率
PIPE_GAPS = [80, 90, 100, 110, 120]  # 缺口的距离 有这6个随机距离
PIPE_HEIGHT_RANGE = [int(MAP_HEIGHT * 0.3), int(MAP_HEIGHT * 0.7)]  # 管道长度范围
PIPE_DISTANCE = 120  # 管道之间距离

######################################## 游戏基本设置
pygame.init()  # 进行初始化
SCREEN = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))  # 调用窗口设置屏幕大小
TITLE_TEXT = "flappy bird"
pygame.display.set_caption(TITLE_TEXT)  # 标题
CLOCK = pygame.time.Clock()  # 建立时钟
FONT_NAME = "fangsong"
FONT = pygame.font.SysFont(FONT_NAME, 20)
FONT.bold = True


######################################## 加载素材
SPRITE_FILE = './assets/images/'
# 列表推导式 三个鸟的图片和三种状态
IMG_LIST_BIRDS = [f'{SPRITE_FILE}bird_{move}.png' for move in ['up', 'middle', 'down']]
IMG_LIST_BGS = [SPRITE_FILE + 'day.png', SPRITE_FILE + 'night.png']
IMG_PIPE = SPRITE_FILE + 'pipe.png'

# 将图片设置成一个大字典 里面通过key-value存不同的场景图
IMAGES = {}
# IMAGES['numbers'] = [pygame.image.load(number) for number in NUMBERS]  # 数字素材有10张 因此遍历
# IMAGES['guide'] = pygame.image.load(SPRITE_FILE + 'guide.png')
# IMAGES['gameover'] = pygame.image.load(SPRITE_FILE + 'gameover.png')
# IMAGES['floor'] = pygame.image.load(SPRITE_FILE + 'floor.png')
IMAGES['bg_img'] = pygame.transform.smoothscale(pygame.image.load(random.choice(IMG_LIST_BGS)).convert_alpha(),
                                                (MAP_WIDTH, MAP_HEIGHT))  # random的choice方法可以随机从列表里返回一个元素 白天或者黑夜
IMAGES['bird_imgs'] = [pygame.transform.smoothscale(pygame.image.load(frame).convert_alpha(), (BIRD_WIDTH, BIRD_HEIGHT)) for frame
                       in IMG_LIST_BIRDS]  # 列表推导式
pipe = pygame.image.load(IMG_PIPE)
# pipe_height = int(PIPE_WIDTH * (pipe.get_height() / pipe.get_width()))
pipe_height = min(pipe.get_height(), MAP_HEIGHT)
pipe = [pygame.transform.smoothscale(pipe, (PIPE_WIDTH, pipe_height)).convert_alpha()]
pipe_transform = [pygame.transform.flip(p, False, True).convert_alpha() for p in pipe]  # flip是翻转 将管道放下面和上面 False水平不动，True上下翻转
IMAGES['pipe'] = pipe + pipe_transform


# 地板的高是一个很常用的变量 因此我们专门拿出来
# FLOOR_H = MAP_HEIGHT - IMAGES['floor'].get_height()  # 屏幕高减去floor图片的高 就是他在屏幕里的位置
FLOOR_H = MAP_HEIGHT  # 屏幕高减去floor图片的高 就是他在屏幕里的位置

SPRITE_SOUND = './assets/sounds/'
SOUNDS = {}  # 同理声音素材也这样做
SOUNDS['btn_click'] = pygame.mixer.Sound(SPRITE_SOUND + 'btn_click.wav')
SOUNDS['game_over'] = pygame.mixer.Sound(SPRITE_SOUND + 'game_over.wav')
SOUNDS['hit'] = pygame.mixer.Sound(SPRITE_SOUND + 'hit.wav')
SOUNDS['jump'] = pygame.mixer.Sound(SPRITE_SOUND + 'jump.wav')
SOUNDS['main_theme'] = pygame.mixer.Sound(SPRITE_SOUND + 'main_theme.wav')
SOUNDS['world_clear'] = pygame.mixer.Sound(SPRITE_SOUND + 'world_clear.wav')
SOUNDS['score'] = pygame.mixer.Sound(SPRITE_SOUND + 'score.mp3')

# 执行函数
def main():
    running = True
    max_score = 0
    while running:
        SOUNDS['main_theme'].play(-1)  # -1表示循环播放
        title_width, title_height = FONT.size(TITLE_TEXT.upper())
        bird_x, bird_y = 40, title_height + 10
        player_1 = Bird(bird_x, bird_y)

        # 最初的画面
        start_window(player_1)
        cur_score = game_window(player_1)
        max_score = over_window(cur_score, max_score)

def start_window(player_1):
    titleTextSurface = FONT.render(TITLE_TEXT.upper(), True, (0, 0, 0))
    title_width, title_height = FONT.size(TITLE_TEXT.upper())
    hit_string = "Press Space to Start"
    hitTextSurface = FONT.render(hit_string, True, (0,0,0))
    hit_string_width, hit_string_height = FONT.size(hit_string)
    SCREEN.blit(IMAGES['bg_img'], (0, 0))
    SCREEN.blit(player_1.image, player_1.rect)
    SCREEN.blit(titleTextSurface, ((MAP_WIDTH - title_width) // 2, 10))
    SCREEN.blit(hitTextSurface, ((MAP_WIDTH - hit_string_width) // 2, 10 + title_height))

    while True:
        for event in pygame.event.get():  # 监控行为
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        # SCREEN.blit(IMAGES['bg_img'], (0, 0))
        pygame.display.flip()
        CLOCK.tick(FPS)  # 以每秒30帧刷新屏幕

def game_window(player_1):
    # 管道
    n_pair = round(MAP_WIDTH / PIPE_DISTANCE)  # 四舍五入取整数 屏幕宽度/两个管道之间的距离 这个距离时候刷新第二个管道  2.4
    pipe_group = pygame.sprite.Group()  # 是一个集合

    # 添加最开始的两个管道
    # 每次添加正反两个管道
    pipe_x = MAP_WIDTH
    pipe_y = random.randint(PIPE_HEIGHT_RANGE[0], PIPE_HEIGHT_RANGE[1])  # 管道长度随机从153.6 到 358.4
    pipe1 = Pipe(pipe_x, pipe_y, upwards=True)  # 创建一个管道对象
    pipe_group.add(pipe1)  # 将对象添加到这个精灵集合里面
    pipe2 = Pipe(pipe_x, pipe_y - random.choice(PIPE_GAPS), upwards=False)  # 翻转的管道
    pipe_group.add(pipe2)
    score = 0
    while True:
        flap_flag = False
        SCREEN.blit(IMAGES['bg_img'], (0, 0))
        SCREEN.blit(player_1.image, player_1.rect)

        # 当小鸟左边大于 管道右边就得分
        tmp_pipe = pipe_group.sprites()[0]
        if not tmp_pipe.get_score_flag() and tmp_pipe.rect.right < player_1.rect.left:
            tmp_pipe.set_score_flag(True)
            SOUNDS['score'].play()
            score += 1
        pipe_group.update()
        pipe_group.draw(SCREEN)
        SCREEN.blit(FONT.render(f"{score}", True, (0, 0, 0)), (MAP_WIDTH - 50, 10))

        dt = CLOCK.tick(FPS) / 1000  # 以每秒30帧刷新屏幕
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player_1.rect.x -= player_1.x_speed * dt
        if keys[pygame.K_d]:
            player_1.rect.x += player_1.x_speed * dt
        for event in pygame.event.get():  # 监控行为
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flap_flag = True
            # 检查是否为鼠标按键按下事件
            if event.type == pygame.MOUSEBUTTONDOWN:
                # 判断是否为左键按下
                if event.button == 1:  # 左键对应的编号是1
                    flap_flag = True
        player_1.update(dt, flap_flag)
        # 生成管道
        # 生成最后一个管道
        if len(pipe_group) / 2 < n_pair:  # 当管道组长度<2.4 时 意思就是两个半管道的时候
            # sprites()将管道组返回成列表
            last_pipe = pipe_group.sprites()[-1]
            pipe_x = last_pipe.rect.right + PIPE_DISTANCE
            pipe_y = random.randint(PIPE_HEIGHT_RANGE[0], PIPE_HEIGHT_RANGE[1])
            pipe1 = Pipe(pipe_x, pipe_y, upwards=True)
            pipe_group.add(pipe1)
            pipe2 = Pipe(pipe_x, pipe_y - random.choice(PIPE_GAPS), upwards=False)
            pipe_group.add(pipe2)

        # 检测鸟与管道是否碰撞
        # 鸟的矩形y坐标如果大于地板的高度 就死亡
        # pygame.sprite.spritecollideany 碰撞函数 如果bird和pipe_group碰撞了 就死亡
        if player_1.rect.y > MAP_HEIGHT or player_1.rect.y < 0 or pygame.sprite.spritecollideany(player_1, pipe_group):
            SOUNDS['main_theme'].stop()
            SOUNDS['hit'].play()
            SOUNDS['game_over'].play()
            player_1.go_die()
            return score
        pygame.display.flip()


def over_window(cur_score, max_score):
    if max_score < cur_score:
        max_score = cur_score
    score_string = f"{cur_score}/{max_score}"
    scoreTextSurface = FONT.render(score_string, True, (0,0,0))
    score_string_width, score_string_height = FONT.size(score_string)
    SCREEN.blit(scoreTextSurface, ((MAP_WIDTH - score_string_width) // 2, MAP_HEIGHT // 2 - score_string_height - 10))
    hit_string = "Press R to Restart"
    hitTextSurface = FONT.render(hit_string, True, (0, 0, 0))
    hit_string_width, hit_string_height = FONT.size(hit_string)
    SCREEN.blit(hitTextSurface, ((MAP_WIDTH - hit_string_width) // 2, MAP_HEIGHT // 2))
    while True:
        for event in pygame.event.get():  # 监控行为
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                SOUNDS['game_over'].stop()
                return max_score
        pygame.display.flip()
        CLOCK.tick(FPS)

class Bird(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self) # 必须这么写
        # pygame.sprite.Sprite.__init__(self)
        self.frames = IMAGES['bird_imgs']  # 鸟儿框架
        self.bird_frame_change_rate = 3
        self.frame_list = [0] * self.bird_frame_change_rate + [1] * self.bird_frame_change_rate \
                          + [2] * self.bird_frame_change_rate + [1] * self.bird_frame_change_rate
        # self.frame_list = cycle([0, 1, 2, 1])  # 控制小鸟翅膀运动上中下
        self.frame_index = 0
        self.image = self.frames[self.frame_list[self.frame_index]]  # 和菜单界面小鸟扇翅膀一个原理
        self.rect = self.image.get_rect()  # 鸟儿的矩形
        self.rect.x = x
        self.rect.y = y
        self.y_vel = 0  # 沿y轴方向的速度，有正有负
        self.gravity_acc = int(MAP_HEIGHT * 2.5)  # 重力
        self.flap_acc = -6 * self.gravity_acc  # 翅膀拍打往上飞 y坐标-10
        self.max_y_vel = 10 * self.gravity_acc  # y轴最大速度


        self.rotate = 0  # 脑袋朝向, rotate为0就是初始朝鲜
        self.rotate_acc = -900 # 转向加速度
        self.rotate_vel = 0  # 转向速度
        self.max_rotate = -900  # 最大转向速度
        self.flap_rotate = 45  # 按了空格只会脑袋朝向上45度
        self.x_speed = int(MAP_WIDTH * 1)  # AD控制左右移动

    def update(self, dt, flap=False):  # 更新速度、帧和图片坐标
        if flap:
            self.y_vel = self.flap_acc * dt  # 拍打翅膀 则y速度-10向上
            self.rotate_vel = 0
            self.rotate = self.flap_rotate
            SOUNDS['jump'].play()
        else:
            tmp = self.rotate_vel + self.rotate_acc * dt
            self.rotate_vel = max(tmp, self.max_rotate)
            tmp = self.rotate + self.rotate_vel * dt
            self.rotate = max(-70, tmp)  # 根据图片调整转向的最小的角度是-70度
            tmp = self.y_vel + self.gravity_acc * dt
            self.y_vel = max(tmp, -self.max_y_vel) if tmp <= 0 else min(tmp, self.max_y_vel)
        self.rect.y += self.y_vel * dt  # 小鸟向上移动的距离
        self.frame_index += 1  # 扇翅膀的速率
        # if self.frame_index % self.bird_frame_change_rate == 0:
        #     self.frame_index = 0
        self.frame_index %= len(self.frame_list)
        self.image = self.frames[self.frame_list[self.frame_index]]
        self.image = pygame.transform.rotate(self.image, self.rotate)  # transform变形方法 旋转

    def go_die(self):
        self.y_vel = 0
        self.rotate_vel = 0
        self.gravity_acc = 0
        self.rotate_acc = 0
        self.flap_acc = 0


class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, upwards=True):
        pygame.sprite.Sprite.__init__(self)
        self.x_vel = -4  # 管道移动速度
        self.score_flag = False
        # 默认属性为真 则是正向管道
        if upwards:
            self.image = IMAGES['pipe'][0]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.top = y
        # 利用flip方法 旋转管道成为反向管道
        else:
            self.image = IMAGES['pipe'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y

    def update(self):
        self.rect.x += self.x_vel  # 管道x轴加移动速度
        if self.rect.right < 0:
            self.kill()

    def set_score_flag(self, flag):
        self.score_flag = flag

    def get_score_flag(self):
        return self.score_flag


if __name__ == '__main__':
    main()
