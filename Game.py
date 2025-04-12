
import pygame
from pygame import K_ESCAPE
from pygame.display import set_icon, set_caption
from pygame.mixer import Sound

from ScoreFuncs import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1280, 720), pygame.SCALED | pygame.DOUBLEBUF, vsync=1)
clock = pygame.time.Clock()


running = True
gameActive = False
game_just_started = False
dt = 0


go_message_alpha = 255


# -- IMAGES --

background = pygame.image.load(resource_path('assets\\Background.png')).convert()
background = pygame.transform.scale(background, (1280, 720))


ball_image = pygame.image.load(resource_path('assets\\Ball.png')).convert_alpha()
ball_image = pygame.transform.scale(ball_image, (80, 80))

paddle_image = pygame.image.load(resource_path('assets\\PADDLE.png')).convert_alpha()
paddle_image = pygame.transform.scale(paddle_image, (268, 110))

set_icon(background)
set_caption('PING!')

# --- COLORS ---
white = (255, 255, 255)
soft_yellow = (255, 245, 157)
orangebrown = (215, 135, 45)



# -- FONTS --

game_font = pygame.font.SysFont('Comic Sans MS', 40, bold= True)
go_font = pygame.font.SysFont('Comic Sans MS', 60, bold= True)
escape_font = pygame.font.SysFont('Comic Sans MS', 25, italic=True)
coming_soon_font = pygame.font.SysFont('Comic Sans MS', 18, bold= True)
sound_font = pygame.font.SysFont('Comic Sans MS', 18, bold= True, italic=True)


# -- MESSAGES --

start_message = game_font.render('Press SPACE to Start', True, white)
start_message_rect = start_message.get_rect(center=(640, 360))

coming_soon_message = coming_soon_font.render('Leaderboard Coming Soon!', True, white)
coming_soon_message_rect = coming_soon_message.get_rect(center= (5, 2))

go_message = go_font.render('GO!', True, soft_yellow)
go_message_rect = go_message.get_rect(center=(640, 300))
go_message.set_alpha(int(go_message_alpha))






# -- Misc Variables --

flashTimer = 0
flashAlpha = 0
flashDecay = 0
flashActive = False

toggle_mute = False
startDelay = 0.3

fadeAlpha = 0
fadeDirection = 1
fadeSpeed = 350

paddle_score_counter = 0
score_count = 0
max_score = load_max_score()

#--------------------------


# --- LOCATIONS ---
center = (640, 360)
top_left = (0, 0)
top_right = (1280, 0)
bottom_left = (0,719)
bottom_right = (1279, 719)


# --- FLASH ---
flash_surface = pygame.Surface((1280, 720))
flash_surface.fill(white)



# --- BALL ---
ball_pos = pygame.Vector2(645, 356)
ball_radius = 20
ball_velocity = pygame.Vector2(0, -500)
gravity = 800
bounce_force_x = -500
bounce_force = -750
max_y_velocity = 1590




# --- TRAIL ---
trail = []
max_trail = 25
trail_radius = 16



# --- PADDLE ---
paddle_width = 200
paddle_height = 35
paddle_speed = 550
min_paddle_speed = 20
paddle = pygame.Rect(540, 690, paddle_width, paddle_height)
paddle_rect = paddle_image.get_rect(center=(int(paddle.x + 100), int(paddle.y + 10)))

paddle_start_x = paddle.x

paddle_returning = False
paddle_return_timer = 0.3
paddle_return_elapsed = 0



# walls = [
#     pygame.Rect(0, 0, 3, 720),                    # Left
#     pygame.Rect(1277, 0, 3, 720),                 # Right
#     pygame.Rect(0, 0, 1280, 3),                    # Top
#     pygame.Rect(0, 719, 1280, 719)
# ]
# --- ORIGINALLY FOR DEBUG, BUT I LIKE THE BORDERS / EDIT: NVM SHE GOONE :P ---
# for wall in walls:
#     pygame.draw.rect(screen, orangebrown, wall, 2)

# --- GAME LOOP ---

