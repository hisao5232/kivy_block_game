from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.graphics import Line
from kivy.clock import Clock
import random

class GameBoard(Widget):  # ゲームボードを表すクラス。KivyのWidgetを継承している。
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 親クラス（Widget）の初期化を呼び出す

        self.cols = 10  # 横方向のマスの数（テトリスなどでは通常10列）
        self.rows = 20  # 縦方向のマスの数（テトリスの標準的な高さ）
        self.cell_size = 0  # 各マスの大きさ（あとで計算される予定）

        # ゲームボードのデータを2次元リストで表現（0 = 空、1など = ブロック）
        self.board = [[0]*self.cols for _ in range(self.rows)]

        # 現在落下中のブロック（ピース）をランダムに取得
        self.current_piece = self.get_random_piece()

        # 0.5秒ごとに update() メソッドを呼び出す（定期的な更新処理）
        Clock.schedule_interval(self.update, 0.5)

        # ウィジェットのサイズまたは位置が変わったときに on_size を呼び出す
        self.bind(size=self.on_size, pos=self.on_size)

    def on_size(self, *args):
        self.cell_size = min(self.width / self.cols, self.height / self.rows)
        self.draw()

    def get_random_piece(self):
        pieces = [
            {
                'name': 'I',
                'rotations': [
                    [
                        [0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                    ],
                    [
                        [0, 0, 1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 1, 0],
                        [0, 0, 1, 0],
                    ],
                    [
                        [0, 0, 0, 0],
                        [0, 0, 0, 0],
                        [1, 1, 1, 1],
                        [0, 0, 0, 0],
                    ],
                    [
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                        [0, 1, 0, 0],
                    ],
                ],
            },
            {
                'name': 'O',
                'rotations': [
                    [
                        [1, 1],
                        [1, 1],
                    ],
                ] * 4,
            },
            {
                'name': 'T',
                'rotations': [
                    [
                        [0, 1, 0],
                        [1, 1, 1],
                    ],
                    [
                        [1, 0],
                        [1, 1],
                        [1, 0],
                    ],
                    [
                        [1, 1, 1],
                        [0, 1, 0],
                    ],
                    [
                        [0, 1],
                        [1, 1],
                        [0, 1],
                    ],
                ],
            },
            {
                'name': 'S',
                'rotations': [
                    [
                        [0, 1, 1],
                        [1, 1, 0],
                    ],
                    [
                        [1, 0],
                        [1, 1],
                        [0, 1],
                    ],
                    [
                        [0, 1, 1],
                        [1, 1, 0],
                    ],
                    [
                        [1, 0],
                        [1, 1],
                        [0, 1],
                    ],
                ],
            },
            {
                'name': 'Z',
                'rotations': [
                    [
                        [1, 1, 0],
                        [0, 1, 1],
                    ],
                    [
                        [0, 1],
                        [1, 1],
                        [1, 0],
                    ],
                    [
                        [1, 1, 0],
                        [0, 1, 1],
                    ],
                    [
                        [0, 1],
                        [1, 1],
                        [1, 0],
                    ],
                ],
            },
            {
                'name': 'J',
                'rotations': [
                    [
                        [1, 0, 0],
                        [1, 1, 1],
                    ],
                    [
                        [1, 1],
                        [1, 0],
                        [1, 0],
                    ],
                    [
                        [1, 1, 1],
                        [0, 0, 1],
                    ],
                    [
                        [0, 1],
                        [0, 1],
                        [1, 1],
                    ],
                ],
            },
            {
                'name': 'L',
                'rotations': [
                    [
                        [0, 0, 1],
                        [1, 1, 1],
                    ],
                    [
                        [1, 0],
                        [1, 0],
                        [1, 1],
                    ],
                    [
                        [1, 1, 1],
                        [1, 0, 0],
                    ],
                    [
                        [1, 1],
                        [0, 1],
                        [0, 1],
                    ],
                ],
            },
        ]

        piece = random.choice(pieces)
        piece['rotation'] = 0
        piece['shape'] = piece['rotations'][0]

        # 初期位置（X：中央に、Y：最上段）
        piece_width = len(piece['shape'][0])
        piece['position'] = (self.cols // 2 - piece_width // 2, 0)
        return piece

    def draw(self):
        self.canvas.clear()
        with self.canvas:
            Color(1, 1, 1)
            self.cell_size = min(self.width / self.cols, self.height / self.rows)

            # 中央に配置するためのオフセットを計算
            board_width = self.cell_size * self.cols
            board_height = self.cell_size * self.rows
            x0 = self.x + (self.width - board_width) / 2
            y0 = self.y + (self.height - board_height) / 2

            # グリッドの描画
            Color(0.3, 0.3, 0.3)
            for i in range(self.cols + 1):
                Line(points=[x0 + i * self.cell_size, y0, x0 + i * self.cell_size, y0 + board_height])
            for j in range(self.rows + 1):
                Line(points=[x0, y0 + j * self.cell_size, x0 + board_width, y0 + j * self.cell_size])

            # 固定されたブロック
            for y in range(self.rows):
                for x in range(self.cols):
                    if self.board[y][x]:
                        Color(0.6, 0.6, 0.9)
                        Rectangle(pos=(x0 + x * self.cell_size, y0 + (self.rows - y - 1) * self.cell_size),
                                size=(self.cell_size, self.cell_size))

            # 現在のミノ
            piece = self.current_piece
            shape = piece['rotations'][piece['rotation']]
            Color(0.8, 0.4, 0.4)
            px_base, py_base = piece['position']  # ここで展開
            for dy, row in enumerate(shape):
                for dx, cell in enumerate(row):
                    if cell:
                        px = x0 + (px_base + dx) * self.cell_size
                        py = y0 + (self.rows - (py_base + dy) - 1) * self.cell_size
                        Rectangle(pos=(px, py), size=(self.cell_size, self.cell_size))

    def check_collision(self, x, y, shape):
        for sy, row in enumerate(shape):
            for sx, cell in enumerate(row):
                if cell:
                    new_x = x + sx
                    new_y = y + sy
                    if (new_x < 0 or new_x >= self.cols or
                        new_y >= self.rows or
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return True
        return False

    def move_piece(self, dx):
        x, y = self.current_piece['position']  # 位置を取得
        if self.can_move(dx, 0):
            self.current_piece['position'] = (x + dx, y)  # 更新
            self.draw()

    def rotate_piece(self, left=False):
        piece = self.current_piece
        old_rotation = piece['rotation']
        num_rotations = len(piece['rotations'])
        x, y = piece['position']

        # 回転インデックス更新
        if left:
            new_rotation = (old_rotation - 1) % num_rotations
        else:
            new_rotation = (old_rotation + 1) % num_rotations

        # 新しい形状を仮に適用
        piece['rotation'] = new_rotation
        piece['shape'] = piece['rotations'][new_rotation]

        # ミノの種類による回転補正（SRS風）
        if piece.get('name') == 'I':
            offsets = [(0, 0), (-1, 0), (1, 0), (0, -1), (0, 1)]
        else:
            offsets = [(0, 0)]

        placed = False
        for dx, dy in offsets:
            piece['position'] = (x + dx, y + dy)
            if self.can_move(0, 0):  # この位置に置けるか
                placed = True
                break

        # すべて失敗 → 回転を元に戻す
        if not placed:
            piece['rotation'] = old_rotation
            piece['shape'] = piece['rotations'][old_rotation]
            piece['position'] = (x, y)

    def can_move(self, dx, dy, rotation_offset=0):
        piece = self.current_piece
        new_rotation = (piece['rotation'] + rotation_offset) % len(piece['rotations'])
        shape = piece['rotations'][new_rotation]

        px, py = piece['position']  # ← ここで位置を取得

        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = px + x + dx
                    new_y = py + y + dy
                    if (new_x < 0 or new_x >= self.cols or
                        new_y >= self.rows or
                        (new_y >= 0 and self.board[new_y][new_x])):
                        return False
        return True

    def move_left(self):
        if self.can_move(-1, 0):
            self.current_piece['x'] -= 1
            self.draw()

    def move_right(self):
        if self.can_move(1, 0):
            self.current_piece['x'] += 1
            self.draw()

    def rotate_right(self):
        if self.can_move(0, 0, 1):
            self.current_piece['rotation'] = (self.current_piece['rotation'] + 1) % 4
            self.draw()

    def rotate_left(self):
        if self.can_move(0, 0, -1):
            self.current_piece['rotation'] = (self.current_piece['rotation'] - 1) % 4
            self.draw()  

    def lock_piece(self):
        x, y = self.current_piece['position']
        shape = self.current_piece['rotations'][self.current_piece['rotation']]

        # 現在のピースをボードに固定
        for dy, row in enumerate(shape):
            for dx, cell in enumerate(row):
                if cell:
                    bx = x + dx
                    by = y + dy
                    if 0 <= by < self.rows and 0 <= bx < self.cols:
                        self.board[by][bx] = 1

        # ラインが揃っていれば消す
        self.clear_lines()

        # 新しいピースを出す
        self.current_piece = self.get_random_piece()

        # 新しいピースが置けなければゲームオーバー（optional）
        if not self.can_move(0, 0):
            print("Game Over")
            self.board = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = self.rows - len(new_board)
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.cols)])
        self.board = new_board

    def update(self, dt):
        x, y = self.current_piece['position']
        if self.can_move(0, 1):
            self.current_piece['position'] = (x, y + 1)
        else:
            self.lock_piece()
        self.draw()

    def hard_drop(self):
        while self.can_move(0, 1):
            x, y = self.current_piece['position']
            self.current_piece['position'] = (x, y + 1)
        self.lock_piece()
        self.draw()

