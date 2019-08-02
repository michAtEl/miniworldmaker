from miniworldmaker.windows import miniworldwindow
class Timed():
    def __init__(self):
        self.board = miniworldwindow.MiniWorldWindow.board
        self.board.timed_objects.append(self)

    def tick(self):
        self.time = self.time - 1

    def unregister(self):
        self.board.timed_objects.remove(self)
        del(self)


class ZeroTimer(Timed):
    def __init__(self, time):
        super().__init__()
        self.time = time

    def tick(self):
        self.time -= 1
        if self.time == 0:
            self.action()
            self.unregister()

    def action(self):
        pass


class Timer(Timed):
    def __init__(self, time):
        super().__init__()
        self.time = time
        self.actual_time = 0

    def tick(self):
        self.actual_time += 1
        if self.actual_time % self.time == 0:
            self.action()

    def action(self):
        pass