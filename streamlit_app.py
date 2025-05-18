import streamlit as st
import pygame
import numpy as np
from PIL import Image

# Initialize Pygame
pygame.init()

# Set up the game
WIDTH = 800
HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Sphere class
class Sphere:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 5

    def move(self, dx, dy):
        self.x += dx * self.speed
        self.y += dy * self.speed

    def draw(self, surface):
        pygame.draw.circle(surface, BLUE, (int(self.x), int(self.y)), self.radius)

# Function to render Pygame surface to a Streamlit-compatible image
def pygame_to_streamlit(surface):
    return Image.fromarray(pygame.surfarray.array3d(surface).swapaxes(0, 1))

# Streamlit app
st.set_page_config(page_title="Moving Sphere Game", page_icon="⚪", layout="wide")

st.title("⚪ Moving Sphere Game")

# Initialize game objects
if 'sphere' not in st.session_state:
    st.session_state.sphere = Sphere(WIDTH // 2, HEIGHT // 2, 20)

# Game loop
def game_loop():
    screen = pygame.Surface((WIDTH, HEIGHT))
    screen.fill(WHITE)

    # Get user input
    keys = pygame.key.get_pressed()
    dx, dy = 0, 0
    if keys[pygame.K_w]:  # Move up
        dy = -1
    if keys[pygame.K_s]:  # Move down
        dy = 1
    if keys[pygame.K_a]:  # Move left
        dx = -1
    if keys[pygame.K_d]:  # Move right
        dx = 1

    # Move the sphere
    st.session_state.sphere.move(dx, dy)

    # Keep the sphere within the screen bounds
    st.session_state.sphere.x = max(st.session_state.sphere.radius, min(st.session_state.sphere.x, WIDTH - st.session_state.sphere.radius))
    st.session_state.sphere.y = max(st.session_state.sphere.radius, min(st.session_state.sphere.y, HEIGHT - st.session_state.sphere.radius))

    # Draw the sphere
    st.session_state.sphere.draw(screen)

    return pygame_to_streamlit(screen)

# Main game display
game_image = st.empty()

# Game loop execution
while True:
    game_image.image(game_loop(), use_column_width=True)
    pygame.time.delay(100)  # Control the frame rate
