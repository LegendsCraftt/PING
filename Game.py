
import pygame
from ScoreFuncs import *





pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
gameActive = False
game_just_started = False
dt = 0

flashTimer = 0
flashAlpha = 0
flashDecay = 0
flashActive = False

startDelay = 0.3

fadeAlpha = 0
fadeDirection = 1
fadeSpeed = 350

paddle_score_counter = 0
score_count = 0
max_score = load_max_score()

# Colors
white = (255, 255, 255)
orangebrown = (215, 135, 45)



game_font = pygame.font.SysFont('Comic Sans MS', 40, bold= True)
escape_font = pygame.font.SysFont('Comic Sans MS', 25, italic=True)

background = pygame.image.load(resource_path('assets\\Background.png')).convert()
background = pygame.transform.scale(background, (1280, 720))

flash_surface = pygame.Surface((1280, 720))
flash_surface.fill(white)

ball_image = pygame.image.load(resource_path('assets\\Ball.png')).convert_alpha()
ball_image = pygame.transform.scale(ball_image, (80, 80))



# BALL
ball_pos = pygame.Vector2(645, 356)
ball_radius = 20
ball_velocity = pygame.Vector2(0, 0)
gravity = 800
bounce_force = -750
max_y_velocity = 1580



# PADDLE
paddle_width = 200
paddle_height = 20
paddle = pygame.Rect(540, 680, paddle_width, paddle_height)
paddle_speed = 550



walls = [
    pygame.Rect(0, 0, 3, 720),                    # Left
    pygame.Rect(1277, 0, 3, 720),                 # Right
    pygame.Rect(0, 0, 1280, 3),                    # Top
    pygame.Rect(0, 719, 1280, 719)
]

start_message = game_font.render('Press SPACE to Start', True, white)
start_message_rect = start_message.get_rect(center=(640, 360))

go_message = game_font.render('GO!', True, white)
go_message_rect = go_message.get_rect(center=(640, 300))
go_message.set_alpha(int(fadeAlpha))


while running:
    dt = clock.tick(144) / 1000
    for event in pygame.event.get():



        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not gameActive:
                gameActive = True
                game_just_started = True

                flashActive = True
                flashDecay = 1000
                flashAlpha = 255

                screen.blit(go_message, (640, 300))


        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                flashActive = True
                flashDecay = 1000
                flashAlpha = 255

                game_just_started = True
                gameActive = False

                ball_pos = pygame.Vector2(645, 350)
                score_count = 0
                paddle = pygame.Rect(540, 680, paddle_width, paddle_height)
                ball_velocity = pygame.Vector2(0, 0)





    if not gameActive:
        fadeAlpha += fadeDirection * fadeSpeed * dt

        if fadeAlpha >= 255:
            fadeAlpha = 255
            fadeDirection = -1

        elif fadeAlpha <= 0:
            fadeAlpha = 0
            fadeDirection = 1



        start_message.set_alpha(int(fadeAlpha))

        screen.blit(background, (0, 0))
        screen.blit(start_message, start_message_rect)
        pygame.draw.rect(screen, white, paddle)

        pygame.display.flip()
        dt = clock.tick(144) / 1000
        continue

    if flashTimer >= startDelay:
        game_just_started = False
        flashActive = False
        flashAlpha = 0
        flashTimer = 0

        # Draw one frame to avoid freeze
        screen.blit(background, (0, 0))
        score_display = game_font.render(f'Score Count: {score_count}', True, white)
        max_score_display = game_font.render(f'Max Score: {max_score}', True, white)
        reset_display = escape_font.render(f'Press ESC to Reset', True, white)

        screen.blit(reset_display, (1040, 0))
        screen.blit(score_display, (10, 0))
        screen.blit(max_score_display, (10, 40))

        pygame.draw.rect(screen, white, paddle)
        screen.blit(ball_image, ball_image.get_rect(center=(int(ball_pos.x), int(ball_pos.y))))

        flash_surface.set_alpha(int(flashAlpha))
        screen.blit(flash_surface, (0, 0))

        pygame.display.flip()
        continue



    # --- Paddle movement ---
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and paddle.left > 0:
        paddle.x -= paddle_speed * dt
    if keys[pygame.K_d] and paddle.right < screen.get_width():
        paddle.x += paddle_speed * dt


    # --- Ball movement ---
    ball_velocity.y += gravity * dt
    ball_pos += ball_velocity * dt

    ball_rect = ball_image.get_rect(center=(int(ball_pos.x), int(ball_pos.y)))
    ball_hitbox = pygame.Rect(ball_pos.x - 20, ball_pos.y - 20, 34, 34)

    if ball_hitbox.colliderect(paddle) and ball_velocity.y > 0:
        ball_velocity.y = bounce_force

        if paddle_speed > 20 and paddle_score_counter < 15:
            paddle_speed -= 20
            paddle_score_counter += 1

        else:
            paddle_speed = 20

        if paddle_score_counter == 15:
            paddle_speed = 450
            paddle_score_counter = 0

        bounce_force *= 1.125

        if abs(bounce_force) > max_y_velocity:
            bounce_force = -max_y_velocity

        offset = (ball_pos.x - paddle.centerx) / (paddle.width / 2)
        ball_velocity.x = offset * 550
        score_count += 1



        # Bounce off side walls
    if ball_pos.x - ball_radius <= 0 or ball_pos.x + ball_radius >= screen.get_width():
        ball_velocity.x *= -1.3
        ball_velocity.y *= 0.4



        # Floor or ceiling
    if ball_pos.y + ball_radius >= screen.get_height():
        ball_velocity.y *= -0.7  # bounce off floor with damping
        ball_pos.y = screen.get_height() - ball_radius
        bounce_force = - 750



        if score_count > max_score:
            max_score = score_count
            save_max_score(max_score)
        score_count = 0
        paddle_speed = 500



    if ball_pos.y - ball_radius <= 0:
        ball_velocity.y *= -1
        ball_pos.y = ball_radius



    # --- Drawing ---
    screen.blit(background, (0, 0))
    score_display = game_font.render(f'Score Count: {score_count}', True, white)
    max_score_display = game_font.render(f'Max Score: {max_score}', True, white)
    reset_display = escape_font.render(f'Press ESC to Reset', True, white)
    screen.blit(reset_display, (1040, 0))
    screen.blit(score_display, (10, 0))
    screen.blit(max_score_display, (10, 40))

    # Screen Flash
    if flashActive:
        flashAlpha -= flashDecay * dt
        if flashAlpha <= 0:
            flashAlpha = 0
            flashActive = False

        flash_surface.set_alpha(int(flashAlpha))
        screen.blit(flash_surface, (0, 0))



    pygame.draw.rect(screen, white, paddle)  # white paddle
    screen.blit(ball_image, ball_rect)

    # Original ball
    # pygame.draw.circle(screen, "red", (int(ball_pos.x), int(ball_pos.y)), ball_radius)

    for wall in walls:
        pygame.draw.rect(screen, orangebrown, wall, 2)

    pygame.display.flip()



pygame.quit()
