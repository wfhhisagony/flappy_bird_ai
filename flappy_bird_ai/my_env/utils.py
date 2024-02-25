# MIT License
#
# Copyright (c) 2020 Gabriel Nogueira (Talendar)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

""" Utility functions.

Some of the code in this module is an adaption of the code in the `FlapPyBird`
GitHub repository by `sourahbhv` (https://github.com/sourabhv/FlapPyBird),
released under the MIT license.
"""

import os
from pathlib import Path
import sys
from typing import Any, Dict, List, Optional

from pygame import image as pyg_image
from pygame import mixer as pyg_mixer
from pygame import Rect
from pygame.transform import flip as img_flip
from pygame.transform import smoothscale


_BASE_DIR = Path(os.path.dirname(os.path.realpath(__file__))).parent

SPRITES_PATH = str(_BASE_DIR / "assets/images")
AUDIO_PATH = str(_BASE_DIR / "assets/sounds")

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 25

BACKGROUND_WIDTH = 360
BACKGROUND_HEIGHT = 450

PIPE_WIDTH = PLAYER_WIDTH
PIPE_HEIGHT = int(BACKGROUND_HEIGHT * 0.7)


def pixel_collision(rect1: Rect,
                    rect2: Rect,
                    hitmask1: List[List[bool]],
                    hitmask2: List[List[bool]]) -> bool:
    """ Checks if two objects collide and not just their rects. """
    rect = rect1.clip(rect2)

    if rect.width == 0 or rect.height == 0:
        return False

    x1, y1 = rect.x - rect1.x, rect.y - rect1.y
    x2, y2 = rect.x - rect2.x, rect.y - rect2.y

    for x in range(rect.width):
        for y in range(rect.height):
            if hitmask1[x1+x][y1+y] and hitmask2[x2+x][y2+y]:
                return True
    return False


def get_hitmask(image) -> List[List[bool]]:
    """ Returns a hitmask using an image's alpha. """
    mask = []
    for x in range(image.get_width()):
        mask.append([])
        for y in range(image.get_height()):
            mask[x].append(bool(image.get_at((x, y))[3]))
    return mask


def _load_sprite(filename, convert, alpha=True):
    img = pyg_image.load(f"{SPRITES_PATH}/{filename}")
    return (img.convert_alpha() if convert and alpha
            else img.convert() if convert
            else img)


def load_images(convert: bool = True,
                bg_type: Optional[str] = None) -> Dict[str, Any]:  # 根据game_logic调整的图片大小(写死的)
    """ Loads and returns the image assets of the game. """
    images = {}

    try:
        # Sprites with the number for the score display:
        # images["numbers"] = tuple([
        #     _load_sprite(f"{n}.png", convert=convert, alpha=True)
        #     for n in range(10)
        # ])

        # Game over sprite:
        # images["gameover"] = _load_sprite("gameover.png",
        #                                   convert=convert, alpha=True)

        # Welcome screen message sprite:
        # images["message"] = _load_sprite("message.png",
        #                                  convert=convert, alpha=True)

        # Sprite for the base (ground):
        # images["base"] = _load_sprite("base.png",
        #                               convert=convert, alpha=True)

        # Background sprite:
        if bg_type is None:
            images["background"] = None
        else:
            images["background"] = smoothscale(_load_sprite(f"{bg_type}.png",
                                                convert=convert, alpha=False), (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

        # Bird sprites:
        images["player"] = (
            smoothscale(_load_sprite(f"bird_up.png",
                         convert=convert, alpha=True),(PLAYER_WIDTH, PLAYER_HEIGHT)),
            smoothscale(_load_sprite(f"bird_middle.png",
                         convert=convert, alpha=True),(PLAYER_WIDTH, PLAYER_HEIGHT)),
            smoothscale(_load_sprite(f"bird_down.png",
                         convert=convert, alpha=True),(PLAYER_WIDTH, PLAYER_HEIGHT)),
        )

        # Pipe sprites:
        pipe_sprite = smoothscale(_load_sprite(f"pipe.png",
                                   convert=convert, alpha=True),(PIPE_WIDTH, PIPE_HEIGHT))
        images["pipe"] = (img_flip(pipe_sprite, False, True),
                          pipe_sprite)  # up_pipe and low_pipe
    except FileNotFoundError as ex:
        raise FileNotFoundError("Can't find the sprites folder! No such file or"
                                f" directory: {SPRITES_PATH}") from ex

    return images


def load_sounds() -> Dict[str, pyg_mixer.Sound]:
    """ Loads and returns the audio assets of the game. """
    pyg_mixer.init()
    sounds = {}
    try:
        sounds["game_over"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "game_over.wav"))
        sounds["hit"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "hit.wav"))
        sounds["score"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "score.mp3"))
        sounds["jump"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "jump.wav"))
        sounds["btn_click"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "btn_click.wav"))
        sounds["main_theme"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "main_theme.mp3"))
        sounds["world_clear"] = pyg_mixer.Sound(os.path.join(AUDIO_PATH, "world_clear.wav"))
    except FileNotFoundError as ex:
        raise FileNotFoundError("Can't find the audio folder! No such file or "
                                f"directory: {AUDIO_PATH}") from ex

    return sounds
