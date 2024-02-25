#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/18 22:09
# @Author  : lqh
# @python-version 3.10
# @File    : DQN_net.py
# @Software: PyCharm
"""
import torch.nn as nn
from collections import deque, namedtuple

import random


Transition = namedtuple('Transition',
                        ('state', 'action', 'next_state', 'reward'))


class ReplayMemory(object):

    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        """Save a transition"""
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQN(nn.Module):
    """
        input: shape(batch_size, 4,84,84)
    """
    def __init__(self, frame_num=4, n_actions=2):
        super(DQN, self).__init__()
        # 参数
        self.number_of_actions = n_actions

        self.conv1 = nn.Conv2d(frame_num, 32, 8, 4)  # (84-8)/4+1 = 20
        self.relu1 = nn.ReLU()
        self.conv2 = nn.Conv2d(32, 64, 4, 2)  # (20-4)/2+1=9
        self.relu2 = nn.ReLU()
        self.conv3 = nn.Conv2d(64, 64, 3, 1)  # (9-3)/1+1 = 7
        self.relu3 = nn.ReLU()
        self.fc4 = nn.Linear(3136, 512)  # 7x7x64 = 3136
        self.relu4 = nn.ReLU()
        self.fc5 = nn.Linear(512, self.number_of_actions)

    def forward(self, x):

        out = self.conv1(x)
        out = self.relu1(out)
        out = self.conv2(out)
        out = self.relu2(out)
        out = self.conv3(out)
        out = self.relu3(out)
        out = out.view(out.size()[0], -1)
        out = self.fc4(out)
        out = self.relu4(out)
        out = self.fc5(out)

        return out
