import pygame
from minigrid.core.world_object import WorldObj


class CustomSprite(WorldObj):
    def __init__(self, obj, image, color='grey'):
        """
        Initialize a CustomSprite with a given object type and custom image.
        """
        super().__init__(obj.type, color)
        self.obj = obj
        self.image = image

    def can_overlap(self):
        return self.obj.can_overlap()

    def render(self, img):
        tile_size = img.shape[0]

        # Scale the image to fit the tile size
        scaled_image = pygame.transform.scale(self.image, (tile_size, tile_size))

        # Create a Surface to handle transparency
        transparent_bg = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)

        # Blit the scaled image onto the transparent background surface
        transparent_bg.blit(scaled_image, (0, 0))

        # Convert the transparent surface to a numpy array
        final_image_array = pygame.surfarray.pixels3d(transparent_bg)
        alpha_array = pygame.surfarray.pixels_alpha(transparent_bg)

        # Apply the transparent image to the grid cell (RGB only)
        for x in range(tile_size):
            for y in range(tile_size):
                if alpha_array[x, y] > 0:  # Only apply non-transparent pixels
                    img[x, y, :3] = final_image_array[x, y, :3]  # Apply RGB values only

        # Clean up the pixel arrays
        del final_image_array
        del alpha_array
