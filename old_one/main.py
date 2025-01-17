import pygame
import random

# Constants representing the defaults
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
AGENT_COUNT = 100
AGENT_RADIUS = 10
AGENT_COLOR = (0, 255, 0)
MAX_SPEED = 5

# Agent class representing each individual in the crowd
class Agent:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed_x = random.uniform(-MAX_SPEED, MAX_SPEED)
        self.speed_y = random.uniform(-MAX_SPEED, MAX_SPEED)

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def bounce(self):
        if self.x <= 0 + self.radius or self.x >= SCREEN_WIDTH - self.radius:
            self.speed_x *= -1
        if self.y <= 0 + self.radius or self.y >= SCREEN_HEIGHT - self.radius:
            self.speed_y *= -1

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Real-Time Crowd Simulation')

# Create a list to hold all the agents
agents = [Agent(random.randint(AGENT_RADIUS, SCREEN_WIDTH-AGENT_RADIUS),
                random.randint(AGENT_RADIUS, SCREEN_HEIGHT-AGENT_RADIUS),
                AGENT_RADIUS, AGENT_COLOR) for _ in range(AGENT_COUNT)]

running = True
# Main loop
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update agent positions
    for agent in agents:
        agent.move()
        agent.bounce()

    # Fill the screen with a black background
    screen.fill((0, 0, 0))

    # Draw all the agents
    for agent in agents:
        agent.draw(screen)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit the game
pygame.quit()