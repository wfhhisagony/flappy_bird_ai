#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/15 10:46
# @Author  : lqh
# @python-version 3.10
# @File    : __init__.py
# @Software: PyCharm
"""
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Exporting gym.make  this import is necessary
from gym import make

# Registering environments:
from gym.envs.registration import register
from .flappy_bird_env import FlappyBirdEnv
from .game_logic import FlappyBirdLogic

register(
    id="FlappyBird-rgb-v0",
    entry_point="my_env:FlappyBirdEnv",
)




