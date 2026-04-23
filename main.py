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
PLAYER_MOVEMENT_SPEED = 3
PLAYER_JUMP = 11
GRAVITY = 0.5


class GameState(enum.Enum):
    NOT_STARTED = 0
    GAME_STARTED = 1
    GAME_LOSE = 2
    GAME_WIN = 3


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background_list = None
        self.wall_list = None
        self.coin_list = None
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
            "Platforms": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
        }

        self.tile_map = arcade.load_tilemap("platformer_map.tmx", TILE_SCALE, layer_options)
        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]
        self.background_list = self.tile_map.sprite_lists["BackgroundLayer"]

        walls = [self.wall_list]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            walls,
            gravity_constant=GRAVITY
        )

    def on_draw(self):
        self.clear()
        self.background_list.draw()
        self.player_sprite_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.SPACE:
            if self.game_state == GameState.NOT_STARTED:
                self.game_state = GameState.GAME_STARTED
                if self.physics_engine.can_jump():
                    self.player_sprite.change_y = PLAYER_JUMP
        if key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED * -1

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        print(f"{self.physics_engine.can_jump()}")


def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
