#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
# @Time    : 2024/2/18 22:46
# @Author  : lqh
# @python-version 3.10
# @File    : tool_func.py
# @Software: PyCharm
"""
import cv2
import numpy as np
import torch

def resize_and_bgr2bin(image):
    image = cv2.resize(image, (84, 84))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    thresh, image = cv2.threshold(image, 199, 1, cv2.THRESH_BINARY_INV)
    return image

def image_to_tensor(image):
    image_tensor = image.transpose(2, 0, 1)
    image_tensor = image_tensor.astype(np.float32)
    image_tensor = torch.from_numpy(image_tensor)
    if torch.cuda.is_available():  # put on GPU if CUDA is available
        image_tensor = image_tensor.cuda()
    return image_tensor

def process_state(state):  # make it  a batch input
    """state is rgb img"""
    state = resize_and_bgr2bin(state)
    state = np.expand_dims(state, axis=0)
    return state
