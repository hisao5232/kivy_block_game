from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.graphics import Line
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.core.audio import SoundLoader
import random
import traceback

class GameBoard(Widget):  # ゲームボードを表すクラス。KivyのWidgetを継承している。
    def __init__(self, parent_ui=None, **kwargs):
        super().__init__(**kwargs)  # 親クラス（Widget）の初期化を呼び出す
        self.parent_ui = parent_ui  # 明示的にTetrisUIを受け取る
        self.cols = 10  # 横方向のマスの数（テトリスなどでは通常10列）
        self.rows = 20  # 縦方向のマスの数（テトリスの標準的な高さ）
        self.cell_size = 0  # 各マスの大きさ（あとで計算される予定）
        # ゲームボードのデータを2次元リストで表現（0 = 空、1など = ブロック）
        self.board = [[0]*self.cols for _ in range(self.rows)]
        # 現在落下中のブロック（ピース）をランダムに取得
        self.current_piece = self.get_random_piece()
        self._clock_event = None
        self.update_event = None  # 後でキャンセルできるように
        self.is_game_over = False
        # 万一 __init__ 前にスケジュールされていたらキャンセルする
        Clock.unschedule(self.update)
        # ウィジェットのサイズまたは位置が変わったときに on_size を呼び出す
        self.bind(size=self.on_size, pos=self.on_size)
        self.score = 0
        self.bgm = parent_ui.bgm  # ← 親のBGMを受け取る
        if self.bgm:
            self.bgm.loop = True  # ループ再生を有効にする
            
    def start(self):
        print("▶️ start called")
        if self.update_event:
            self.update_event.cancel()
        self.schedule_update()
        if self.bgm:
            self.bgm.play()  # ゲーム開始時にBGM再生
        self.schedule_update()  # ← これを必ず追加

    def stop(self):
        print("⏹ stop called")
        if self.bgm:
            self.bgm.stop()
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
            print("🛑 Clock cancelled")

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
            self.game_over()

    def clear_lines(self):
        new_board = [row for row in self.board if any(cell == 0 for cell in row)]
        lines_cleared = self.rows - len(new_board)

        if lines_cleared > 0:
            # 落下処理の一時停止
            if self.update_event:
                print(f"[clear_lines] Canceling update_event id={id(self.update_event)}")
                self.update_event.cancel()
                self.update_event = None

            # 効果音再生
            if self.parent_ui and self.parent_ui.line_clear_se:
                self.parent_ui.line_clear_se.play()

            # 0.5秒後に再開
            Clock.schedule_once(self.resume_game, 0.5)

            # スコア更新（先にしておく）
            self.score += lines_cleared
            if self.parent_ui:
                self.parent_ui.update_score(self.score)

        # 再構築
        for _ in range(lines_cleared):
            new_board.insert(0, [0 for _ in range(self.cols)])
        self.board = new_board

    def update(self, dt):
        print(f"⚠️ update called before start() (dt={dt})")
        traceback.print_stack(limit=10)
        if self.is_game_over:
            print("⛔ update stopped: game over")
            return

        x, y = self.current_piece['position']
        
        # 下に動かせるなら1マス落とす
        if self.can_move(0, 1):
            self.current_piece['position'] = (x, y + 1)
        else:
            # 動かせないので固定する
            self.lock_piece()

            # 💡 lock後にゲームオーバーを判定
            if self.detect_game_over():
                self.game_over()  # ここで止めて親に通知

        # 毎フレーム描画更新
        self.draw()

    def detect_game_over(self):
        # 最上段にブロックが積もったかを判定
        return any(cell != 0 for cell in self.board[0])

    def game_over(self):
        print("Game Over")
        self.is_game_over = True
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None
        self.stop()
        if self.parent_ui and hasattr(self.parent_ui, 'show_game_over'):
            print("Calling parent's show_game_over()")
            self.parent_ui.show_game_over()
        else:
            print("⚠️ No show_game_over method in parent_ui")
            print(self.parent)

    def hard_drop(self): 
        while self.can_move(0, 1):
            x, y = self.current_piece['position']
            self.current_piece['position'] = (x, y + 1)
        self.lock_piece()
        self.draw()

    def reset(self):
        print("🧹 Resetting GameBoard...")

        # ボードをクリア
        self.board = [[0]*self.cols for _ in range(self.rows)]

        # 落下中のブロックを新しくする
        self.current_piece = self.get_random_piece()

        # フラグを初期化
        self.is_game_over = False

        # 既存の描画をすべて削除（必要なら）
        self.clear_widgets()

        # タイマーをリセット
        self._clock_event = None
        self.score = 0

    def resume_game(self, dt):
        self.schedule_update()  # 落下処理を再開

    def schedule_update(self):
        if self.update_event is not None:
            print("[schedule_update] Already scheduled, skipping.")
            return
        print("[schedule_update] Scheduling new update event.")
        traceback.print_stack(limit=5)  # ← どこから呼ばれたか表示
        self.update_event = Clock.schedule_interval(self.update, 0.5)
        print(f"[schedule_update] Scheduled update_event id={id(self.update_event)}")

    def stop_update(self):
        if self.update_event:
            self.update_event.cancel()
            self.update_event = None

