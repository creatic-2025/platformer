"""
Créer par Dorian B. Girard le 13 avril 2026.
Un platformer avec Arcade qui utilise des tilemaps de Tiled pour créer
"""

import arcade
import enum
from pyglet.math import Vec2

WINDOW_HEIGHT = 416
WINDOW_WIDTH = 640
WINDOW_TITLE = "POV: L'oeuf qui s'échappe du magasin"
TILE_SCALE = 2
PLAYER_MOVEMENT_SPEED = 3
PLAYER_JUMP = 10
GRAVITY = 0.5
CAMERA_SPEED = 0.1
VIEWPORT_MARGIN = 220


class GameState(enum.Enum):
    NOT_STARTED = 0
    GAME_STARTED = 1
    GAME_LOSE = 2
    GAME_WIN = 3
    MAP_LOADING = 4


class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        self.background_list_2 = None
        self.jump_platforms_2 = None
        self.kill_platforms_2 = None
        self.special_coin_list_2 = None
        self.coin_list_2 = None
        self.wall_list_2 = None
        self.tile_map_2 = None
        self.kill_platforms = None
        self.jump_platforms = None
        self.special_coin_list = None
        self.coin_counter_text = None
        self.background_list = None
        self.wall_list = None
        self.coin_list = None
        self.background_color = arcade.csscolor.WHITE
        self.game_state = GameState.GAME_STARTED
        self.tile_map = None
        self.scene = None
        self.physics_engine = None
        self.is_paused = False
        self.player_sprite = arcade.Sprite("main_sprite.png", 2, 20, 145)
        self.normal_texture = arcade.load_texture("main_sprite.png")
        self.hit_texture = arcade.load_texture("main_sprite_die.png")
        self.texture = self.normal_texture
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)
        self.coins_counter = 0
        self.camera = arcade.Camera2D()
        self.gui_camera = arcade.Camera2D()
        self.end_of_map = 0
        self.current_map = 1
        self.setup()

        self.camera_sprites = arcade.Camera2D(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.camera_gui = arcade.Camera2D(WINDOW_WIDTH, WINDOW_HEIGHT)



    def setup(self):
        layer_options = {
            "Platforms": {"use_spatial_hash": True},
            "Coins": {"use_spatial_hash": True},
            "SpecialCoin": {"use_spatial_hash": True},
            "KillPlatform": {"use_spatial_hash": True},
            "JumpPlatform": {"use_spatial_hash": True}
        }
        print(dir(self))
        map_name = f"platformer_map_{self.current_map}.tmx"

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALE, layer_options)
        print("DEBUG: map loaded")

        self.wall_list = self.tile_map.sprite_lists["Platforms"]
        self.coin_list = self.tile_map.sprite_lists["Coins"]
        self.special_coin_list = self.tile_map.sprite_lists["SpecialCoin"]
        self.kill_platforms = self.tile_map.sprite_lists["KillPlatform"]
        self.jump_platforms = self.tile_map.sprite_lists["JumpPlatform"]
        self.background_list = self.tile_map.sprite_lists["BackgroundLayer"]
        self.background_color = [130, 200, 229]

        walls = [self.wall_list]
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player_sprite,
            walls=walls,
            gravity_constant=GRAVITY
        )
        self.end_of_map = (self.tile_map.width * self.tile_map.tile_width) * TILE_SCALE
        print(f"{self.end_of_map}")
        self.camera = arcade.Camera2D()

        self.gui_camera = arcade.Camera2D()

    def on_draw(self):
        self.clear()
        self.camera_sprites.use()
        self.background_list.draw()

        self.wall_list.draw()
        self.kill_platforms.draw()
        self.jump_platforms.draw()
        self.coin_list.draw()
        self.special_coin_list.draw()

        self.camera_gui.use()

        self.coin_counter_text = arcade.Text(f"Coins: {self.coins_counter}", 20, 350, arcade.csscolor.
                                             LIGHT_GOLDENROD_YELLOW, 25)
        self.coin_counter_text.draw()
        self.player_sprite_list.draw()
        self.gui_camera.use()
        if self.game_state == GameState.GAME_LOSE:
            self.player_sprite.texture = self.hit_texture
            self.player_sprite.change_y = 20



    def on_key_press(self, key, key_modifiers):
        if self.game_state != GameState.GAME_STARTED:
            return

        if key == arcade.key.SPACE:
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
        if not self.is_paused:
            self.physics_engine.update()
        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.coin_list
        )
        special_coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.special_coin_list
        )
        for coin in special_coin_hit_list:
            coin.remove_from_sprite_lists()
            self.coins_counter += 5
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.coins_counter += 1

        jump_platform_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.jump_platforms
        )

        for boost in jump_platform_hit_list:
            self.player_sprite.change_y = 15

        kill_platform_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.kill_platforms
        )

        for kill_player in kill_platform_hit_list:
            self.is_paused = True
            self.game_state = GameState.GAME_LOSE

        self.scroll_to_player()

    def scroll_to_player(self):
        """
        Scroll the window to the player.

        if CAMERA_SPEED is 1, the camera will immediately move to the desired position.
        Anything between 0 and 1 will have the camera move to the location with a smoother
        pan.
        """

        position = Vec2(self.player_sprite.center_x - self.width / 2,
                        self.player_sprite.center_y - self.height / 2)
        self.camera_sprites.move_to(position, CAMERA_SPEED)

    def on_resize(self, width, height):
        """
        Resize window
        Handle the user grabbing the edge and resizing the window.
        """
        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))
def main():
    window = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    game = GameView()
    window.show_view(game)
    arcade.run()


if __name__ == "__main__":
    main()
