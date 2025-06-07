import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Rectangle, Color, Line
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30

TETROMINOS = {
    'I': [[1, 1, 1, 1]],
    'O': [[1, 1], [1, 1]],
    'T': [[0, 1, 0], [1, 1, 1]],
    'L': [[1, 0], [1, 0], [1, 1]],
    'J': [[0, 1], [0, 1], [1, 1]],
    'S': [[0, 1, 1], [1, 1, 0]],
    'Z': [[1, 1, 0], [0, 1, 1]]
}

def rotate_piece(piece, direction):
    # ミノの回転（右：clockwise、左：counterclockwise）
    if direction == "right":
        return [list(row) for row in zip(*piece[::-1])]
    elif direction == "left":
        return [list(row) for row in zip(*piece)][::-1]
    return piece

class TetrisGame(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.spawn_new_piece()
        Clock.schedule_interval(self.update, 1)

    def spawn_new_piece(self):
        self.piece_type = random.choice(list(TETROMINOS.keys()))
        self.piece = TETROMINOS[self.piece_type]
        self.piece_x = GRID_WIDTH // 2 - len(self.piece[0]) // 2
        self.piece_y = 0

    def update(self, dt):
        if not self.check_collision(self.piece_x, self.piece_y + 1):
            self.piece_y += 1
        else:
            self.lock_piece()
            self.spawn_new_piece()
        self.draw()

    def check_collision(self, x, y, piece=None):
        if piece is None:
            piece = self.piece
        for row_idx, row in enumerate(piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = x + col_idx
                    grid_y = y + row_idx
                    if grid_x < 0 or grid_x >= GRID_WIDTH or grid_y >= GRID_HEIGHT:
                        return True
                    if grid_y >= 0 and self.grid[grid_y][grid_x]:
                        return True
        return False

    def lock_piece(self):
        for row_idx, row in enumerate(self.piece):
            for col_idx, cell in enumerate(row):
                if cell:
                    grid_x = self.piece_x + col_idx
                    grid_y = self.piece_y + row_idx
                    if 0 <= grid_y < GRID_HEIGHT and 0 <= grid_x < GRID_WIDTH:
                        self.grid[grid_y][grid_x] = 1

    def rotate_current_piece(self, direction):
        rotated = rotate_piece(self.piece, direction)
        # 衝突していなければ回転を適用
        if not self.check_collision(self.piece_x, self.piece_y, rotated):
            self.piece = rotated
            self.draw()

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            # 背景グリッド線を先に描く
            Color(0.6, 0.6, 0.6)
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    pos_x = x * BLOCK_SIZE
                    pos_y = (GRID_HEIGHT - y - 1) * BLOCK_SIZE
                    Line(rectangle=(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE), width=1)
            
            # 固定されたブロックの描画
            for y in range(GRID_HEIGHT):
                for x in range(GRID_WIDTH):
                    if self.grid[y][x]:
                        Color(0.3, 0.3, 0.3)  # ブロックの塗りつぶし色
                        pos_x = x * BLOCK_SIZE
                        pos_y = (GRID_HEIGHT - y - 1) * BLOCK_SIZE
                        Rectangle(pos=(pos_x, pos_y), size=(BLOCK_SIZE, BLOCK_SIZE))

                        # 枠線を描画（黒色）
                        Color(0, 0, 0)
                        Line(rectangle=(pos_x, pos_y, BLOCK_SIZE, BLOCK_SIZE), width=1)

            
            # 落下中のミノの描画
            for row_idx, row in enumerate(self.piece):
                for col_idx, cell in enumerate(row):
                    if cell:
                        Color(1, 0, 0)  # ミノの色（赤）
                        x = (self.piece_x + col_idx) * BLOCK_SIZE
                        y = (GRID_HEIGHT - (self.piece_y + row_idx) - 1) * BLOCK_SIZE
                        Rectangle(pos=(x, y), size=(BLOCK_SIZE, BLOCK_SIZE))

                        # 枠線を描画（黒色）
                        Color(0, 0, 0)
                        Line(rectangle=(x, y, BLOCK_SIZE, BLOCK_SIZE), width=1)  

    def move_piece(self, dx):
        new_x = self.piece_x + dx
        if not self.check_collision(new_x, self.piece_y, self.piece):
            self.piece_x = new_x
            self.draw()


class TetrisRoot(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        # ゲームエリア
        self.game = TetrisGame()
        self.add_widget(self.game)

        # ボタンパネル
        button_panel = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
        
        # 回転ボタン
        btn_left = Button(text='rotate-left')
        btn_right = Button(text='rotate-right')
        btn_left.bind(on_press=lambda instance: self.game.rotate_current_piece("left"))
        btn_right.bind(on_press=lambda instance: self.game.rotate_current_piece("right"))
        
        # 左右移動ボタン
        btn_move_left = Button(text='move-Left')
        btn_move_right = Button(text='move-Right')
        btn_move_left.bind(on_press=lambda instance: self.game.move_piece(-1))
        btn_move_right.bind(on_press=lambda instance: self.game.move_piece(1))
        
        # ボタンをパネルに追加
        button_panel.add_widget(btn_left)
        button_panel.add_widget(btn_right)
        button_panel.add_widget(btn_move_left)
        button_panel.add_widget(btn_move_right)

        self.add_widget(button_panel)

class TetrisApp(App):
    def build(self):
        return TetrisRoot()

if __name__ == '__main__':
    TetrisApp().run()
