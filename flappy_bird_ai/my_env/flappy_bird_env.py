#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/15 22:08
# @Author  : lqh
# @python-version 3.10
# @File    : flappy_bird_env.py
# @Software: PyCharm
"""
from typing import Dict, Tuple, Optional, Union

import gym
import numpy as np
import pygame
from .renderer import FlappyBirdRenderer
from .game_logic import FlappyBirdLogic

class FlappyBirdEnv(gym.Env):  # custom env using gym
    metadata = {"render.modes": ["human", "rgb_array"]}  # 其实在这里human mode 和 rgb_array没什么区别,就是render函数返回不同而已,不过压根不会用render函数的返回值

    def __init__(self,
                 screen_size: Tuple[int, int] = (360, 450),
                 pipe_gap: int = 100,
                 background: Optional[str] = None
                 ):
        self.action_space = gym.spaces.Discrete(2)
        self.observation_space = gym.spaces.Box(0, 255, [*screen_size, 3])
        self._screen_size = screen_size
        self._pipe_gap = pipe_gap

        self._game = None  # game_logic的实例
        self._renderer = FlappyBirdRenderer(screen_size=self._screen_size,
                                            background=background)

    def _get_observation(self):
        self._renderer.draw_surface(show_score=False)
        return pygame.surfarray.array3d(self._renderer.surface)  # 返回的是图片矩阵

    def reset(self):
        """ Resets the environment (starts a new game).
        return a current game screen shot and don't include a info_dict
        """
        self._game = FlappyBirdLogic(screen_size=self._screen_size,
                                     pipe_gap_size=self._pipe_gap)

        self._renderer.game = self._game
        return self._get_observation()



    def step(self,
             action: Union[FlappyBirdLogic.Actions, int],
         )-> Tuple[np.ndarray, float, bool, Dict]:
        """
        :param
            action(Union[FlappyBirdLogic.Actions, int]): The action taken by
                the agent. Zero (0) means "do nothing" and one (1) means "flap".
        :return:
         A tuple containing, respectively:

                * an observation (RGB-array representing the game's screen);
                * a reward (always 1);
                * a status report (`True` if the game is over and `False`
                  otherwise);
                * an info dictionary.
        """
        alive = self._game.update_state(action)
        obs = self._get_observation()

        reward = 0.1   # redefined reward，你可能需要重新定义reward在你自己的游戏中
        done = not alive
        if done:
            reward = -2.8
        elif self._game.sound_cache == 'score':
            reward = 2.8

        info = {"score": self._game.score}

        return obs, reward, done, info

    def render(self, mode="human") -> Optional[np.ndarray]:
        """
        If ``mode`` is:

            - human: render to the current display. Usually for human
              consumption.
            - rgb_array: Return an numpy.ndarray with shape (x, y, 3),
              representing RGB values for an x-by-y pixel image, suitable
              for turning into a video.
        :return:
            `None` if ``mode`` is "human" and a numpy.ndarray with RGB values if
            it's "rgb_array"
        """
        if mode not in FlappyBirdEnv.metadata["render.modes"]:
            raise ValueError("Invalid render mode!")

        self._renderer.draw_surface(show_score=True)
        if mode == "rgb_array":
            return pygame.surfarray.array3d(self._renderer.surface)  # infact not need this return, use step()'s return is enough
        else:
            if self._renderer.display is None:
                self._renderer.make_display()

            self._renderer.update_display()

    def close(self):
        """ Closes the environment. """
        if self._renderer is not None:
            pygame.display.quit()
            self._renderer = None
        super().close()