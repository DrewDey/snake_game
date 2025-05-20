import pygame
import random

# Initialize Pygame
pygame.init()

# Define screen dimensions
screen_width = 600
screen_height = 400

# Create the game display
screen = pygame.display.set_mode((screen_width, screen_height))

# Set window caption
pygame.display.set_caption("Retro Snake")

# Define colors
black = (0, 0, 0)
grid_color = (40, 40, 40) # Dark grey for the grid
green = (0, 255, 0)
red = (255, 0, 0)

# Snake properties
snake_block_size = 10
snake_speed = 15 # Frames per second

# Initialize snake
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_body = [[snake_x, snake_y]] # List of [x,y] coordinates for snake blocks
snake_direction = "RIGHT"

# Food properties
food_block_size = 10
food_pos = [0,0] # Will be updated by spawn_food

# Initialize Clock for controlling game speed
clock = pygame.time.Clock()

# Score
score = 0

# Initialize fonts (done once after pygame.init())
pygame.font.init() 
# Load the custom retro font
font_path = "retro_font.ttf" 
try:
    font_style = pygame.font.Font(font_path, 20) # Smaller size for general messages
    score_font = pygame.font.Font(font_path, 28) # Slightly larger for score
    game_over_font = pygame.font.Font(font_path, 40) # Larger for "Game Over"
except pygame.error as e:
    print(f"Error loading font {font_path}: {e}. Using default system fonts.")
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    game_over_font = pygame.font.SysFont("comicsansms", 50)


def display_score(current_score_val):
    """Renders and displays the current score."""
    value = score_font.render("Your Score: " + str(current_score_val), True, (255,255,0)) # Yellow
    screen.blit(value, [10, 10])

# Helper function to display messages
def message(msg, color, y_displace=0, font=None):
    if font is None: # Default font if none provided
        font = font_style
    mesg = font.render(msg, True, color)
    # Center the message, allow y_displace for vertical positioning
    text_rect = mesg.get_rect(center=(screen_width / 2, screen_height / 2 + y_displace))
    screen.blit(mesg, text_rect)

# --- Core Logic Functions for Testing ---

def update_snake_head_logic(current_x, current_y, direction, block_size):
    """Calculates new head position based on direction."""
    if direction == "UP":
        current_y -= block_size
    elif direction == "DOWN":
        current_y += block_size
    elif direction == "LEFT":
        current_x -= block_size
    elif direction == "RIGHT":
        current_x += block_size
    return current_x, current_y

def check_wall_collision_logic(head_x, head_y, screen_w, screen_h):
    """Checks for collision with screen boundaries."""
    if head_x >= screen_w or head_x < 0 or head_y >= screen_h or head_y < 0:
        return True
    return False

def check_self_collision_logic(new_head_coords, current_snake_body):
    """Checks if the snake's head collides with its body.
    current_snake_body is the body *before* the new head is added."""
    for segment in current_snake_body:
        if segment[0] == new_head_coords[0] and segment[1] == new_head_coords[1]:
            return True
    return False

def spawn_food_logic(current_snake_body_list, screen_w, screen_h, block_s):
    """Generates a new food pellet, ensuring it doesn't spawn on the given snake body."""
    # Renamed from spawn_food and parameterized
    while True:
        food_x = round(random.randrange(0, screen_w - block_s) / float(block_s)) * block_s
        food_y = round(random.randrange(0, screen_h - block_s) / float(block_s)) * block_s
        
        is_on_snake = False
        for segment in current_snake_body_list: # Use passed parameter
            if segment[0] == food_x and segment[1] == food_y:
                is_on_snake = True
                break
        if not is_on_snake:
            return [food_x, food_y]

# --- End of Core Logic Functions ---

def draw_grid():
    """Draws a grid on the game screen."""
    for x in range(0, screen_width, snake_block_size):
        pygame.draw.line(screen, grid_color, (x, 0), (x, screen_height))
    for y in range(0, screen_height, snake_block_size):
        pygame.draw.line(screen, grid_color, (0, y), (screen_width, y))

# Global game state variables (can be manipulated by tests by importing snake_game)
# These are initialized here and then re-initialized at the start of each game_loop_function call
snake_x = screen_width / 2
snake_y = screen_height / 2
snake_body = [[snake_x, snake_y]] # This global snake_body will be used by spawn_food_logic if not careful
snake_direction = "RIGHT"
# food_pos is initialized using spawn_food_logic, ensuring it uses the initial snake_body
food_pos = spawn_food_logic(snake_body, screen_width, screen_height, snake_block_size) 
score = 0

