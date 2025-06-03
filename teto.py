import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.clock import Clock

CELL_SIZE = 30
COLUMNS = 10
ROWS = 20

# テトリミノの形状（各ブロックの座標）
TETROMINOES = {
    'I': [(0, 1), (1, 1), (2, 1), (3, 1)],
    'O': [(0, 0), (1, 0), (0, 1), (1, 1)],
    'T': [(1, 0), (0, 1), (1, 1), (2, 1)],
    'S': [(1, 0), (2, 0), (0, 1), (1, 1)],
    'Z': [(0, 0), (1, 0), (1, 1), (2, 1)],
    'J': [(0, 0), (0, 1), (1, 1), (2, 1)],
    'L': [(2, 0), (0, 1), (1, 1), (2, 1)],
}

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cell_size = CELL_SIZE
        self.current_piece = None
        self.piece_position = [3, 19]  # 初期位置
        Clock.schedule_interval(self.update, 0.5)
        self.spawn_piece()

    def spawn_piece(self):
        self.piece_type = random.choice(list(TETROMINOES.keys()))
        self.current_piece = TETROMINOES[self.piece_type]
        self.piece_position = [3, 19]  # 左下が(0,0)の座標系

    def update(self, dt):
        self.piece_position[1] -= 1  # 1マス下に移動
        if self.piece_position[1] < 0:
            self.spawn_piece()
        self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(0.2, 0.2, 0.2)
            for x in range(COLUMNS):
                for y in range(ROWS):
                    Rectangle(pos=(x * CELL_SIZE, y * CELL_SIZE), size=(CELL_SIZE - 1, CELL_SIZE - 1))
            Color(0, 1, 0)
            for block in self.current_piece:
                bx = self.piece_position[0] + block[0]
                by = self.piece_position[1] + block[1]
                if 0 <= bx < COLUMNS and 0 <= by < ROWS:
                    Rectangle(pos=(bx * CELL_SIZE, by * CELL_SIZE), size=(CELL_SIZE - 1, CELL_SIZE - 1))

class TetrisApp(App):
    def build(self):
        game = TetrisGame()
        game.size = (CELL_SIZE * COLUMNS, CELL_SIZE * ROWS)
        return game

if __name__ == '__main__':
    TetrisApp().run()
