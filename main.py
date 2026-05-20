from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.storage.jsonstore import JsonStore
from kivy.core.audio import SoundLoader
from random import randint
from kivy.config import Config

Config.set('graphics', 'resizable', False)

# WINDOW SETTINGS
Window.clearcolor = (0, 0, 0, 1)

# SAVE SYSTEM
store = JsonStore("save.json")


class Player(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        size = min(Window.width, Window.height)

        self.size = (size * 0.15, size * 0.15)

        self.pos = (
            Window.width / 2 - self.width / 2,
            100
        )

        with self.canvas:
            self.rect = Rectangle(
                source="assets/player.png",
                pos=self.pos,
                size=self.size
            )

    def update_graphics(self):
        self.rect.pos = self.pos


class Enemy(Widget):

    def __init__(self, speed=5, **kwargs):
        super().__init__(**kwargs)

        self.speed = speed

        size = min(Window.width, Window.height)

        self.size = (
            size * 0.12,
            size * 0.12
        )

        self.pos = (
            randint(0, int(Window.width - self.width)),
            Window.height
        )

        with self.canvas:
            self.rect = Rectangle(
                source="assets/enemy.png",
                pos=self.pos,
                size=self.size
            )

    def fall(self):
        self.y -= self.speed
        self.rect.pos = self.pos


class GameWidget(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.running = False

        # BACKGROUND
        with self.canvas.before:
            self.bg = Rectangle(
                source="assets/background.png",
                pos=(0, 0),
                size=Window.size
            )

        # SCORE
        self.score = 0

        # HIGH SCORE
        if store.exists("highscore"):
            self.highscore = store.get("highscore")["score"]
        else:
            self.highscore = 0

        # SOUNDS
        self.hit_sound = SoundLoader.load(
            "assets/hit.wav"
        )

        self.bg_music = SoundLoader.load(
            "assets/background.mp3"
        )

        if self.bg_music:
            self.bg_music.loop = True
            self.bg_music.volume = 0.5

        # PLAYER
        self.player = Player()
        self.add_widget(self.player)

        # ENEMIES
        self.enemies = []

        for i in range(3):

            enemy = Enemy(speed=5)

            enemy.y += i * 300

            self.enemies.append(enemy)

            self.add_widget(enemy)

        # SCORE LABEL
        self.score_label = Label(
            text="Score: 0",
            font_size="28sp",
            size_hint=(None, None),
            size=(300, 50),
            pos=(
                Window.width / 2 - 150,
                Window.height - 80
            ),
            halign="center",
            color=(1, 1, 1, 1)
        )

        self.score_label.bind(
            size=self.score_label.setter("text_size")
        )

        self.add_widget(self.score_label)

        # HIGH SCORE LABEL
        self.high_label = Label(
            text=f"High Score: {self.highscore}",
            font_size="22sp",
            size_hint=(None, None),
            size=(300, 50),
            pos=(
                Window.width / 2 - 150,
                Window.height - 130
            ),
            halign="center",
            color=(1, 1, 0, 1)
        )

        self.high_label.bind(
            size=self.high_label.setter("text_size")
        )

        self.add_widget(self.high_label)

        # START BUTTON
        self.start_button = Button(
            text="START GAME",
            font_size="24sp",
            size_hint=(None, None),
            size=(250, 80),
            pos=(
                Window.width / 2 - 125,
                Window.height / 2 - 40
            )
        )

        self.start_button.bind(
            on_press=self.start_game
        )

        self.add_widget(self.start_button)

        Clock.schedule_interval(
            self.update,
            1 / 60
        )

    def start_game(self, instance):

        self.running = True

        self.score = 0

        self.start_button.opacity = 0
        self.start_button.disabled = True

        # PLAY MUSIC
        if self.bg_music:
            self.bg_music.play()

        for enemy in self.enemies:

            enemy.y = randint(
                Window.height,
                Window.height + 800
            )

            enemy.x = randint(
                0,
                int(Window.width - enemy.width)
            )

    def game_over(self):

        self.running = False

        # STOP MUSIC
        if self.bg_music:
            self.bg_music.stop()

        # PLAY HIT SOUND
        if self.hit_sound:
            self.hit_sound.play()

        # SAVE HIGH SCORE
        if self.score > self.highscore:

            self.highscore = self.score

            store.put(
                "highscore",
                score=self.highscore
            )

        self.high_label.text = (
            f"High Score: {self.highscore}"
        )

        self.start_button.opacity = 1
        self.start_button.disabled = False

    def update(self, dt):

        if not self.running:
            return

        # UPDATE SCORE
        self.score += 1

        self.score_label.text = (
            f"Score: {self.score}"
        )

        # DIFFICULTY
        speed_boost = 5 + (
            self.score // 300
        )

        # ENEMY LOGIC
        for enemy in self.enemies:

            enemy.speed = speed_boost

            enemy.fall()

            # RESPAWN
            if enemy.y < -enemy.height:

                enemy.y = randint(
                    Window.height,
                    Window.height + 400
                )

                enemy.x = randint(
                    0,
                    int(Window.width - enemy.width)
                )

            # COLLISION
            if self.player.collide_widget(enemy):

                self.game_over()

    def on_touch_move(self, touch):

        if not self.running:
            return

        self.player.center_x = touch.x

        # KEEP PLAYER INSIDE SCREEN
        if self.player.x < 0:
            self.player.x = 0

        if self.player.right > Window.width:
            self.player.right = Window.width

        self.player.update_graphics()


class DodgeGame(App):

    def build(self):
        return GameWidget()


DodgeGame().run()