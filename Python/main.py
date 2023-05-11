import pygame, sys, random

pygame.init()

# Screen Variables
width = 1280
height = 720

screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

pygame.display.set_caption("Pong")

# Shape Variables
player_paddle = pygame.Rect(width - 20, height / 2 - 50, 10, 100)
opponent_paddle = pygame.Rect(10, height / 2 - 50, 10, 100)
ball = pygame.Rect(width / 2 - 15, height / 2 - 15, 30, 30)

# Color Variables
bg_color = pygame.Color('grey12')
main_color = pygame.Color(255, 255, 255)

# Speed and Score Variables
player_speed = 0
opponent_speed = 600
ball_speed_x = 700
ball_speed_y = 700

player_score = 0
opponent_score = 0

# Game Variables
game_font = pygame.font.Font('Python/BrunoAce-Regular.ttf', 200)

delta = 0

def restart():
    global ball_speed_x, ball_speed_y

    ball_speed_x *= random.choice([-1, 1])
    ball_speed_y *= random.choice([-1, 1])

    ball.x = width / 2 - 60
    ball.y = height / 2 - 60

# Main Game Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_speed += 700
            if event.key == pygame.K_UP:
                player_speed += -700
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_speed += -700
            if event.key == pygame.K_UP:
                player_speed += 700

    # Ball Logic
    ball.x += ball_speed_x * delta
    ball.y += ball_speed_y * delta

    if ball.top <= 0 or ball.bottom >= height:
        ball_speed_y *= -1
    if ball.left <= 0:
        player_score += 1
        restart()
    if ball.right >= width:
        opponent_score += 1
        restart()
    
    if ball.colliderect(player_paddle) or ball.colliderect(opponent_paddle):
        ball_speed_x *= -1
    
    # Player Logic
    player_paddle.y += player_speed * delta

    if player_paddle.top <= 0:
        player_paddle.top = 0
    if player_paddle.bottom >= height:
        player_paddle.bottom = height
    
    # Opponent Logic
    if opponent_paddle.top >= ball.top:
        opponent_paddle.y -= opponent_speed * delta
    if opponent_paddle.bottom <= ball.bottom:
        opponent_paddle.y += opponent_speed * delta

    if opponent_paddle.top <= 0:
        opponent_paddle.top = 0
    if opponent_paddle.bottom >= height:
        opponent_paddle.bottom = height
    
    # Background Color
    screen.fill(bg_color)

    # Draw Shapes
    pygame.draw.aaline(screen, pygame.Color(200, 200, 200), (width / 2, 0), (width / 2, height))
    pygame.draw.rect(screen, main_color, player_paddle)
    pygame.draw.rect(screen, main_color, opponent_paddle)
    pygame.draw.ellipse(screen, main_color, ball)

    # Player Score Text
    player_score_surface = game_font.render(str(player_score), True, main_color)
    player_score_rect = player_score_surface.get_rect(center = ((width / 2) + (width / 4), height / 2))
    screen.blit(player_score_surface, player_score_rect)

    # Opponent Score Text
    opponent_score_surface = game_font.render(str(opponent_score), True, main_color)
    opponent_score_rect = opponent_score_surface.get_rect(center = (width / 4, height / 2))
    screen.blit(opponent_score_surface, opponent_score_rect)

    pygame.display.flip()
    delta = clock.tick(60) / 1000