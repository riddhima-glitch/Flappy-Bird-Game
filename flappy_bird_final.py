import pygame
import random
import pygame_gui 



pygame.init()


SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Image Flappy Clone with GUI")


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (46, 178, 46) 
RED = (255, 0, 0) 


GRAVITY = 0.5 
FLAP_STRENGTH = -10 
PIPE_SPEED = 3 
GAP_HEIGHT = 180 


game_over = False
score = 0
font = pygame.font.Font(None, 48)


clock = pygame.time.Clock()
FPS = 60


try:
    bird_img_raw = pygame.image.load('bird.png').convert_alpha()
    pipe_img_raw = pygame.image.load('pipe.png').convert_alpha()
    background_img_raw = pygame.image.load('background.png').convert() # Background doesn't need alpha
    

    BIRD_WIDTH, BIRD_HEIGHT = 60, 50
    bird_image = pygame.transform.scale(bird_img_raw, (BIRD_WIDTH, BIRD_HEIGHT))
    
    PIPE_WIDTH = 70
    pipe_image = pygame.transform.scale(pipe_img_raw, (PIPE_WIDTH, pipe_img_raw.get_height())) # Scale width, maintain aspect ratio roughly
    
    
    background_image = pygame.transform.scale(background_img_raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

except pygame.error as e:
    print(f"Error loading image: {e}")
    print("Please ensure 'bird.png', 'pipe.png', and 'background.png' are in the same folder as the script.")
    pygame.quit()
    exit

GROUND_HEIGHT = 100
ground_rect = pygame.Rect(0, SCREEN_HEIGHT - GROUND_HEIGHT, SCREEN_WIDTH, GROUND_HEIGHT)



ui_manager = pygame_gui.UIManager((SCREEN_WIDTH, SCREEN_HEIGHT))
restart_button = None 




class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        
        self.image = bird_image
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT // 2)
        self.velocity = 0

    def flap(self):
        """Makes the bird jump up."""
        self.velocity = FLAP_STRENGTH

    def update(self):
        """Applies gravity and updates the bird's position."""
        
        self.velocity += GRAVITY
        
        self.rect.y += self.velocity

        
        if self.velocity > 15:
            self.velocity = 15

    def check_boundary(self):
        """Checks if the bird hits the floor, ceiling, or ground."""
        
        if self.rect.top < 0 or self.rect.bottom > ground_rect.top:
            return True
        return False




class PipePair:
    def __init__(self, top_rect, bottom_rect):
        self.top_pipe_rect = top_rect 
        self.bottom_pipe_rect = bottom_rect 
        self.passed = False 

def create_pipe():
    """Generates a pair of top and bottom pipes with a random gap."""
    
    min_y = GAP_HEIGHT // 2 + 50
    max_y = SCREEN_HEIGHT - GROUND_HEIGHT - GAP_HEIGHT // 2 - 50 
    gap_center_y = random.randint(min_y, max_y)

    
    top_pipe_height = gap_center_y - GAP_HEIGHT // 2
    top_rect = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, top_pipe_height)

    ct
    bottom_pipe_y = gap_center_y + GAP_HEIGHT // 2
    bottom_pipe_height = SCREEN_HEIGHT - GROUND_HEIGHT - bottom_pipe_y 
    bottom_rect = pygame.Rect(SCREEN_WIDTH, bottom_pipe_y, PIPE_WIDTH, bottom_pipe_height)
    
    s
    return PipePair(top_rect, bottom_rect)




def draw_pipes(pipe_pairs):
    """Draws all active pipes using the pipe image."""
    for pair in pipe_pairs:
        
        top_pipe_scaled_img = pygame.transform.scale(pipe_image, (pair.top_pipe_rect.width, pair.top_pipe_rect.height))
        top_pipe_flipped_img = pygame.transform.flip(top_pipe_scaled_img, False, True) # Flip vertically
        screen.blit(top_pipe_flipped_img, pair.top_pipe_rect)

        
        bottom_pipe_scaled_img = pygame.transform.scale(pipe_image, (pair.bottom_pipe_rect.width, pair.bottom_pipe_rect.height))
        screen.blit(bottom_pipe_scaled_img, pair.bottom_pipe_rect)

