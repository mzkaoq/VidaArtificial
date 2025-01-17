import pygame
import random
import math

# Initialize pygame
pygame.init()


# Screen dimensions
WIDTH, HEIGHT = 1700, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Collision Game with Obstacles")
#20px = 1m 

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
TEAM_RED = (255, 0, 0)
TEAM_BLUE = (0, 0, 255)
START_COLOR = (0, 255, 0)
FINISH_COLOR = (255, 255, 0)
OBSTACLE_COLOR = (100, 100, 100)
SPEED = 15


# Clock for controlling frame rate
clock = pygame.time.Clock()

dt = clock.tick(60) / 1000.0
obstacles = [pygame.Rect(WIDTH//2 - 50 , HEIGHT//2 - 100, 50, 200), pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 20, 250, 20)]

def create_obstacle_grid(obstacles, width, height):
    grid = [[0] * width for _ in range(height)]

    for rect in obstacles:
        for x in range(rect.left, rect.right):
            for y in range(rect.top, rect.bottom):
                grid[y][x] = 1

    return grid

obstacle_grid = create_obstacle_grid(obstacles, WIDTH, HEIGHT)


def count_ones_2d(map):
  count = 0
  for row in map:
    for cell in row:
      if cell == 1:
        count += 1
  return count

print(count_ones_2d(obstacle_grid))


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
        self.actual_angle = self.angle
        self.reached = False

    def move(self):
        # Move towards the target point if not reached
        if not self.reached:
            # Predict next position
            next_x = self.x + self.speed * math.cos(self.angle) * dt
            next_y = self.y + self.speed * math.sin(self.angle) * dt

            # Create a rect for the next position to check for collision
            next_rect = pygame.Rect(next_x, next_y, self.size, self.size)
            
            # Check for obstacles
            for obstacle in obstacles:
                if next_rect.colliderect(obstacle):
                    self.avoid_obstacle(obstacle)
                # else:
                #      self.angle = math.atan2(self.target_y - self.y, self.target_x - self.x)

            # No collision detected, move towards target
            self.x = next_x
            self.y = next_y

            # Check if the dot has reached its target
            if math.hypot(self.x - self.target_x, self.y - self.target_y) < self.size * 2:
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

    def avoid_obstacle(self, obstacle):
        # Here, we can either move the dot around the obstacle
        # or simply stop the movement. This example stops the dot.
       
        self.angle = math.atan2(0,0)
      
  



# Create two teams of dots with start and target points
def create_team(count, color, start_x, start_y, target_x, target_y):
    team = []
    for _ in range(count):
        #speed = 1.4 * 20 #speed - 1.4 m/s = 1.4 * 20px 
        speed = SPEED * 20 #speed - 1.4 m/s = 1.4 * 20px 
        size = 10 # diameter of 20px -> 1m 
        team.append(Dot(start_x - random.randrange(10), start_y-random.randrange(10), target_x, target_y, speed, size, color))
    return team

# Red team: start from bottom-left, target top-right
team_red = create_team(30, TEAM_RED, 300, HEIGHT - 300, WIDTH - 300, 300)

# Blue team: start from top-right, target bottom-left
team_blue = create_team(20, TEAM_BLUE, WIDTH - 300, 300, 300, HEIGHT - 300)

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

    pygame.draw.line(screen, BLACK, (50, 150), (100, 150), 1)

    # Draw obstacle in the center
    for obstacle in obstacles:
        pygame.draw.rect(screen, (0, 0, 0), obstacle)

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