while running:
    dt = clock.tick(165) / 1000
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
                show_go = True
                goAlpha = 255


            elif event.key == pygame.K_ESCAPE:
                flashActive = True
                flashDecay = 1000
                flashAlpha = 255

                game_just_started = True
                gameActive = False

                ball_pos = pygame.Vector2(645, 350)
                ball_velocity = pygame.Vector2(0, -500)
                score_count = 0

                paddle_returning = True
                paddle_return_elapsed = 0
                paddle_start_x = paddle.x

            elif event.key == pygame.K_m:
                toggle_mute = not toggle_mute



    if not gameActive:
        fadeAlpha += fadeDirection * fadeSpeed * dt

        if fadeAlpha >= 255:
            fadeAlpha = 255
            fadeDirection = -1

        elif fadeAlpha <= 0:
            fadeAlpha = 0
            fadeDirection = 1

        start_message.set_alpha(int(fadeAlpha))

        if paddle_returning:
            paddle_return_elapsed += dt
            t = min(paddle_return_elapsed / paddle_return_timer, 1)
            ease_t = t * t * (3 - 2 * t)

            target_x = 540
            paddle.x = paddle_start_x + (target_x - paddle_start_x) * ease_t
            paddle_rect = paddle_image.get_rect(center=(int(paddle.x + 100), int(paddle.y + 10)))

            if t >= 1:
                paddle.x = target_x
                paddle_returning = False


        screen.blit(background, (0, 0))
        screen.blit(coming_soon_message, (5, 2))
        screen.blit(start_message, start_message_rect)
        paddle_returning = True
        screen.blit(paddle_image, paddle_rect)

        if toggle_mute:
            sound_display = sound_font.render("Sound: ON (Press M to toggle)", True, white)
        else:
            sound_display = sound_font.render("Sound: OFF (Press M to toggle)", True, white)

        screen.blit(sound_display, (1000, 5))


        pygame.display.flip()
        dt = clock.tick(144) / 1000
        continue



    if flashTimer >= startDelay:
        game_just_started = False
        flashActive = False
        flashAlpha = 0
        flashTimer = 0


        screen.blit(background, (0, 0))
        score_display = game_font.render(f'Score Count: {score_count}', True, white)
        max_score_display = game_font.render(f'Max Score: {max_score}', True, white)
        reset_display = escape_font.render(f'Press ESC to Reset', True, white)

        screen.blit(reset_display, (1040, 0))
        screen.blit(score_display, (10, 0))
        screen.blit(max_score_display, (10, 40))

        paddle = pygame.Rect(540, 690, paddle_width, paddle_height)
        screen.blit(ball_image, ball_image.get_rect(center=(int(ball_pos.x), int(ball_pos.y))))

        flash_surface.set_alpha(int(flashAlpha))
        screen.blit(flash_surface, (0, 0))

        pygame.display.flip()
        continue



    # --- Ball movement ---
    ball_velocity.y += gravity * dt
    ball_pos += ball_velocity * dt

    ball_rect = ball_image.get_rect(center=(int(ball_pos.x), int(ball_pos.y)))
    ball_hitbox = pygame.Rect(ball_pos.x - 20, ball_pos.y - 20, 34, 34)

    trail.append(ball_pos.copy())

    if len(trail) > max_trail:
        trail.pop(0)


        # --- Bounce off side walls ---
        if ball_pos.x - ball_radius <= 0 or ball_pos.x + ball_radius >= screen.get_width():
            ball_velocity.x *= -1.1
            ball_velocity.y *= 1

            # --- Floor or ceiling ---
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


    # --- Paddle movement ---

    keys = pygame.key.get_pressed()

    if keys[pygame.K_a] and paddle.left > 0:
        paddle.x -= paddle_speed * dt

    if keys[pygame.K_d] and paddle.right < screen.get_width():
        paddle.x += paddle_speed * dt



    # --- Paddle Collision ---
    paddle_rect = paddle_image.get_rect(center=(int(paddle.x + 100), int(paddle.y + 10)))

    if ball_hitbox.colliderect(paddle) and ball_velocity.x > 0:
        ball_velocity.x = bounce_force_x
        ball_velocity.y = ball_velocity.y + 10
        if toggle_mute:
            bounce_sound()

    if ball_hitbox.colliderect(paddle) and ball_velocity.x < 0:
        ball_velocity.x = -bounce_force_x
        ball_velocity.y = ball_velocity.y + 10
        if toggle_mute:
            bounce_sound()

    if ball_hitbox.colliderect(paddle) and ball_velocity.y > 0:
        ball_velocity.y = bounce_force
        if toggle_mute:
            bounce_sound()

        if paddle_speed > 20 and paddle_score_counter < 15:
            paddle_speed -= 20
            paddle_score_counter += 1

        else:
            paddle_speed = min_paddle_speed

        if paddle_score_counter == 15:
            paddle_speed = 450
            paddle_score_counter = 0

        bounce_force *= 1.125

        if abs(bounce_force) > max_y_velocity:
            bounce_force = -max_y_velocity


        offset = (ball_pos.x - paddle.centerx) / (paddle.width / 2)
        ball_velocity.x = offset * 550
        score_count += 1



    # --- Drawing ---
    screen.blit(background, (0, 0))
    score_display = game_font.render(f'Score Count: {score_count}', True, white)
    max_score_display = game_font.render(f'Max Score: {max_score}', True, white)
    reset_display = escape_font.render(f'Press ESC to Reset', True, white)
    screen.blit(reset_display, (1040, 0))
    screen.blit(score_display, (10, 0))
    screen.blit(max_score_display, (10, 40))
    screen.blit(paddle_image, paddle_rect)

    if toggle_mute:
        sound_display = sound_font.render("Sound: ON (Press M to toggle)", True, white)
    else:
        sound_display = sound_font.render("Sound: OFF (Press M to toggle)", True, white)

    screen.blit(sound_display, (1000, 30))



    # --- Ball Trail ---
    for i, pos in enumerate(trail):
        alpha = int(115 * (i / max_trail))
        trail_surface = pygame.Surface((trail_radius * 2, trail_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(trail_surface, (255, 211, 0, alpha), (trail_radius, trail_radius), trail_radius)
        screen.blit(trail_surface, (pos.x - trail_radius, pos.y - trail_radius))

    screen.blit(ball_image, ball_rect)


    # --- Screen Flash ---
    if flashActive:
        flashAlpha -= flashDecay * dt
        if flashAlpha <= 0:
            flashAlpha = 0
            flashActive = False

        flash_surface.set_alpha(int(flashAlpha))
        screen.blit(flash_surface, (0, 0))


    if show_go:
        goAlpha -= 244 * dt
        if goAlpha <= 0:
            goAlpha = 0
            show_go = False
        go_message.set_alpha(int(goAlpha))
        screen.blit(go_message, go_message_rect)


    pygame.display.flip()
pygame.quit()
