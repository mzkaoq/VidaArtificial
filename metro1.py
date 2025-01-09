import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
COEFF_DIST = 1.1
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Game with Temporary Targets")

# Colors
WHITE = (255, 255, 255)
TEAM_RED = (255, 0, 0)
TEAM_BLUE = (0, 0, 255)
START_COLOR = (0, 255, 0)
FINISH_COLOR = (255, 255, 0)
WALL_COLOR = (100, 100, 100)

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Dot:
    def __init__(self, x, y, temp_target, final_target, speed, size, color):
        self.x = x
        self.y = y
        self.temp_target = temp_target  # Temporary target as (x, y)
        self.final_target = final_target  # Final target as a Rect
        self.speed = speed
        self.size = size
        self.color = color
        self.angle = math.atan2(temp_target[1] - y, temp_target[0] - x)  # Angle toward temporary target
        self.reached_temp = False
        self.reached_final = False

    def move(self):
        if not self.reached_final:
            if not self.reached_temp:
                # Move towards temporary target
                self.x += self.speed * math.cos(self.angle)
                self.y += self.speed * math.sin(self.angle)

                # Check if the dot has reached its temporary target
                if math.hypot(self.x - self.temp_target[0], self.y - self.temp_target[1]) < self.size * 2:
                    self.reached_temp = True
                    # Recalculate angle to the final target
                    self.angle = math.atan2(
                        self.final_target.centery - self.y, self.final_target.centerx - self.x
                    )
            else:
                # Move towards final target
                self.x += self.speed * math.cos(self.angle)
                self.y += self.speed * math.sin(self.angle)

                # Check if the dot has reached its final target
                if self.final_target.collidepoint(self.x, self.y):
                    self.reached_final = True

    def draw(self, screen):
        if not self.reached_final:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

    def avoid_overlap(self, other):
        if not self.reached_final and not other.reached_final:
            dist = math.hypot(self.x - other.x, self.y - other.y)
            if dist < self.size * COEFF_DIST + other.size * COEFF_DIST:
                # Calculate the overlap distance
                overlap = self.size * COEFF_DIST + other.size * COEFF_DIST - dist

                # Calculate the angle of collision
                collision_angle = math.atan2(other.y - self.y, other.x - self.x)

                # Move the dots apart along the collision axis
                self.x -= math.cos(collision_angle) * overlap / 2
                self.y -= math.sin(collision_angle) * overlap / 2

                other.x += math.cos(collision_angle) * overlap / 2
                other.y += math.sin(collision_angle) * overlap / 2

# Create two teams of dots with start, temporary, and final targets
def create_team(count, color, start_area, temp_target, final_target):
    team = []
    for _ in range(count):
        x = random.randint(start_area.left, start_area.right)
        y = random.randint(start_area.top, start_area.bottom)
        speed = random.uniform(2, 4)
        size = 15
        team.append(Dot(x, y, temp_target, final_target, speed, size, color))
    return team

# Define start areas and targets
red_start = pygame.Rect(0, 0, WIDTH // 2 - 40, HEIGHT)  # Left side
blue_start = pygame.Rect(WIDTH // 2 + 40, 0, WIDTH // 2 - 40, HEIGHT)  # Right side

# Temporary targets
red_temp_target = (WIDTH // 2, HEIGHT // 3 + 20)  # Gap between top and middle wall
blue_temp_target = (WIDTH // 2, 2 * HEIGHT // 3 - 20)  # Gap between middle and bottom wall

# Final targets
red_finish = pygame.Rect(WIDTH - 120, HEIGHT // 2 - 60, 40, 40)
blue_finish = pygame.Rect(80, HEIGHT // 2 + 60, 40, 40)

# Create teams
team_red = create_team(10, TEAM_RED, red_start, red_temp_target, red_finish)
teamb_blue = create_team(10, TEAM_BLUE, blue_start, blue_temp_target, blue_finish)

# Combine all dots for processing
all_dots = team_red + teamb_blue

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw finish areas
    pygame.draw.rect(screen, FINISH_COLOR, red_finish)  # Red finish
    pygame.draw.rect(screen, FINISH_COLOR, blue_finish)  # Blue finish

    # Draw the three vertical walls
    wall_thickness = 14
    wall_gap = 40  # Gap between walls
    pygame.draw.rect(screen, WALL_COLOR, (WIDTH // 2 - wall_thickness // 2, 0, wall_thickness, HEIGHT // 3 - wall_gap))  # Upper wall
    pygame.draw.rect(screen, WALL_COLOR, (WIDTH // 2 - wall_thickness // 2, HEIGHT // 3 + wall_gap, wall_thickness, HEIGHT // 3 - 2 * wall_gap))  # Middle wall
    pygame.draw.rect(screen, WALL_COLOR, (WIDTH // 2 - wall_thickness // 2, 2 * HEIGHT // 3 + wall_gap, wall_thickness, HEIGHT // 3 - wall_gap))  # Lower wall

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
    if all(dot.reached_final for dot in all_dots):
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
