from tkinter import RIGHT
import pygame
import os
pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shooter Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
MAX_BULLETS = 3
BULLET_VEL = 7
CHARACTER_WIDTH, CHARACTER_HEIGHT = 80, 82

BLUE_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

BLUE_CHARACTER_IMAGE_LEFT = pygame.image.load(os.path.join('Assets', 'Gunner_Blue_Left.png'))
BLUE_CHARACTER_IMAGE_RIGHT = pygame.image.load(os.path.join('Assets', 'Gunner_Blue_Right.png'))
# The next line can be used to resize and rotate the image by 90 degrees:
#BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_CHARACTER_IMAGE, (CHARACTER_WIDTH, CHARACTER_HEIGHT)), 90)
RED_CHARACTER_IMAGE_LEFT = pygame.image.load(os.path.join('Assets', 'Gunner_Red_Left.png'))
RED_CHARACTER_IMAGE_RIGHT = pygame.image.load(os.path.join('Assets', 'Gunner_Red_Right.png'))

BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.jpg')), (WIDTH, HEIGHT))

def draw_window(blue, red, blueBullets, redBullets, blueHealth, redHealth, blue_direction, red_direction):
#    WIN.fill(WHITE)
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    blue_health_text = HEALTH_FONT.render("Health: "+str(blueHealth), 1, WHITE)
    red_health_text = HEALTH_FONT.render("Health: "+str(redHealth), 1, WHITE)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(blue_health_text, (10, 10))
    if blue_direction == 'right':
        WIN.blit(BLUE_CHARACTER_IMAGE_RIGHT, (blue.x, blue.y))
    else:
        WIN.blit(BLUE_CHARACTER_IMAGE_LEFT, (blue.x, blue.y))
    if red_direction == 'right':
        WIN.blit(RED_CHARACTER_IMAGE_RIGHT, (red.x, red.y))
    else:
        WIN.blit(RED_CHARACTER_IMAGE_LEFT, (red.x, red.y))

    for bullet in blueBullets:
        pygame.draw.rect(WIN, BLUE, bullet[0])

    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet[0])

    pygame.display.update()

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_a] and blue.x - VEL > 0: # LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_d] and blue.x + VEL + blue.width < WIDTH: # RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_w] and blue.y - VEL > 0: # UP
        blue.y -= VEL
    if keys_pressed[pygame.K_s] and blue.y + VEL + blue.height < HEIGHT: # DOWN
        blue.y += VEL 

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0: # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT: # DOWN
        red.y += VEL

def handle_bullets(blueBullets, redBullets, blue, red):
    for bullet in blueBullets:
        if bullet[1] == 'right':
            bullet[0].x += BULLET_VEL
        else:
            bullet[0].x -= BULLET_VEL
        if red.colliderect(bullet[0]):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blueBullets.remove(bullet)
        elif bullet[0].x > WIDTH or bullet[0].x + bullet[0].width < 0:
            blueBullets.remove(bullet)

    for bullet in redBullets:
        if bullet[1] == 'right':
            bullet[0].x += BULLET_VEL
        else:
            bullet[0].x -= BULLET_VEL
        if blue.colliderect(bullet[0]):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            redBullets.remove(bullet)
        elif bullet[0].x > WIDTH or bullet[0].x + bullet[0].width < 0:
            redBullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    blue = pygame.Rect(100, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)
    red = pygame.Rect(700, 300, CHARACTER_WIDTH, CHARACTER_HEIGHT)

    blueBullets = []
    redBullets = []

    blueHealth = 10
    redHealth = 10

    blue_direction = 'right'
    red_direction = 'left'

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    blue_direction = 'left'
                
                if event.key == pygame.K_d:
                    blue_direction = 'right'

                if event.key == pygame.K_LCTRL and len(blueBullets) < MAX_BULLETS:
                    if blue_direction == 'right':
                        bullet = pygame.Rect(blue.x+blue.width-2, blue.y + blue.height//3 + 6, 10, 5)
                    else:
                        bullet = pygame.Rect(blue.x+2, blue.y + blue.height//3 + 6, 10, 5)
                    blueBullets.append([bullet, blue_direction])
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(redBullets) < MAX_BULLETS:
                    if red_direction == 'left':
                        bullet = pygame.Rect(red.x+2, red.y + red.height//3 + 6, 10, 5)
                    else:
                        bullet = pygame.Rect(red.x+red.width-2, red.y + red.height//3 + 6, 10, 5)
                    redBullets.append([bullet, red_direction])
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_a:
                    blue_direction = 'left'
                
                if event.key == pygame.K_d:
                    blue_direction = 'right'

                if event.key == pygame.K_RIGHT:
                    red_direction = 'right'
                
                if event.key == pygame.K_LEFT:
                    red_direction = 'left'

            if event.type == RED_HIT:
                redHealth -= 1
                BULLET_HIT_SOUND.play()

            if event.type == BLUE_HIT:
                blueHealth -= 1
                BULLET_HIT_SOUND.play()
        
        winner_text = ""
        if redHealth <=0:
            winner_text = "Blue Wins!"

        if blueHealth <= 0:
            winner_text = "Red Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break
        
        keys_pressed  = pygame.key.get_pressed()
        blue_handle_movement(keys_pressed, blue)
        red_handle_movement(keys_pressed, red)

        handle_bullets(blueBullets, redBullets, blue, red)

        draw_window(blue, red, blueBullets, redBullets, blueHealth, redHealth, blue_direction, red_direction)
    
    main()

if __name__ == "__main__":
    main()