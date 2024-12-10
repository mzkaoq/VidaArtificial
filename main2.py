import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Game - Opposite Targets")

# Colors
WHITE = (255, 255, 255)
TEAM_RED = (255, 0, 0)
TEAM_BLUE = (0, 0, 255)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Dot:
    def __init__(self, x, y, target_x, target_y, speed, size, color):
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.speed = speed
        self.size = size
        self.color = color
        self.angle = math.atan2(target_y - y, target_x - x)  # Angle toward target
        self.reached = False

    def move(self):
        # Move towards the target point
        if not self.reached:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

            # Check if the dot has reached its target
            if math.hypot(self.x - self.target_x, self.y - self.target_y) < self.speed:
                self.reached = True

    def draw(self, screen):
        # Draw the dot if it hasn't reached its target
        if not self.reached:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def avoid_overlap(self, other):
        # Ensure the dots do not overlap
        if not self.reached and not other.reached:
            dist = math.hypot(self.x - other.x, self.y - other.y)
            if dist < self.size + other.size:
                # Calculate the overlap distance
                overlap = self.size + other.size - dist

                # Calculate the angle of collision
                collision_angle = math.atan2(other.y - self.y, other.x - self.x)

                # Move the dots apart along the collision axis
                self.x -= math.cos(collision_angle) * overlap / 2
                self.y -= math.sin(collision_angle) * overlap / 2

                other.x += math.cos(collision_angle) * overlap / 2
                other.y += math.sin(collision_angle) * overlap / 2

# Create two teams of dots with start and target points
def create_team(count, color, start_x, start_y, target_x, target_y):
    team = []
    for _ in range(count):
        speed = random.uniform(2, 4)
        size = 15
        team.append(Dot(start_x, start_y, target_x, target_y, speed, size, color))
    return team

# Red team: start from bottom-left, target top-right
team_red = create_team(10, TEAM_RED, 50, HEIGHT - 50, WIDTH - 50, 50)

# Blue team: start from top-right, target bottom-left
team_blue = create_team(10, TEAM_BLUE, WIDTH - 50, 50, 50, HEIGHT - 50)

# Combine all dots for processing
all_dots = team_red + team_blue

# Main game loop
running = True
while running:
    screen.fill(WHITE)

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

    # Check if the game should end (all dots have reached their targets)
    if all(dot.reached for dot in all_dots):
        running = False

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Display game over message
screen.fill(WHITE)
font = pygame.font.Font(None, 74)
text = font.render("Game Over!", True, (0, 0, 0))
screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
pygame.display.flip()
pygame.time.wait(3000)

# Quit pygame
pygame.quit()
