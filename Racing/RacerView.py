import arcade
import time
from Car import Car
from FinishLine import FinishLine
from PIL import Image
from Checkpoint import Checkpoint

class RacerView(arcade.View):

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.camera = arcade.Camera2D()
        
        self.map = arcade.load_texture("Racing/images/map.png")
        self.map_rect = arcade.Rect.from_kwargs(left=0, bottom=0, width=self.map.width * 4, height=self.map.height * 4)

        self.map_mask = Image.open("Racing/images/map.png").convert("RGB")
        self.mask_pixels = self.map_mask.load()

        self.map_mask_checkpoints = Image.open("Racing/images/Map_Mask_Checkpoints.png").convert("RGB")
        self.mask_checkpoints_pixels = self.map_mask_checkpoints.load()

        self.sprite_list = arcade.SpriteList()

        self.finish_line = FinishLine("Racing/images/Finish_Line.png", 4)
        self.finish_line.center_x = 1808
        self.finish_line.center_y = 7335
        self.sprite_list.append(self.finish_line)

        self.car = Car("Racing/images/car.png", 0.2)
        self.car.center_x = self.finish_line.center_x
        self.car.center_y = self.finish_line.center_y
        self.sprite_list.append(self.car)

        self.paused = False
        self.velocity_multiplier = 1.0

        self.checkpoints_passed = 0
        self.on_checkpoint = False
        self.checkpoint_colour = [(188, 6, 6), (188, 91, 5), (188, 177, 5), (132, 5, 188)]
        self.current_colour_index = 0

         # Held keys
        self.held_w = False
        self.held_s = False
        self.held_a = False
        self.held_d = False

        # Checkpoints
        self.checkpoints = []
        self.on_checkpoint = False 

        visited = set()

        # Timer
        self.start_time = time.time()
        self.current_time = 0.0

        for y in range(self.map_mask_checkpoints.height):
            for x in range(self.map_mask_checkpoints.width):
                if self.mask_checkpoints_pixels[x, y] == self.checkpoint_colour[self.current_colour_index] and (x, y) not in visited:

                    # Flood fill to find the whole red band
                    pixels = self.flood_fill_checkpoint(x, y, visited)

                    # Convert pixel cluster to bounding box
                    xs = [p[0] for p in pixels]
                    ys = [p[1] for p in pixels]

                    left   = min(xs) * 4
                    right  = (max(xs) + 1) * 4
                    bottom = (self.map_mask_checkpoints.height - max(ys) - 1) * 4
                    top    = (self.map_mask_checkpoints.height - min(ys)) * 4

                    rect = arcade.Rect.from_kwargs(
                        left=left,
                        bottom=bottom,
                        width=right - left,
                        height=top - bottom
                    )

                    self.checkpoints.append(
                        Checkpoint(rect, len(self.checkpoints))
                    )

    def on_draw(self):
        self.clear()

        self.camera.use()

        # Draw map
        arcade.draw_texture_rect(
            self.map,
            self.map_rect
        )

        self.sprite_list.draw()

        # Draw timer
        arcade.draw_text(
            f"Time: {self.current_time:.2f}s",
            self.camera.position[0] - self.camera.viewport_width / 2 + 10,
            self.camera.position[1] + self.camera.viewport_height / 2 - 30,
            arcade.color.WHITE,
            20
        )


    def on_update(self, delta_time: float):
        if self.paused:
            return
        
        self.current_time = time.time() - self.start_time

        # Car current position
        px, py = self.world_to_mask(
        self.car.center_x,
        self.car.center_y
        )

        # Clamp to map image bounds
        px = max(0, min(px, self.map.width - 1))
        py = max(0, min(py, self.map.height - 1))

        if arcade.check_for_collision(self.car, self.finish_line ) and self.checkpoints_passed >= 52:
            print("Finished!")
            arcade.close_window()

        # Checkpoint and end detection
        r_c, g_c, b_c = self.mask_checkpoints_pixels[px, py]

        if (r_c, g_c, b_c) == self.checkpoint_colour[self.current_colour_index] and self.checkpoints_passed < 52:
            if not self.on_checkpoint:
                self.checkpoints_passed += 1
                self.on_checkpoint = True
                self.current_colour_index += 1
                if (self.current_colour_index % 4) == 0:
                    self.current_colour_index = 0
                print(f"Checkpoint {self.checkpoints_passed} passed, next colour: {self.checkpoint_colour[self.current_colour_index]}")
        else:
            self.on_checkpoint = False

        r, g, b = self.mask_pixels[px, py]
        
        # Collision
        if (r, g, b) == (56, 56, 56):
            self.collision()
        # Grass
        elif (r, g, b) == (83, 209, 72):
            self.velocity_multiplier = 0.5
        else:
            self.velocity_multiplier = 1.0
        
        # Accelerate or decelerate based on held keys
        if self.held_w:
            self.car.Accelerate(10 * self.velocity_multiplier * delta_time)
                
        if self.held_s:
            self.car.Decelerate(10 * self.velocity_multiplier * delta_time)

        # Rotate based on held keys
        if self.held_a:
            self.car.Rotate(-120 * delta_time)

        if self.held_d:
            self.car.Rotate(120 * delta_time)

        # Apply drag
        if (r, g, b) != (83, 209, 72):
            self.car.apply_drag(0.99)
        else:
            self.car.apply_drag(0.97)

        self.camera.position = self.car.position
        
        self.sprite_list.update()

    # Key Press Handler
    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.Q:
            # Quit immediately
            arcade.close_window()

        if symbol == arcade.key.P:
            self.paused = not self.paused

        if symbol == arcade.key.W:
            self.held_w = True

        if symbol == arcade.key.S:
            self.held_s = True

        if symbol == arcade.key.A:
            self.held_a = True

        if symbol == arcade.key.D:
            self.held_d = True

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.held_w = False
        
        if symbol == arcade.key.S:
            self.held_s = False

        if symbol == arcade.key.A:
            self.held_a = False

        if symbol == arcade.key.D:
            self.held_d = False


    def world_to_mask(self, x, y):
        px = int(x / 4)
        py = int(y / 4)

        py = (self.map.height - 1) - py

        return px, py
    
    def flood_fill_checkpoint(self, start_x, start_y, visited):
        stack = [(start_x, start_y)]
        pixels = []

        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            if self.mask_checkpoints_pixels[x, y] != (188, 6, 6):
                continue

            visited.add((x, y))
            pixels.append((x, y))

            stack.extend([
                (x+1, y), (x-1, y),
                (x, y+1), (x, y-1)
            ])

        return pixels
    
    def collision(self):
        arcade.close_window()