def move_pipes(pipe_pairs):
    """Moves pipes to the left."""
    for pair in pipe_pairs:
        pair.top_pipe_rect.x -= PIPE_SPEED
        pair.bottom_pipe_rect.x -= PIPE_SPEED

def check_score(bird_rect, pipe_pairs, score):
    """Checks if the bird has passed a pipe and updates the score."""
    for pair in pipe_pairs:
        
        if pair.top_pipe_rect.right < bird_rect.left and not pair.passed:
            pair.passed = True 
            return score + 1.0 
            
    return score

def check_collision(bird, pipe_pairs):
    """Checks if the bird hits any pipe or the ground."""
    bird_rect = bird.rect
    
    if bird_rect.colliderect(ground_rect):
        return True

    
    for pair in pipe_pairs:
        if bird_rect.colliderect(pair.top_pipe_rect) or bird_rect.colliderect(pair.bottom_pipe_rect):
            return True
    return False

def draw_score(score):
    """Renders the current score on the screen."""
    score_text = font.render(f"Score: {int(score)}", True, BLACK)
    screen.blit(score_text, (10, 10))

def show_game_over():
    """Displays the Game Over screen and the Pygame_GUI button."""
    global restart_button 

    
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(150)
    overlay.fill(BLACK)
    screen.blit(overlay, (0, 0))

    
    game_over_text = font.render("GAME OVER", True, RED)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
    screen.blit(game_over_text, text_rect)

    
    final_score_text = font.render(f"Final Score: {int(score)}", True, WHITE)
    score_rect = final_score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(final_score_text, score_rect)

    
    if restart_button is None:
        button_width = 200
        button_height = 50
        button_x = SCREEN_WIDTH // 2 - button_width // 2
        button_y = SCREEN_HEIGHT // 2 + 50
        
        restart_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), (button_width, button_height)),
            text='Restart Game',
            manager=ui_manager
        )

def reset_game():
    """Resets all game state variables and objects."""
    global game_over, score, player_bird, all_sprites, pipe_list, pipe_timer, restart_button
    
    game_over = False
    score = 0
    
    
    player_bird = Bird()
    all_sprites = pygame.sprite.Group(player_bird)
    pipe_list.clear() 
    pipe_timer = 0 
    
    
    if restart_button is not None:
        restart_button.kill()
        restart_button = None




player_bird = Bird()
all_sprites = pygame.sprite.Group(player_bird)
pipe_list = [] 
pipe_timer = 0
PIPE_SPAWN_INTERVAL = 1500 

time_delta = 0 

running = True
while running:
    
    time_delta = clock.tick(FPS) / 1000.0 

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        
        ui_manager.process_events(event)

        if not game_over:
            
            if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1) or \
               (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                player_bird.flap()
        
        
        if event.type == pygame.USEREVENT: 
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == restart_button:
                    reset_game()
                    
        
        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            reset_game()

    if not game_over:
        
        all_sprites.update()

        
        pipe_timer += time_delta * 1000 
        if pipe_timer > PIPE_SPAWN_INTERVAL:
            
            new_pipe_pair = create_pipe() 
            pipe_list.append(new_pipe_pair)
            pipe_timer = 0

        
        move_pipes(pipe_list)
        
        pipe_list = [pair for pair in pipe_list if pair.top_pipe_rect.right > 0] 

        
        
        if player_bird.check_boundary() or check_collision(player_bird, pipe_list):
            game_over = True

    
        score = check_score(player_bird.rect, pipe_list, score)


    

    
    screen.blit(background_image, (0, 0)) 

    
    draw_pipes(pipe_list)


    pygame.draw.rect(screen, GREEN, ground_rect)


    all_sprites.draw(screen)

    
    draw_score(score)

    
    if game_over:
        show_game_over()
        
    
    ui_manager.update(time_delta)
    ui_manager.draw_ui(screen)

    
    pygame.display.flip()


pygame.quit()