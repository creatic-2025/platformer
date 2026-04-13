"""
Créer par Dorian B. Girard le 13 avril 2026.
Un platformer avec Arcade qui utilise des tilemaps de Tiled pour créer
"""

import arcade
import random
from enum import Enum

WINDOW_HEIGHT = 672
WINDOW_WIDTH = 960
WINDOW_TITLE = "POV: L'oeuf qui s'échappe du magasin"


class GameState(Enum):
    NOT_STARTED = 0
    GAME_STARTED = 1
    GAME_LOSE = 2
    GAME_WIN = 3


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        game_state = None
        self.background_color = arcade.csscolor.WHITE

    def on_key_press(self, key, key_modifiers):
        if arcade.key == arcade.key.SPACE and GameState.NOT_STARTED:
            game_state = GameState.GAME_STARTED
            print("Game Started")




def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
