import pygame
import time
import os
import tkinter as tk
from tkinter import simpledialog

# Constants
WIDTH, HEIGHT = 1200, 800  # Default window size
PODIUM_WIDTH = 150
PODIUM_DEPTH = 50
PODIUM_HEIGHTS = [300, 250, 200, 150]  # Heights for up to 4 podiums
PODIUM_COLORS = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (0, 255, 0)]  # Up to 4 colors
BUTTON_COLOR = (0, 255, 0)
BUTTON_HOVER_COLOR = (0, 200, 0)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Animated Podium for VEX EXP with Bots")

# Set custom window icon
icon_path = r"C:\Users\om31d\Desktop\Animated Podium\assets\app_logo.png"
if os.path.exists(icon_path):
    icon_image = pygame.image.load(icon_path)
    pygame.display.set_icon(icon_image)
else:
    print("Icon image not found! Using default Pygame logo.")

# Fonts and Sounds
font = pygame.font.Font(None, 30)  # Smaller font size for team members
sound_effect = pygame.mixer.Sound(r"C:\Users\om31d\Desktop\Animated Podium\assets\podium_rise.wav")

# Function to load bot image
def load_bot_image():
    bot_image_path = r"C:\Users\om31d\Desktop\Animated Podium\assets\bot.png"
    if os.path.exists(bot_image_path):
        return pygame.image.load(bot_image_path)
    else:
        print("Bot image not found! Using placeholder.")
        return pygame.Surface((50, 50))

# Function to collect the number of teams and members using tkinter dialogs
def get_team_and_member_names():
    teams = []
    
    # Create a tkinter root window, but keep it hidden
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Get number of teams
    num_teams = simpledialog.askinteger("Input", "Enter the number of teams:", minvalue=1)
    
    for i in range(num_teams):
        # Get the number of members in the current team
        num_members = simpledialog.askinteger("Input", f"Enter the number of members in Team {i + 1}:", minvalue=1)
        members = []
        for j in range(num_members):
            # Get the member name
            member_name = simpledialog.askstring("Input", f"Enter the name of member {j + 1} for Team {i + 1}:")
            members.append(member_name)
        teams.append((f"Team {i + 1}", members))  # Automatically generate team names like "Team 1", "Team 2"
    
    return teams

# Function to calculate podium positions dynamically based on the number of teams
def calculate_staggered_podium_positions(num_teams, screen_width, screen_height):
    positions = []
    center_x = screen_width // 2
    spacing = screen_width // (num_teams + 1)  # Adjust horizontal space based on number of teams
    for i in range(num_teams):
        x = center_x - (num_teams // 2 - i) * spacing  # Evenly space podiums
        y = screen_height - PODIUM_HEIGHTS[i % len(PODIUM_HEIGHTS)] - 100  # Dynamic vertical position
        positions.append((x, y))
    return positions

# Function to draw 3D podium
def draw_3d_podium(x, y, width, height, depth, color):
    pygame.draw.polygon(screen, color, [(x, y), (x + width, y), (x + width - depth, y - depth), (x - depth, y - depth)])
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.polygon(screen, [c // 1.5 for c in color], [
        (x + width, y),
        (x + width - depth, y - depth),
        (x + width - depth, y - depth + height),
        (x + width, y + height),
    ])

# Function to draw bot on the podium with the requested adjustments
def draw_bot_on_podium(x, y, width, height, bot_image, screen_width, screen_height):
    bot_size = screen_width // 15  # Dynamic bot size
    bot_x = x + (width - bot_size) // 2 - 50  # Shift 30px to the left
    bot_y = y - bot_size - (screen_height // 15) - 60 # Shift 20px up
    screen.blit(bot_image, (bot_x, bot_y))

# Function to draw start button
def draw_start_button():
    button_width, button_height = 300, 100
    button_x = (WIDTH - button_width) // 2
    button_y = (HEIGHT - button_height) // 2
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Change button color when mouse hovers over it
    if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
        pygame.draw.rect(screen, BUTTON_HOVER_COLOR, (button_x, button_y, button_width, button_height))
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, button_y, button_width, button_height))

    # Button text
    text_surface = font.render("Start Podium", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(text_surface, text_rect)

    return button_x, button_y, button_width, button_height

# Main Game Loop
def main():
    running = True
    animation_started = False
    bot_image = load_bot_image()
    teams = get_team_and_member_names()
    
    y_offsets = [HEIGHT] * len(teams)
    target_y_offsets = [HEIGHT - PODIUM_HEIGHTS[i % len(PODIUM_HEIGHTS)] for i in range(len(teams))]
    ANIMATION_SPEED = 5
    
    while running:
        screen.fill((30, 30, 30))  # Background color
        screen_width, screen_height = pygame.display.get_surface().get_size()  # Dynamic screen size

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detect button click
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                button_x, button_y, button_width, button_height = draw_start_button()
                if button_x < event.pos[0] < button_x + button_width and button_y < event.pos[1] < button_y + button_height:
                    animation_started = True
                    sound_effect.play()

        # If animation has started, animate podiums and remove button
        if animation_started:
            for i in range(len(y_offsets)):
                if y_offsets[i] > target_y_offsets[i]:
                    y_offsets[i] -= ANIMATION_SPEED
                elif y_offsets[i] < target_y_offsets[i]:
                    y_offsets[i] = target_y_offsets[i]  # Snap to final position

            podium_positions = calculate_staggered_podium_positions(len(teams), screen_width, screen_height)

            for i, (team_name, members) in enumerate(teams):
                x, y = podium_positions[i]
                current_y = y_offsets[i]
                draw_3d_podium(x, current_y, PODIUM_WIDTH, PODIUM_HEIGHTS[i % len(PODIUM_HEIGHTS)], PODIUM_DEPTH, PODIUM_COLORS[i % len(PODIUM_COLORS)])

                # Display team members on the podium with adjusted position (25px right and 20px down)
                for idx, member in enumerate(members):
                    member_text = font.render(member, True, (0, 0, 0))  # Smaller font
                    member_rect = member_text.get_rect(center=(x + 35, current_y - 40 + (idx * 30) + 20))  # Adjusted position
                    screen.blit(member_text, member_rect)

                # Draw bot on top of the podium with adjusted position
                draw_bot_on_podium(x, current_y, PODIUM_WIDTH, PODIUM_HEIGHTS[i % len(PODIUM_HEIGHTS)], bot_image, screen_width, screen_height)

        # Draw start button
        if not animation_started:
            draw_start_button()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()