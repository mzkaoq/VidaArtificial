import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
COEFF_DIST = 1.1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Metro Simulation")

# Colors
WHITE = (255, 255, 255)
TEAM_RED = (255, 0, 0)
TEAM_BLUE = (0, 0, 255)
PLATFORM_COLOR = (100, 200, 100)
CART_COLOR = (200, 200, 200)
DOOR_COLOR = (50, 50, 50)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Dot:
    def __init__(self, x, y, temp_target, final_target, speed, size, color):
        self.x = x
        self.y = y
        self.temp_target = temp_target
        self.final_target = final_target
        self.speed = speed
        self.size = size
        self.color = color
        self.angle = math.atan2(temp_target[1] - y, temp_target[0] - x)
        self.reached_temp = False
        self.reached_final = False

    def move(self):
        if not self.reached_final:
            if not self.reached_temp:
                next_x = self.x + self.speed * math.cos(self.angle)
                next_y = self.y + self.speed * math.sin(self.angle)

                if metro_cart.collidepoint(self.x, self.y) or platform.collidepoint(self.x, self.y):
                    self.x = next_x
                    self.y = next_y

                if math.hypot(self.x - self.temp_target[0], self.y - self.temp_target[1]) < self.size * 2:
                    self.reached_temp = True
                    self.angle = math.atan2(
                        self.final_target[1] - self.y, self.final_target[0] - self.x
                    )
            else:
                next_x = self.x + self.speed * math.cos(self.angle)
                next_y = self.y + self.speed * math.sin(self.angle)

                if platform.collidepoint(next_x, next_y) or metro_cart.collidepoint(next_x, next_y):
                    self.x = next_x
                    self.y = next_y

                if math.hypot(self.x - self.final_target[0], self.y - self.final_target[1]) < self.size * 2:
                    self.reached_final = True

    def draw(self, screen):
        if not self.reached_final:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def avoid_overlap(self, other):
        if not self.reached_final and not other.reached_final:
            dist = math.hypot(self.x - other.x, self.y - other.y)
            if dist < self.size * COEFF_DIST + other.size * COEFF_DIST:
                overlap = self.size * COEFF_DIST + other.size * COEFF_DIST - dist
                collision_angle = math.atan2(other.y - self.y, other.x - self.x)
                self.x -= math.cos(collision_angle) * overlap / 2
                self.y -= math.sin(collision_angle) * overlap / 2
                other.x += math.cos(collision_angle) * overlap / 2
                other.y += math.sin(collision_angle) * overlap / 2

# Create dots for metro and platform

def create_dots(count, color, start_area, temp_target, final_target):
    dots = []
    for _ in range(count):
        x = random.randint(start_area.left, start_area.right)
        y = random.randint(start_area.top, start_area.bottom)
        speed = random.uniform(2, 4)
        size = 10
        dots.append(Dot(x, y, temp_target, final_target, speed, size, color))
    return dots

# Define the metro cart and platform
platform = pygame.Rect(20, 0, WIDTH - 40, HEIGHT // 3)
metro_cart = pygame.Rect(platform.left, platform.bottom, platform.width, HEIGHT // 3)

# Define doors
door_width, door_height = 40, 20
metro_doors = [
    pygame.Rect(metro_cart.left + 20, metro_cart.top - door_height, door_width, door_height),
    pygame.Rect(metro_cart.left + 80, metro_cart.top - door_height, door_width, door_height),
    pygame.Rect(metro_cart.right - 120, metro_cart.top - door_height, door_width, door_height),
    pygame.Rect(metro_cart.right - 60, metro_cart.top - door_height, door_width, door_height),
]

# Create people
exiting_people = create_dots(
    20, TEAM_BLUE, metro_cart, (WIDTH // 2, platform.centery), (random.randint(platform.left, platform.right), platform.centery)
)
entering_people = create_dots(
    20, TEAM_RED, platform, (WIDTH // 2, metro_cart.top), (random.randint(metro_cart.left, metro_cart.right), metro_cart.centery)
)
all_dots = exiting_people + entering_people

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw metro cart and platform
    pygame.draw.rect(screen, PLATFORM_COLOR, platform)
    pygame.draw.rect(screen, CART_COLOR, metro_cart)

    # Draw doors
    for door in metro_doors:
        pygame.draw.rect(screen, DOOR_COLOR, door)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move all dots
    for dot in all_dots:
        dot.move()

    # Check for overlaps between all dots
    for i, dot1 in enumerate(all_dots):
        for dot2 in all_dots[i + 1:]:
            dot1.avoid_overlap(dot2)

    # Draw all dots
    for dot in all_dots:
        dot.draw(screen)

    # Check if the game should end
    if all(dot.reached_final for dot in all_dots):
        running = False

    pygame.display.flip()
    clock.tick(60)

# Quit pygame
pygame.quit()
