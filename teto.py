import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color

# ゲームフィールドのサイズ（横10マス、縦20マス）
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30  # ブロック1個のサイズ（ピクセル）

# テトリミノの形（1がブロック、0が空白）
TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'L': [[1, 0], [1, 0], [1, 1]],
    'J': [[0, 1], [0, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # フィールドの初期化（0=空きマス）
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

        # 最初のミノを出現させる
        self.spawn_new_piece()

        # 一定間隔（0.5秒）でupdate()を呼び出す
        Clock.schedule_interval(self.update, 0.5)

    def spawn_new_piece(self):
        # ランダムにミノの種類を選ぶ
        self.piece_type = random.choice(list(TETROMINOS.keys()))
        self.piece = TETROMINOS[self.piece_type]

        # ミノの出現位置（中央上）
        self.piece_x = GRID_WIDTH // 2 - len(self.piece[0]) // 2
        self.piece_y = 0

    def update(self, dt):
        # 下にブロックが無ければ下に移動
        if not self.check_collision(self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            # 下にぶつかっていたらその場に固定
            self.lock_piece()

            # 次のミノを出す
            self.spawn_new_piece()

        # 描画更新
        self.draw()

    def check_collision(self, x, y):
        # ミノのすべてのセルをチェック
        for row_idx, row in enumerate(self.piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = x + col_idx
                    grid_y = y + row_idx

                    # フィールド外（地面や壁）に出ていれば衝突
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return True

                    # フィールド内のブロックと衝突
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        return False

    def lock_piece(self):
        # ミノのブロックをフィールド（self.grid）に記録
        for row_idx, row in enumerate(self.piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_x + col_idx
                    grid_y = self.piece_y + row_idx

                    # フィールドの範囲内なら記録
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = 1

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # 固定されたブロックの描画（灰色）
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.grid[y][x]:
                        Color(0.3, 0.3, 0.3)  # グレー
                        Rectangle(pos=(x * BLOCK_SIZE, (GRID_HEIGHT - y - 1) * BLOCK_SIZE),
                                  size=(BLOCK_SIZE, BLOCK_SIZE))

            # 現在のミノの描画（赤）
            for row_idx, row in enumerate(self.piece):
                for col_idx, cell in enumerate(row):
                    if cell:
                        Color(1, 0, 0)  # 赤色
                        x = (self.piece_x + col_idx) * BLOCK_SIZE
                        y = (GRID_HEIGHT - (self.piece_y + row_idx) - 1) * BLOCK_SIZE
                        Rectangle(pos=(x, y), size=(BLOCK_SIZE, BLOCK_SIZE))

# Kivyアプリとして起動
class TetrisApp(App):
    def build(self):
        return TetrisGame()

if __name__ == '__main__':
    TetrisApp().run()

