from miniworldmaker import *


class MyBoard(TiledBoard):

    def __init__(self):
        super().__init__(tile_size=50, columns=10, rows=1, tile_margin=1)
        player1 = Player((0, 0))
        self.add_image("images/water.png")


class Player(Actor):

    def __init__(self, position):
        super().__init__(position)
        self.add_image(path="images/fish.png")
        self.costume.orientation = - 90
        self.direction = "right"

    def act(self):
        if self.sensing_on_board():
            self.move()
            print(self.position, self.position.is_on_board())
        else:
            self.flip_x()
            self.move()
            print(self.position, self.position.is_on_board())



board = MyBoard()
board.show()