class TetrisUI(BoxLayout):  # Tetrisアプリ全体のUIを構成するクラス。BoxLayoutを継承。
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # 親クラス(BoxLayout)の初期化

        self.orientation = 'horizontal'  # 水平方向にウィジェットを並べるレイアウトに設定

        self.game_board = GameBoard()  # 中央に表示されるゲームボード（前に定義したGameBoardクラスのインスタンス）

        # 左コントロールエリアの作成
        left_controls = BoxLayout(orientation='vertical', size_hint=(0.2, 1))  # 縦に並ぶボタン、画面幅の20%
        left_move_btn = Button(text='L Move')  # 左移動ボタン
        left_rotate_btn = Button(text='L Rotate')  # 左回転ボタン

        # ボタンが押されたときに対応するGameBoardのメソッドを呼び出す
        left_move_btn.bind(on_press=lambda instance: self.game_board.move_piece(-1))  # 左に1マス移動
        left_rotate_btn.bind(on_press=lambda instance: self.game_board.rotate_piece(left=True))  # 左回転

        # 左コントロールにボタンを追加
        left_controls.add_widget(left_move_btn)
        left_controls.add_widget(left_rotate_btn)

        # 中央ゲームエリアの設定（ゲーム画面部分）
        center_area = BoxLayout(size_hint=(0.6, 1))  # 幅の60%を占める
        center_area.add_widget(self.game_board)  # ゲームボードを中央エリアに追加
        self.game_board.size_hint = (1, 1)  # 明示的にサイズ比率を指定（エリアいっぱいに広がる）

        # 右コントロールエリアの作成
        right_controls = BoxLayout(orientation='vertical', size_hint=(0.2, 1))  # 縦並び、画面幅の20%
        right_move_btn = Button(text='R Move')  # 右移動ボタン
        right_rotate_btn = Button(text='R Rotate')  # 右回転ボタン
        hard_drop_btn = Button(text='Hard Drop')  # ハードドロップ（即座に落下させる）ボタン

        # 各ボタンに機能をバインド（イベント接続）
        right_move_btn.bind(on_press=lambda instance: self.game_board.move_piece(1))  # 右に1マス移動
        right_rotate_btn.bind(on_press=lambda instance: self.game_board.rotate_piece(left=False))  # 右回転
        hard_drop_btn.bind(on_press=lambda instance: self.game_board.hard_drop())  # 一気にブロックを落とす

        # 右コントロールにボタンを追加
        right_controls.add_widget(right_move_btn)
        right_controls.add_widget(right_rotate_btn)
        right_controls.add_widget(hard_drop_btn)

        # 全体のレイアウトに、左・中央・右の各エリアを順番に追加
        self.add_widget(left_controls)
        self.add_widget(center_area)
        self.add_widget(right_controls)


class TetrisApp(App):  # Kivyのアプリケーション全体を管理するクラス。Appを継承。
    def build(self):
        return TetrisUI()  # アプリのルートウィジェットとしてTetrisUI（画面のレイアウト）を返す

if __name__ == '__main__':
    TetrisApp().run()