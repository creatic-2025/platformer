"""
Créer par Dorian B. Girard le 13 avril 2026.
Un platformer avec Arcade qui utilise des tilemaps de Tiled pour créer
"""

import arcade
import enum

WINDOW_HEIGHT = 416
WINDOW_WIDTH = 640
WINDOW_TITLE = "POV: L'oeuf qui s'échappe du magasin"
TILE_SCALE = 2


class GameState(enum.Enum):
    NOT_STARTED = 0
    GAME_STARTED = 1
    GAME_LOSE = 2
    GAME_WIN = 3


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_color = arcade.csscolor.WHITE
        self.game_state = GameState.NOT_STARTED
        self.tile_map = None
        self.scene = None
        self.physics_engine = None
        self.player_sprite = arcade.Sprite("main_sprite.png", 2, 20, 145)
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)
        self.setup()

    def setup(self):
        layer_options = {
            "Platforms": {"use_spatial_hash": True}
        }

        self.tile_map = arcade.load_tilemap("platformer_map.tmx", TILE_SCALE, layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls=self.scene["Platforms"],
            gravity_constant=0.5
        )

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.player_sprite_list.draw()

    def on_key_press(self, key, key_modifiers):
        if arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.GAME_STARTED



def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
