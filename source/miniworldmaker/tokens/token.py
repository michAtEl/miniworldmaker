import math
from logging import *
from typing import Union
import pygame
from boards import board_position
from tokens import costume


class Token(pygame.sprite.DirtySprite):

    token_count = 0
    log = getLogger("Token")
    lookup = True

    def __init__(self):
        super().__init__()
        self.costume = None
        # private
        self._size = (0, 0)  # Tuple with size
        self._position: board_position = None
        self._on_board = False
        self._is_at_border = False
        self._at_borders_list = False
        self._is_flipped = False
        Token.token_count += 1
        # public
        self.token_id = Token.token_count + 1
        self.is_static = True
        self.direction = 0
        self._orientation = 0
        self.board = None
        # costume
        self.costume = costume.Costume(self)
        self._image = self.costume.image
        self.costumes = [self.costume]
        self.init = 1

    @property
    def is_flipped(self):
        return self._is_flipped

    @is_flipped.setter
    def is_flipped(self, value):
        self.is_flipped = value
        self.costume.changed.add("flipped")

    @property
    def orientation(self):
        return self._orientation

    @orientation.setter
    def orientation(self, value):
        self._orientation = value
        self.dirty = 1
        self.costume.changed.add("orientation")

    def __str__(self):
        if self.board:
            return "Klasse: {0}; ID: {1}, Position: {2}".format(self.class_name, self.token_id, self.rect)
        else:
            return "Klasse: {0}; ID: {1}".format(self.class_name, self.token_id)

    @property
    def image(self) -> pygame.Surface:
        if not self.dirty:
            return self._image
        else:
            self._image = self.costume.image
            return self.costume.image

    @property
    def rect(self):
        if self.dirty == 1:
            self._rect = self.position.to_rect(rect=self.image.get_rect())
            self.dirty = 0
            return self._rect
        else:
            return self._rect

    def add_image(self, path: str) -> int:
        return self.costume.add_image(path)

    def add_costume(self, path: str) -> int:
        new_costume = costume.Costume(self)
        new_costume.add_image(path)
        self.costumes.append(new_costume)
        return len(self.costumes) - 1

    def switch_costume(self):
        index = self.costumes.index(self.costume)
        if index < len(self.costumes) - 1:
            index += 1
        else:
            index = 0
        self.costume = self.costumes[index]
        return self.costume

    def add_to_board(self, board, position):
        self.board = board
        self.costume.changed.add("direction")
        self.costume.changed.add("flipped")
        self.dirty = 1
        if self.init != 1:
            raise UnboundLocalError("Init was not called")

    @property
    def direction(self) -> int:
        """ Sets direction the token is oriented

            0°:  East, x degrees clock-wise otherwise
            You can also set the direction by String ("forward", "up", "down", ...
        """
        return self._direction

    @direction.setter
    def direction(self, value):
        direction = self._value_to_direction(value)
        self._direction = direction
        self.dirty = 1
        if self.costume:
            self.costume.changed.add("direction")

    @property
    def size(self):
        """Size of the token

        """
        return self._size

    @size.setter
    def size(self, value):
        self._size = value
        self.dirty = 1
        self.costume.changed.add("size")

    @property
    def position(self) -> tuple:
        """
        The position of the token is tuple (x, y)
        """
        return self._position

    @position.setter
    def position(self, value: Union[board_position.BoardPosition, tuple]):
        if type(value) == tuple:
            value = board_position.BoardPosition(value[0], value[1])
        self._position = value
        self.dirty = 1

    @property
    def class_name(self) -> str:
        return self.__class__.__name__

    # Methoden
    def act(self):
        """Custom acting

        This method is called every frame in the mainloop.
        Overwrite this method in your subclass

        """
        pass

    def update(self):
        if self.costume.is_animated:
            self.costume.update()

    def _value_to_direction(self, value) -> int:
        if value == "right":
            value = 0
        if value == "left":
            value = 180
        if value == "up":
            value = 90
        if value == "down":
            value = 270
        if value == "forward":
            value = self.direction
        if value == "back":
            value = 360 - self.direction
        value = value % 360
        return value

    def remove(self):
        """Removes this actor from board
        """
        if self.board:
            self.board.remove_from_board(self)
        self.kill()
        del (self)

    def is_colliding(self):
        return self.board.is_colliding(self)

    def get_colliding_tokens(self):
        return self.board.get_colliding_tokens(self)

    def is_colliding_with(self, class_name):
        colliding_tokens = self.board.get_colliding_tokens(self)
        from boards import board
        return board.Board.filter_actor_list(colliding_tokens, class_name)

    def is_at_border(self):
        return self.board.borders(self.rect)

    def is_on_the_board(self):
        return self.board.is_on_board(self.rect)

    def get_event(self, event, data):
        pass

    @classmethod
    def register_subclasses(base):
        d = {}
        for cls in base.__subclasses__():
            d[cls.__name__] = cls
        print(d)
        return d