import math

import pygame
from miniworldmaker.appearances import appearance as appear


class Costume(appear.Appearance):
    """ A costume contains one or multiple images

    Every token has a costume which defines the "look" of the token.
    You can switch the images in a costume to animate the token.

    A costume is created if you add an image to an actor with token.add_image(path_to_image)
    """

    def __init__(self, token):
        super().__init__()
        self.parent = token  #: the parent of a costume is the associated token.
        self._is_upscaled = True
        self._info_overlay = False
        self._is_rotatable = True
        self.image_actions_pipeline.append(("info_overlay", self.image_action_info_overlay, "info_overlay"))

    @property
    def info_overlay(self):
        return self._info_overlay

    @info_overlay.setter
    def info_overlay(self, value):
        """
        Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        self._info_overlay = value
        self.dirty = 1
        self.call_action("info_overlay")

    def set_costume(self, index):
        self._image_index = index

    def image_action_info_overlay(self, image: pygame.Surface, parent) -> pygame.Surface:
        pygame.draw.rect(image, (255, 0, 0, 100),
                         image.get_rect(), 4)
        # draw direction marker on image
        rect = parent.rect
        center = rect.centerx - parent.x, rect.centery - parent.y
        x = center[0] + math.sin(math.radians(parent.direction)) * rect.width / 2
        y = center[1] - math.cos(math.radians(parent.direction)) * rect.width / 2
        start_pos, end_pos = (center[0], center[1]), (x, y)
        pygame.draw.line(image, (255, 0, 0, 100), start_pos, end_pos, 3)
        return image

    async def update(self):
        if self.parent.board and self.is_animated:
            if self.parent.board.frame % self.animation_speed == 0:
                self.next_image()
                self.reload_image()
            else:
                self.reload_image()
        else:
            self.reload_image()