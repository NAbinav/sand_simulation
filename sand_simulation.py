import pygame
import random
import math
# Initialize Pygame
pygame.init()
# Constants for the screen size
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
TILE_SIZE =7

class FallingObject:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.fall_speed = 7

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, pygame.Rect(self.x, self.y, self.width, self.height))

    def fall(self, screen):
        if self.y >= SCREEN_HEIGHT - self.height:
            return

        if self.y < SCREEN_HEIGHT - self.height :
            below = screen.get_at((self.x, min(self.y+10,SCREEN_HEIGHT-1)))
            pixel_color = screen.get_at((self.x, self.y +6))
            belowr = screen.get_at((min(SCREEN_WIDTH-1,self.x+TILE_SIZE), self.y + self.height))
            belowl = screen.get_at((max(self.x-TILE_SIZE,0), self.y + self.height))
            # belowl = screen.get_at((self.x-8, self.y + self.height))
            # Check neighbor colors, ensure x stays within bounds
            if below== screen.get_at((0, 6)):
                self.y += self.fall_speed
            else:
                if belowr!=screen.get_at((0, 6))  and belowl==screen.get_at((0, 6)):
                    self.x-=TILE_SIZE
                    self.y += self.fall_speed
                elif belowr==screen.get_at((0, 6))  and belowl!=screen.get_at((0, 6)):
                    self.x+=TILE_SIZE
                    self.y += self.fall_speed
                if belowl==screen.get_at((0, 6)) and belowr==screen.get_at((0, 6)):
                    self.x+=[-1*TILE_SIZE,TILE_SIZE][random.randint(0,1)]
                    self.y += self.fall_speed
class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Falling Objects Simulation")
        self.clock = pygame.time.Clock()

        # Store multiple falling objects in a list
        self.falling_objects = []

        self.done = False

    def draw_grid(self):
        for x in range(0, SCREEN_WIDTH, TILE_SIZE):
            for y in range(0, SCREEN_HEIGHT, TILE_SIZE):
                rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, (60, 60, 60), rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1)

    def run(self):
        while not self.done:
            mx,my=pygame.mouse.get_pos()
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    raise SystemExit 
            hue_x = (mx / SCREEN_WIDTH) * 360  # Map horizontal movement to hue
            hue_y = (my / SCREEN_HEIGHT) * 360  # Map vertical movement to 0-180 range

            # Combine them in a more intuitive way, possibly averaging them
            hue = (hue_y )  # This combines both the horizontal and vertical positions
            # Convert HSL to RGB
            c = (1 - abs(2 * 0.5 - 1)) * 1  # Saturation = 1, Lightness = 0.5
            x = c * (1 - abs((hue / 60) % 2 - 1))
            m = 0.5 - c / 2
            r, g, b = 0, 0, 0

            if 0 <= hue < 60:
                r, g, b = c, x, 0
            elif 60 <= hue < 120:
                r, g, b = x, c, 0
            elif 120 <= hue < 180:
                r, g, b = 0, c, x
            elif 180 <= hue < 240:
                r, g, b = 0, x, c
            elif 240 <= hue < 300:
                r, g, b = x, 0, c
            elif 300 <= hue < 360:
                r, g, b = c, 0, x

            r = math.floor((r + m) * 255)
            g = math.floor((g + m) * 255)
            b = math.floor((b + m) * 255)

            self.falling_objects.append(
                FallingObject((mx // TILE_SIZE) * TILE_SIZE,
                              (my // TILE_SIZE) * TILE_SIZE,
                              TILE_SIZE, TILE_SIZE,
                              (r, g, b))
            )

            self.screen.fill((0, 0, 0))

            # Draw the grid
            self.draw_grid()

            # Update and draw each falling object
            for obj in self.falling_objects:
                obj.fall(self.screen)
                obj.draw(self.screen)

            # Update display
            pygame.display.flip()

            # Frame rate
            self.clock.tick(70)

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = Game()
    game.run()
