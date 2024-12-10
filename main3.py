import pygame
import random
import math

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Game with Obstacles")

# Colors
WHITE = (255, 255, 255)
TEAM_RED = (255, 0, 0)
TEAM_BLUE = (0, 0, 255)
START_COLOR = (0, 255, 0)
FINISH_COLOR = (255, 255, 0)
OBSTACLE_COLOR = (100, 100, 100)

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
        # Move towards the target point if not reached
        if not self.reached:
            self.x += self.speed * math.cos(self.angle)
            self.y += self.speed * math.sin(self.angle)

            # Check if the dot has reached its target
            if math.hypot(self.x - self.target_x, self.y - self.target_y) < self.size * 2:
                self.reached = True

            # Avoid obstacle
            self.avoid_obstacle()

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

    def avoid_obstacle(self):
        # Check if the dot is too close to the obstacle
        obstacle_center = (WIDTH // 2, HEIGHT // 2)
        obstacle_radius = 100
        dist = math.hypot(self.x - obstacle_center[0], self.y - obstacle_center[1])

        if dist < obstacle_radius + self.size:
            # Adjust direction to move away from the obstacle
            angle_to_obstacle = math.atan2(obstacle_center[1] - self.y, obstacle_center[0] - self.x)
            self.x -= math.cos(angle_to_obstacle) * self.speed
            self.y -= math.sin(angle_to_obstacle) * self.speed
            self.angle += random.uniform(-0.2, 0.2)  # Slightly adjust the angle to avoid getting stuck
        else:
            self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

# Create two teams of dots with start and target points
def create_team(count, color, start_x, start_y, target_x, target_y):
    team = []
    for _ in range(count):
        speed = random.uniform(2, 4)
        size = 15
        team.append(Dot(start_x, start_y, target_x, target_y, speed, size, color))
    return team

# Red team: start from bottom-left, target top-right
team_red = create_team(10, TEAM_RED, 100, HEIGHT - 100, WIDTH - 100, 100)

# Blue team: start from top-right, target bottom-left
team_blue = create_team(10, TEAM_BLUE, WIDTH - 100, 100, 100, HEIGHT - 100)

# Combine all dots for processing
all_dots = team_red + team_blue

# Main game loop
running = True
while running:
    screen.fill(WHITE)

    # Draw start and finish squares
    pygame.draw.rect(screen, START_COLOR, (80, HEIGHT - 120, 40, 40))  # Red start
    pygame.draw.rect(screen, FINISH_COLOR, (WIDTH - 120, 80, 40, 40))  # Red finish
    pygame.draw.rect(screen, START_COLOR, (WIDTH - 120, 80, 40, 40))  # Blue start
    pygame.draw.rect(screen, FINISH_COLOR, (80, HEIGHT - 120, 40, 40))  # Blue finish

    # Draw obstacle in the center
    pygame.draw.circle(screen, OBSTACLE_COLOR, (WIDTH // 2, HEIGHT // 2), 100)

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
pygame.time.wait(1)

# Quit pygame
pygame.quit()
