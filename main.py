#flappy bird folder script 
import pygame
import random
import sys


# Initialize Pygame
pygame.init()

# Define constants for screen size
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 1500
FPS = 60

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# Load images
bird_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/bird.png').convert_alpha()
bird_img = pygame.transform.scale(bird_img, (100, 100))
background_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/background.png')
background_img = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
base_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/base.png').convert_alpha()
base_img = pygame.transform.scale(base_img, (SCREEN_WIDTH, 150))
pipe_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/pipe.png').convert_alpha()
heart_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/heart.png').convert_alpha()
heart_img = pygame.transform.scale(heart_img, (50, 50))
message_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/message.png').convert_alpha()
message_img = pygame.transform.scale(message_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
game_over_img = pygame.image.load('/storage/emulated/0/flappybird/gallery/sprites/game_over.png').convert_alpha()

# Load sound effects
jump_sound = pygame.mixer.Sound('/storage/emulated/0/flappybird/gallery/audio/wing.wav')
hit_sound = pygame.mixer.Sound('/storage/emulated/0/flappybird/gallery/audio/hit.wav')
point_sound = pygame.mixer.Sound('/storage/emulated/0/flappybird/gallery/audio/point.wav')
die_sound = pygame.mixer.Sound('/storage/emulated/0/flappybird/gallery/audio/die.wav')
heart_sound = pygame.mixer.Sound('/storage/emulated/0/flappybird/gallery/audio/heart.wav')  # Add a sound for the heart

# Load number sprites for the score
numbers = [pygame.image.load(f'/storage/emulated/0/flappybird/gallery/sprites/{i}.png').convert_alpha() for i in range(10)]
# Scale the numbers to make them smaller and uniform in size
numbers = [pygame.transform.scale(num, (30, 50)) for num in numbers]  # Resize each number to 30x50

# Bird class
class Bird:
    def __init__(self):
        self.x = 200
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.gravity = 0.7
        self.lift = -12
        self.width = 80
        self.height = 80
        self.immortal = False
        self.immortal_timer = 0

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity
        if self.y >= SCREEN_HEIGHT - base_img.get_height() - self.height:
            self.y = SCREEN_HEIGHT - base_img.get_height() - self.height
            self.velocity = 0
        if self.y <= 0:
            self.y = 0

        # Handle immortality timer
        if self.immortal and pygame.time.get_ticks() > self.immortal_timer:
            self.immortal = False

    def jump(self):
        self.velocity = self.lift
        jump_sound.play()

    def draw(self):
        screen.blit(bird_img, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, heart_available_time):
        self.x = SCREEN_WIDTH
        self.gap = 300
        self.width = 120
        self.top_height = random.randint(100, SCREEN_HEIGHT - base_img.get_height() - self.gap - 200)
        self.bottom_height = SCREEN_HEIGHT - base_img.get_height() - self.top_height - self.gap
        self.passed = False
        self.heart_added = False
        self.heart_y = None

        # Set the heart availability time (only after 40 seconds)
        if pygame.time.get_ticks() >= heart_available_time:
            self.heart_added = True
            self.heart_y = self.top_height + self.gap // 2 - 25  # Place the heart in the middle of the gap

    def update(self):
        self.x -= 6

    def draw(self):
        # Draw top pipe
        top_pipe = pygame.transform.rotate(pipe_img, 180)
        screen.blit(top_pipe, (self.x, self.top_height - top_pipe.get_height()))
        # Draw bottom pipe
        screen.blit(pipe_img, (self.x, SCREEN_HEIGHT - base_img.get_height() - self.bottom_height))
        # Draw heart (if applicable)
        if self.heart_added:
            screen.blit(heart_img, (self.x + self.width // 2 - heart_img.get_width() // 2, self.heart_y))

# Collision detection
def check_collision(bird, pipes):
    if bird.y >= SCREEN_HEIGHT - base_img.get_height() - bird.height:
        return True
    for pipe in pipes:
        if pipe.x < bird.x + bird.width and pipe.x + pipe.width > bird.x:
            if not bird.immortal:
                # Check if bird hits the top or bottom pipes
                if bird.y < pipe.top_height or bird.y + bird.height > SCREEN_HEIGHT - base_img.get_height() - pipe.bottom_height:
                    return True
    return False

# Check for heart collection
def check_heart_collection(bird, pipes):
    for pipe in pipes:
        if pipe.heart_added and pipe.x < bird.x + bird.width and pipe.x + pipe.width > bird.x:
            # Check if bird intersects with the heart
            heart_rect = pygame.Rect(
                pipe.x + pipe.width // 2 - heart_img.get_width() // 2,
                pipe.heart_y,
                heart_img.get_width(),
                heart_img.get_height()
            )
            bird_rect = pygame.Rect(bird.x, bird.y, bird.width, bird.height)
            if bird_rect.colliderect(heart_rect):
                pipe.heart_added = False
                heart_sound.play()
                bird.immortal = True
                bird.immortal_timer = pygame.time.get_ticks() + 5000  # 10 seconds of immortality

# Update score
def check_score(bird, pipes, score):
    for pipe in pipes:
        if not pipe.passed and pipe.x + pipe.width < bird.x:
            pipe.passed = True
            point_sound.play()
            return score + 1
    return score

# Draw score
def draw_score(score):
    score_str = str(score)
    x_pos = SCREEN_WIDTH // 2 - (len(score_str) * 15) // 2  # Adjusting the center position for smaller numbers
    for digit in score_str:
        screen.blit(numbers[int(digit)], (x_pos, 20))
        x_pos += 35  # Adjust spacing between digits to fit smaller numbers

# Game loop
def game_loop():
    bird = Bird()
    pipes = []
    score = 0
    base_x = 0
    pipe_frequency = 1500
    last_pipe_time = pygame.time.get_ticks()
    last_heart_time = pygame.time.get_ticks()
    heart_available_time = last_heart_time + 15000 # First heart will appear after 30 seconds
    game_started = False

    while True:
        screen.fill((0, 0, 0))
        screen.blit(background_img, (0, 0))
        screen.blit(base_img, (base_x, SCREEN_HEIGHT - base_img.get_height()))
        screen.blit(base_img, (base_x + SCREEN_WIDTH, SCREEN_HEIGHT - base_img.get_height()))

        # Scroll base
        base_x -= 6
        if base_x <= -SCREEN_WIDTH:
            base_x = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not game_started:
                    game_started = True
                else:
                    bird.jump()

        if not game_started:
            screen.blit(message_img, (0, 0))
            pygame.display.update()
            clock.tick(FPS)
            continue

        # Update bird
        bird.update()

        # Add new pipes and set heart availability after 15 seconds
        if pygame.time.get_ticks() - last_pipe_time > pipe_frequency:
            pipes.append(Pipe(heart_available_time))
            last_pipe_time = pygame.time.get_ticks()
            
        # Update and remove pipes
        for pipe in pipes[:]:
            pipe.update()
            if pipe.x + pipe.width < 0:
                pipes.remove(pipe)
                
                # Check if 15 seconds have passed since the last heart was spawned
        if pygame.time.get_ticks() - last_heart_time >= 15000:  # 15 seconds passed
            heart_available_time = pygame.time.get_ticks() + 15000  # Schedule the next heart
            last_heart_time = pygame.time.get_ticks()  # Update the last heart spawn time

        # Check collisions
        if check_collision(bird, pipes):
            if not bird.immortal:
                hit_sound.play()
                die_sound.play()
                screen.blit(game_over_img, (SCREEN_WIDTH // 2 - game_over_img.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_img.get_height() // 2))
                pygame.display.update()
                pygame.time.wait(2000)
                return game_loop()

        # Check for heart collection
        check_heart_collection(bird, pipes)

        # Update score
        score = check_score(bird, pipes, score)

        # Draw everything
        bird.draw()
        for pipe in pipes:
            pipe.draw()
        draw_score(score)

        # Update the display
        pygame.display.update()
        clock.tick(FPS)

# Start game
game_loop()
