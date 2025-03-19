from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Rectangle, Ellipse, Color
from kivy.clock import Clock
from kivy.core.window import Window
import random

class Block(Widget):
    """ブロック"""
    def __init__(self, x, y, **kwargs):
        super().__init__(**kwargs)
        self.size = (60, 20)
        self.pos = (x, y)
        with self.canvas:
            Color(1, random.random(), random.random(), 1)  # ランダムな色
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def destroy(self):
        self.canvas.clear()
        self.parent.remove_widget(self)

class Ball(Widget):
    """ボール"""
    def __init__(self, paddle, **kwargs):
        super().__init__(**kwargs)
        self.size = (20, 20)
        self.paddle = paddle
        self.reset_position()
        with self.canvas:
            Color(1, 1, 1, 1)
            self.ellipse = Ellipse(pos=self.pos, size=self.size)

    def reset_position(self):
        """ボールの位置をパドルの上にリセット"""
        self.pos = (self.paddle.center_x - self.width / 2, self.paddle.top + 10)
        self.velocity = [random.choice([-4, 4]), 4]  # 上向きに発射

    def move(self):
        """ボールの移動処理"""
        self.x += self.velocity[0]
        self.y += self.velocity[1]
        self.ellipse.pos = self.pos

        # 壁との衝突判定
        if self.x <= 0 or self.right >= Window.width:
            self.velocity[0] *= -1
        if self.top >= Window.height:
            self.velocity[1] *= -1

class Paddle(Widget):
    """パドル"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size = (100, 20)
        self.pos = (Window.width / 2 - self.width / 2, 50)
        with self.canvas:
            Color(0, 1, 0, 1)
            self.rect = Rectangle(pos=self.pos, size=self.size)

    def move(self, touch_x):
        """タッチまたはマウス操作で移動"""
        self.x = max(0, min(touch_x - self.width / 2, Window.width - self.width))
        self.rect.pos = self.pos

class BrickBreakerGame(Widget):
    """ゲーム全体の管理"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.paddle = Paddle()
        self.ball = Ball(self.paddle)
        self.blocks = []
        self.add_widget(self.paddle)
        self.add_widget(self.ball)
        self.running = True  # ゲームが動作中かどうか

        self.create_blocks()
        Clock.schedule_interval(self.update, 1 / 60)
        Window.bind(on_key_down=self.on_key_down)  # キーボード入力を監視

    def create_blocks(self):
        """ブロックを配置する"""
        for row in range(5):
            for col in range(8):
                block = Block(80 * col + 30, Window.height - 100 - 25 * row)
                self.blocks.append(block)
                self.add_widget(block)

    def update(self, dt):
        """ゲームループ"""
        if not self.running:
            return

        self.ball.move()

        # パドルとの衝突判定
        if self.ball.collide_widget(self.paddle):
            self.ball.velocity[1] *= -1

        # ブロックとの衝突判定
        for block in self.blocks[:]:
            if self.ball.collide_widget(block):
                self.blocks.remove(block)
                block.destroy()
                self.ball.velocity[1] *= -1
                break

        # ゲームオーバー判定
        if self.ball.y <= 0:
            self.game_over()

    def game_over(self):
        """ゲームオーバー処理"""
        self.running = False
        self.add_widget(Label(text="Game Over\nPress SPACE to Restart", font_size=40, center=(Window.width / 2, Window.height / 2)))

    def restart_game(self):
        """ゲームを再スタート"""
        self.clear_widgets()
        self.blocks = []
        self.add_widget(self.paddle)
        self.add_widget(self.ball)

        self.create_blocks()
        self.ball.reset_position()
        self.running = True

    def on_touch_move(self, touch):
        """パドルの操作"""
        if self.running:
            self.paddle.move(touch.x)

    def on_key_down(self, window, keycode, scancode, text, modifiers):
        """スペースキーでリスタート"""
        if keycode == 32:  # スペースキー
            self.restart_game()

class BrickBreakerApp(App):
    def build(self):
        return BrickBreakerGame()

if __name__ == '__main__':
    BrickBreakerApp().run()

