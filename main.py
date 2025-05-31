import os
import random
import sys
from screeninfo import get_monitors
import pygame
import win32api
import win32con
import win32gui
import vlc


RADIO_URL = "http://stream.radioparadise.com/mp3-192"

player = vlc.MediaPlayer(RADIO_URL)

player_mode = 1
player.play()


# Function to load mp3 files from a directory
def load_tone_files(directory):
    return [f for f in os.listdir(directory) if f.endswith(".mp3")]


guess_mode = 0
tones_directory = "assets/sound/tones"
tone_files = load_tone_files(tones_directory)

if not tone_files:
    print("AAAAAAAA. No tone files found! No files - No XingTian")
    pygame.quit()
    sys.exit()


def load_rek_images(folder_path):
    images = [
        f for f in os.listdir(folder_path) if "rek" in f and f.endswith(".png")
    ]
    return [
        pygame.image.load(os.path.join(folder_path, img)) for img in images
    ]


rek_images = load_rek_images("assets/img")
rek_image = random.choice(rek_images)

pygame.init()  # musthave (font, etc)
pygame.display.set_caption("Xingtian (Esc)ape")
# icon_image = pygame.image.load('assets/img/rek.png')
pygame.display.set_icon(rek_image)
# Initialize Pygame mixer (musthave)
pygame.mixer.init()

# Get monitor resolution
first_monitor = get_monitors()[0]
size = first_monitor.width, first_monitor.height

screen = pygame.display.set_mode(size, pygame.NOFRAME)
done = False
fuchsia = (255, 0, 128)
dark_red = (139, 0, 0)
clock = pygame.time.Clock()

angle = 0
# Play the initial selected tone
count_guess = 0
GUESS_LIMIT = 5
count_wrong = 0


aura_image = pygame.image.load(
    "assets/img/aura.png"
)
aura_rect = aura_image.get_rect(center=(0, 0))
muse_rect = aura_image.get_rect(center=(size[0], 0))

# pygame.mixer.music.load('./Screenshots/background_music.mp3')
# pygame.mixer.music.play(-1)  # Loop the background music


# Function to play sound
def play_sound(tone_file):
    pygame.mixer.Sound(tones_directory + "/" + tone_file).play()


font = pygame.font.Font(
    "assets/font/RampartOne-Regular.ttf", 64
)


# Yay transparency
hwnd = pygame.display.get_wm_info()["window"]
win32gui.SetWindowLong(
    hwnd,
    win32con.GWL_EXSTYLE,
    win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
    | win32con.WS_EX_LAYERED,
)
win32gui.SetLayeredWindowAttributes(
    hwnd, win32api.RGB(*fuchsia), 0, win32con.LWA_COLORKEY
)
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, size[0], size[1], 0)


# Load xingtian sprite
player_image = pygame.image.load("assets/img/刑天.png")
player_rect = player_image.get_rect()

# Initial xingtian position
x, y = [round(dim / 2) - round(player_rect.width / 2) for dim in size]


speed = 500
window_focused = True


SELECTED_TONE = random.choice(tone_files)
correct_tone = SELECTED_TONE[:-4]  # Get the name without .mp3
print(correct_tone)




def handle_player_mode(mode):
    if mode == 1:
        player.stop()
        return 0
    player.play()
    return 1


while True:
    text_surface = font.render(
        str(count_guess) + "/" + str(GUESS_LIMIT), True, dark_red
    )  # Render the text
    text_rect = text_surface.get_rect(
        center=(size[0] // 2, 50)
    )  # Center the text at the top
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            player.stop()
            #pythoncom.CoUninitialize()
            pygame.quit()
            sys.exit()
        if event.type == pygame.ACTIVEEVENT:
            window_focused = bool(event.gain)

        # Add guess handling here
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                player.stop()
                #pythoncom.CoUninitialize()
                pygame.quit()
                sys.exit()

            guess = pygame.key.name(event.key)
            if guess_mode and guess in ["1", "2", "3", "4"]:
                print("guess in progress...")
                print(correct_tone)
                if guess in correct_tone:
                    x = 0
                    print(f"Correct! Tone was: {correct_tone}")
                    SELECTED_TONE = random.choice(tone_files)
                    correct_tone = SELECTED_TONE[:-4]
                    count_guess += 1
                else:
                    count_wrong = 1
                    print("Wrong! Try again.")
                    print(correct_tone)
                play_sound(SELECTED_TONE)

        if x < 100 and y < 100:
            guess_mode = not guess_mode
            x = size[0]
            y = size[1]
        if x > size[0] - 300 and y < 300:
            player_mode = handle_player_mode(player_mode)
            y = size[1]
            print(player_mode, 's')

    # Movement handling (outside event loop)
    if not window_focused:
        x = size[0] - player_rect.width
        y = size[1] - player_rect.height
    else:
        if guess_mode:
            play_sound(SELECTED_TONE)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            y -= speed * dt
        if keys[pygame.K_DOWN]:
            y += speed * dt
        if keys[pygame.K_LEFT]:
            x -= speed * dt
        if keys[pygame.K_RIGHT]:
            x += speed * dt

    # Keep within bounds
    x = max(0, min(x, size[0] - player_rect.width))
    y = max(0, min(y, size[1] - player_rect.height))

    # Drawing code
    screen.fill(fuchsia)
    if count_guess > GUESS_LIMIT:
        player.stop()
        pythoncom.CoUninitialize()
        pygame.quit()
        sys.exit()
    if count_wrong == 1:
        rek_image = random.choice(rek_images)
        rek_rect = rek_image.get_rect()
        x0 = random.randint(0, size[0] - rek_rect.width)
        y0 = random.randint(0, max(size[1] - 200, size[1] - rek_rect.height))
        screen.blit(rek_image, (x0, y0))
        count_wrong = 0
        x = size[0]
    if pygame.time.get_ticks() // (1000 / (count_guess + 1)) % 2 == 0:
        screen.blit(player_image, (x, y))
    else:
        flipped_sprite = pygame.transform.flip(player_image, True, False)
        screen.blit(flipped_sprite, (x, y))
    rotated_image = pygame.transform.rotate(aura_image, angle)
    rotated_rect = rotated_image.get_rect(center=aura_rect.center)
    rotated_muse_rect = rotated_image.get_rect(center=muse_rect.center)
    if y < size[1] // 2:
        screen.blit(rotated_image, rotated_rect.topleft)
        screen.blit(rotated_image, rotated_muse_rect.topleft)
    angle += 1  # Adjust the speed of rotation here
    if angle >= 360:
        angle = 0
    # Draw the guess count text
    if guess_mode:
        screen.blit(text_surface, text_rect)

    pygame.display.update()