class TetrisUI(FloatLayout):  # Tetrisアプリ全体のUIを構成するクラス。BoxLayoutを継承。
    def __init__(self, screen_manager=None, **kwargs):
        super().__init__(**kwargs)
        self.screen_manager = screen_manager
        self._clock_event = None

        # ゲームボード作成前にBGMを読み込む
        self.bgm = SoundLoader.load('assets\game_bgm.ogg')
        if self.bgm:
            self.bgm.loop = True
        else:
            print("⚠️ BGMファイルが読み込めませんでした")
        # 効果音ロード（ファイルがある場所を確認）
        self.line_clear_se = SoundLoader.load('assets/line_clear.wav')

        main_layout = BoxLayout(orientation='horizontal', size_hint=(1, 1))

        self.game_board = GameBoard(parent_ui=self)

        # 左コントロール
        left_controls = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
        left_move_btn = Button(text='L Move')
        left_rotate_btn = Button(text='L Rotate')
        # スコア表示用ラベル
        self.score_label = Label(text='Score: 0', font_size='20sp', size_hint=(1, 0.2),
                         halign='center', valign='middle')
        self.score_label.bind(size=self.score_label.setter('text_size'))  # テキストを中央に揃える
        left_move_btn.bind(on_press=lambda instance: self.game_board.move_piece(-1))
        left_rotate_btn.bind(on_press=lambda instance: self.game_board.rotate_piece(left=True))
        left_controls.add_widget(left_move_btn)
        left_controls.add_widget(left_rotate_btn)
        left_controls.add_widget(Widget())  # 空白で真ん中調整
        left_controls.add_widget(self.score_label)

        # 中央ゲームエリア
        center_area = BoxLayout(size_hint=(0.6, 1))
        center_area.add_widget(self.game_board)
        self.game_board.size_hint = (1, 1)

        # 右コントロール
        right_controls = BoxLayout(orientation='vertical', size_hint=(0.2, 1))
        right_move_btn = Button(text='R Move')
        right_rotate_btn = Button(text='R Rotate')
        hard_drop_btn = Button(text='Hard Drop')
        right_move_btn.bind(on_press=lambda instance: self.game_board.move_piece(1))
        right_rotate_btn.bind(on_press=lambda instance: self.game_board.rotate_piece(left=False))
        hard_drop_btn.bind(on_press=lambda instance: self.game_board.hard_drop())
        right_controls.add_widget(right_move_btn)
        right_controls.add_widget(right_rotate_btn)
        right_controls.add_widget(hard_drop_btn)

        main_layout.add_widget(left_controls)
        main_layout.add_widget(center_area)
        main_layout.add_widget(right_controls)

        self.add_widget(main_layout)

        # オーバーレイは最前面に表示
        self.overlay = FloatLayout()
        self.overlay_label = Label(text='GAME OVER', font_size='40sp',
                                   size_hint=(None, None), size=(400, 100),
                                   pos_hint={'center_x': 0.5, 'center_y': 0.7})
        continue_btn = Button(text='Continue', size_hint=(0.3, 0.1),
                              pos_hint={'center_x': 0.5, 'center_y': 0.5})
        title_btn = Button(text='Back to Title', size_hint=(0.3, 0.1),
                           pos_hint={'center_x': 0.5, 'center_y': 0.35})
        continue_btn.bind(on_press=self.continue_game)
        title_btn.bind(on_press=self.back_to_title)
        self.overlay.add_widget(self.overlay_label)
        self.overlay.add_widget(continue_btn)
        self.overlay.add_widget(title_btn)
        self.overlay.opacity = 0
        self.add_widget(self.overlay)

    def show_game_over(self):
        self.overlay.opacity = 1  # ゲームオーバー表示

    def continue_game(self, instance):
        self.overlay.opacity = 0
        self.game_board.reset()  # GameBoardにresetメソッドを用意してリセット
        self.cancel_update()     # ← これを追加
        self.schedule_update()   # ← これを追加
        self.update_score(0)  # スコアをリセット
        self.game_board.start()

    def back_to_title(self, instance):
        self.cancel_update()
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None
        if self.game_board.bgm:
            self.game_board.bgm.stop()
        if self.screen_manager:
            self.screen_manager.current = 'title'

    def schedule_update(self):
        if not self._clock_event:
            self._clock_event = Clock.schedule_interval(self.update, 0.5)

    def update(self, dt):
        self.game_board.update(dt)  # GameBoardのupdateを呼ぶ

    def cancel_update(self):
        if self._clock_event:
            self._clock_event.cancel()
            self._clock_event = None

    def update_score(self, new_score):
        self.score_label.text = f"Score: {new_score}"

