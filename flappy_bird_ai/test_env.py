#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/18 0:28
# @Author  : lqh
# @python-version 3.10
# @File    : test_env.py
# @Software: PyCharm
"""
import time
import my_env
import pygame
import sys
pygame.init()
CLOCK = pygame.time.Clock()
FPS = 30
def hunman_agent_env():
    env = my_env.make("FlappyBird-rgb-v0")
    env.reset()
    score = 0
    while True:
        env.render()

        # Getting random action:
        action = 0
        for event in pygame.event.get():  # 监控行为
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                action = 1

        # Processing:
        obs, reward, done, _ = env.step(action)

        score += reward
        print(f"Obs: {obs}\n"
              f"Action: {action}\n"
              f"Score: {score}\n")

        CLOCK.tick(FPS)


        if done:
            env.render()
            CLOCK.tick(FPS)
            env.reset()
if __name__ == '__main__':
    hunman_agent_env()