def draw_snake(snake_body_list):
    """Draws the snake on the screen."""
    for segment in snake_body_list:
        pygame.draw.rect(screen, green, [segment[0], segment[1], snake_block_size, snake_block_size])

def draw_food(position):
    """Draws the food on the screen."""
    pygame.draw.rect(screen, red, [position[0], position[1], food_block_size, food_block_size])


# Global variables to be reset or managed by game_loop
# snake_x, snake_y, snake_body, snake_direction are already global by assignment at top level
# food_pos is also global
# score is global

def game_loop_function():
    """Main function to run the game logic for one session."""
    # Declare globals that will be modified and need to persist or be reset
    global snake_x, snake_y, snake_body, snake_direction, food_pos, score
    global running # Outer loop control

    # Declare and reset global game state variables at the start of each game loop
    global snake_x, snake_y, snake_body, snake_direction, food_pos, score, running

    snake_x = screen_width / 2
    snake_y = screen_height / 2
    snake_body = [[snake_x, snake_y]] # New list for each game session
    snake_direction = "RIGHT"
    score = 0
    # food_pos is initialized using the current (just reset) snake_body
    food_pos = spawn_food_logic(snake_body, screen_width, screen_height, snake_block_size)
    
    game_session_active = True

    while game_session_active:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False # Signal outer loop to terminate
                game_session_active = False # Exit current game session
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and snake_direction != "RIGHT":
                    snake_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and snake_direction != "LEFT":
                    snake_direction = "RIGHT"
                elif event.key == pygame.K_UP and snake_direction != "DOWN":
                    snake_direction = "UP"
                elif event.key == pygame.K_DOWN and snake_direction != "UP":
                    snake_direction = "DOWN"
        
        if not running: # If QUIT was pressed
            break

        # Update snake head position using the new core logic function
        snake_x, snake_y = update_snake_head_logic(
            snake_x, snake_y, snake_direction, snake_block_size
        )
        new_head = [snake_x, snake_y]

        # Game Over conditions using new core logic functions
        # Pass snake_body (which is the body *before* new_head is added) for self-collision check
        if check_wall_collision_logic(new_head[0], new_head[1], screen_width, screen_height) or \
           check_self_collision_logic(new_head, snake_body): 
            game_session_active = False 
            # Score is already up-to-date globally if this was the last action
            break
        
        # Add new head to snake body
        snake_body.insert(0, new_head) # snake_body is the global one here

        # Food consumption
        if new_head[0] == food_pos[0] and new_head[1] == food_pos[1]:
            score += 10 # score is global
            # food_pos is global, updated by spawn_food_logic using the current global snake_body
            food_pos = spawn_food_logic(snake_body, screen_width, screen_height, snake_block_size)
        else:
            snake_body.pop() # snake_body is global

        # Drawing
        screen.fill(black)
        draw_grid() # Draw the grid first
        draw_snake(snake_body)
        draw_food(food_pos)
        display_score(score) 
        pygame.display.flip()

        clock.tick(snake_speed)

# Main application loop
running = True
while running:
    game_loop_function() # Start/Restart the game

    if not running: # If QUIT event was handled in game_loop_function (e.g. window closed)
        break

    # Game Over screen (shown when game_loop_function ends unless running is False)
    screen.fill(black) 
    message("Game Over!", red, y_displace=-50, font=game_over_font)
    message("Your Score: " + str(score), (255,255,0), y_displace=20, font=score_font) 
    message("Press C-Play Again or Q-Quit", (200,200,200), y_displace=70, font=font_style)
    pygame.display.flip()

    waiting_for_user_decision = True
    while waiting_for_user_decision:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                waiting_for_user_decision = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                    waiting_for_user_decision = False
                if event.key == pygame.K_c:
                    waiting_for_user_decision = False 
                    # The outer 'while running:' loop will call game_loop_function() again.

if __name__ == "__main__":
    # Main application loop
    running = True
    while running:
        game_loop_function() # Start/Restart the game

        if not running: # If QUIT event was handled in game_loop_function (e.g. window closed)
            break

        # Game Over screen (shown when game_loop_function ends unless running is False)
        screen.fill(black) 
        message("Game Over!", red, y_displace=-50, font=game_over_font)
        message("Your Score: " + str(score), (255,255,0), y_displace=20, font=score_font) 
        message("Press C-Play Again or Q-Quit", (200,200,200), y_displace=70, font=font_style)
        pygame.display.flip()

        waiting_for_user_decision = True
        while waiting_for_user_decision:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_user_decision = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False
                        waiting_for_user_decision = False
                    if event.key == pygame.K_c:
                        waiting_for_user_decision = False 
                        # The outer 'while running:' loop will call game_loop_function() again.
        
    # Quit Pygame
    pygame.quit()
    quit()