class TetrisApp(App):
    def build(self):
        sm = MyScreenManager()  # 独自のScreenManagerで画面遷移を管理
        sm.add_widget(TitleScreen(name='title'))  # 最初の画面を追加
        sm.add_widget(GameScreen(name='game'))  # ← ゲーム画面も追加
        sm.current = 'title'  # 初期表示を設定
        return sm

# ゲーム画面
class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        print("🟠 GameScreen.__init__ called")
        self.tetris_ui = TetrisUI()  # 一旦 screen_manager なしで初期化
        self.add_widget(self.tetris_ui)
        self.bgm = None  # ← BGMを保持する変数

    def on_enter(self):
        print("🔶 GameScreen.on_enter called")
        print("🔷 calling game_board.start() in on_enter")
        # 画面遷移時に screen_manager を改めて設定（managerが使えるようになる）
        self.tetris_ui.screen_manager = self.manager  # 遷移後に設定
        if self.tetris_ui and self.tetris_ui.game_board:
            print("🔷 calling game_board.start() in on_enter")
            self.tetris_ui.game_board.start()

# タイトル画面
class TitleScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        # タイトルラベル
        title_label = Label(text="TETRIS", font_size=48, size_hint=(1, 0.8))

        # スタートボタン
        start_button = Button(text='Start Game', size_hint=(1, 0.2))
        start_button.bind(on_press=self.start_game)

        layout.add_widget(title_label)
        layout.add_widget(start_button)

        self.add_widget(layout)

    def start_game(self, *args):  # Buttonから呼ばれるときに引数が来るため
        print("🟡 TitleScreen.start_game() called")
        self.manager.start_game()  # 親のScreenManagerに処理を任せる

# 画面遷移を管理
class TetrisRoot(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TitleScreen(name='title'))  # スクリーン名は 'title'
        self.current = 'title'
        
    def start_game(self):
        print("🟢 TetrisRoot.start_game() called")
        if not self.has_screen('game'):
            self.add_widget(GameScreen(name='game'))
        self.current = 'game'

        # GameScreen 内の game_board を start
        game_screen = self.get_screen('game')
        print(f"🔵 game_screen: {game_screen}")
        print(f"🔵 tetris_ui: {getattr(game_screen, 'tetris_ui', None)}")
        print(f"🔵 game_board: {getattr(getattr(game_screen, 'tetris_ui', None), 'game_board', None)}")
        game_screen.tetris_ui.game_board.start()

class MyScreenManager(ScreenManager):
    def start_game(self):
        if self.has_screen('game'):
            self.remove_widget(self.get_screen('game'))

        game_screen = GameScreen(name='game')
        self.add_widget(game_screen)
        self.current = 'game'

if __name__ == '__main__':
    TetrisApp().run()