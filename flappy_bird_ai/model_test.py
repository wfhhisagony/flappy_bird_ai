#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/18 22:08
# @Author  : lqh
# @python-version 3.10
# @File    : model_test.py
# @Software: PyCharm
"""
from my_model.DQN_net import DQN
import torch
import torch.optim as optim

import my_env
import my_tool_func
import numpy as np
import pygame

def load_state(policy_net, target_net):
    path1 = 'my_model/policy_net.pkl'
    path2 = 'my_model/target_net.pkl'
    policy_net.load_state_dict(torch.load(path1))
    target_net.load_state_dict(torch.load(path2))
# if GPU is to be used
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

env = my_env.make("FlappyBird-rgb-v0")
# Get number of actions from gym action space
n_actions = env.action_space.n
# Get the number of state observations
n_observations = 4  # each time use four frames

policy_net = DQN(n_observations, n_actions).to(device)
target_net = DQN(n_observations, n_actions).to(device)  # not used
load_state(policy_net, target_net)
CLOCK = pygame.time.Clock()
FPS = 60

if __name__ == '__main__':

    for i in range(1000):
        state = env.reset()  # rgb img data:shape(360,450,3)
        state = my_tool_func.process_state(state)
        state = np.repeat(state, 4, axis=0)  # 最开始将四帧图片全部初始化为第一帧图片
        state = torch.tensor(state, dtype=torch.float32, device=device).unsqueeze(0)  # 作成batch
        done = False
        reward = 0
        policy_net.eval()
        while not done:
            env.render()
            action = policy_net(state).max(1).indices.view(1, 1)
            observation, reward, done, info = env.step(action.item())
            if done:
                next_state = None
            else:
                next_state = my_tool_func.process_state(observation)
                next_state = torch.tensor(next_state, dtype=torch.float32, device=device)
                next_state = torch.cat((state.squeeze(0)[1:, :, :], next_state)).unsqueeze(0)  # 更新帧组
            for event in pygame.event.get():  # 监控行为
                if event.type == pygame.QUIT:
                    env.close()
            # Move to the next state
            state = next_state
            # reward += transition[1]
            CLOCK.tick(FPS)