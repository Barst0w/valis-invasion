import pygame
import random
import os

pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VALIS Invasion")

# Constant Game Logic Variables
FPS = 144
SHIP_WIDTH, SHIP_HEIGHT = 100, 75
MAX_BULLETS = 30
VEL = 3
BULLET_VEL = 8
BIG_ROCK_VEL = 2
MED_ROCK_VEL = 3.5

# Changing variables
bullet_count = 30

# Fonts
GAME_OVER_FONT = pygame.font.SysFont('comicsans', 100)
BULLET_COUNT_FONT = pygame.font.SysFont('comicsans', 35)

# Image Imports
BLUE_SHIP_IMG = pygame.image.load(os.path.join('assets', 'blue_ship.png')).convert()
BLUE_SHIP = pygame.transform.scale(BLUE_SHIP_IMG, (SHIP_WIDTH, SHIP_HEIGHT))
BLUE_LASER = pygame.image.load(os.path.join('assets', 'blue_laser.png')).convert()
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'space.png')).convert(), (WIDTH, HEIGHT))
EXPLOSION = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'explosion.png')).convert(), (SHIP_WIDTH, SHIP_HEIGHT + 25))
BIG_ROCK = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'big_rock.png')).convert(), (75, 75))
MED_ROCK = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'big_rock.png')).convert(), (25, 25))

# Sound Imports
LASER_SOUND = pygame.mixer.Sound(os.path.join('assets', 'laser_sound.ogg'))
GAME_OVER_SOUND = pygame.mixer.Sound(os.path.join('assets', 'game_over_sound.ogg'))
GAME_MUSIC = pygame.mixer.music.load(os.path.join('assets','game_music.ogg'))

# Userevents
big_rock_event, big_rock_time = pygame.USEREVENT + 1, 3000
med_rock_event1, med_rock_time1 = pygame.USEREVENT + 2, 500
med_rock_event2, med_rock_time2 = pygame.USEREVENT + 3, 1500
is_hit = pygame.USEREVENT + 4
update_time = pygame.USEREVENT + 5

# Timed events
pygame.time.set_timer(big_rock_event, big_rock_time)
pygame.time.set_timer(med_rock_event1, med_rock_time1)
pygame.time.set_timer(med_rock_event2, med_rock_time2)
pygame.time.set_timer(update_time, 1000)

# Display and Update Content
def draw_window(ship, ship_bullets, big_rocks, med_rocks, score, destroyed):
    WIN.blit(SPACE, (0, 0))

    if not destroyed:
        BULLET_COUNT_TEXT = BULLET_COUNT_FONT.render(f"BULLETS: {bullet_count}", 1, (255, 255, 255))
        WIN.blit(BULLET_COUNT_TEXT, (1000, 25))
        WIN.blit(BLUE_SHIP, (ship.x, ship.y))
    else:
        WIN.blit(EXPLOSION, (ship.x, ship.y))
        GAME_OVER_TEXT = GAME_OVER_FONT.render("YOU DIED", 1, (255, 255, 255))
        if score > 60:
            TIME_LASTED = BULLET_COUNT_FONT.render(f"You lasted: {score} minutes", 1, (255, 255, 255))
        else:
            TIME_LASTED = BULLET_COUNT_FONT.render(f"You lasted: {score} seconds", 1, (255, 255, 255))
        WIN.blit(GAME_OVER_TEXT, ((WIDTH / 2) - 164, (HEIGHT / 2) - 34))
        WIN.blit(TIME_LASTED, ((WIDTH / 2) - 125, (HEIGHT / 2) + 34))

    for bullet in ship_bullets:
        WIN.blit(BLUE_LASER, (bullet.x, bullet.y))

    for rock in big_rocks:
        WIN.blit(BIG_ROCK, (rock.x, rock.y))

    for rock in med_rocks:
        WIN.blit(MED_ROCK, (rock.x, rock.y))
    
    pygame.display.update()

def handle_controls(keys_pressed, ship, destroyed):
    if not destroyed:
        if keys_pressed[pygame.K_w] and ship.y - VEL > 0:
            ship.y -= VEL
        if keys_pressed[pygame.K_a] and ship.x - VEL > 0:
            ship.x -= VEL
        if keys_pressed[pygame.K_s] and ship.y + VEL + SHIP_HEIGHT < HEIGHT:
            ship.y += VEL
        if keys_pressed[pygame.K_d] and ship.x + VEL + SHIP_WIDTH < WIDTH:
            ship.x += VEL

def handle_bullets(ship, ship_bullets, big_rocks, med_rocks):
    for bullet in ship_bullets:
        bullet.y -= BULLET_VEL
        for rock in big_rocks:
            if rock.colliderect(bullet):
                bullet.x = -10000
                big_rocks.remove(rock)
        for rock in med_rocks:
            if rock.colliderect(bullet):
                bullet.x = -10000
                med_rocks.remove(rock)


def handle_rocks(big_rocks, med_rocks, ship):
    for rock in big_rocks:
        rock.y += BIG_ROCK_VEL
        if rock.colliderect(ship):
            pygame.event.post(pygame.event.Event(is_hit))
        
    for rock in med_rocks:
        rock.y += MED_ROCK_VEL
        if rock.colliderect(ship):
            pygame.event.post(pygame.event.Event(is_hit))

# Main Game Logic / Loop
def main():
    pygame.mixer.music.play()
    ship = pygame.Rect((WIDTH / 2) - (SHIP_WIDTH / 2), (HEIGHT / 2), SHIP_WIDTH, SHIP_HEIGHT)
    ship_bullets = []
    big_rocks = []
    med_rocks = []
    score = 0

    clock = pygame.time.Clock()
    run = True
    destroyed = False
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if not destroyed:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and len(ship_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(ship.x + ship.width / 2 - 2, ship.y, 5, 10)
                        ship_bullets.append(bullet)
                        LASER_SOUND.play()
                        global bullet_count
                        bullet_count -= 1

                if event.type == big_rock_event:
                    rock1 = pygame.Rect(random.randint(50, 400), 0, 75, 75)
                    rock2 = pygame.Rect(random.randint(550, 800), 0, 75, 75)
                    rock3 = pygame.Rect(random.randint(950, 1150), 0, 75, 75)
                    big_rocks.append(rock1)
                    big_rocks.append(rock2)
                    big_rocks.append(rock3)

                if event.type == med_rock_event1:
                    rock1 = pygame.Rect(random.randint(0, 600), 0, 25, 25)
                    rock2 = pygame.Rect(random.randint(600, 1200), 0, 25, 25)
                    med_rocks.append(rock1)
                    med_rocks.append(rock2)

                if event.type == med_rock_event2:
                    rock1 = pygame.Rect(random.randint(0, 375), 0, 25, 25)
                    rock2 = pygame.Rect(random.randint(425, 775), 0, 25, 25)
                    rock3 = pygame.Rect(random.randint(825, 1200), 0, 25, 25)
                    med_rocks.append(rock1)
                    med_rocks.append(rock2)
                    med_rocks.append(rock3)

                if event.type == update_time:
                    score += 1
            
            if event.type == is_hit:
                destroyed = True
                GAME_OVER_SOUND.play()
                pygame.mixer.music.stop()
        
        keys_pressed = pygame.key.get_pressed()
        handle_controls(keys_pressed, ship, destroyed)
        handle_bullets(ship, ship_bullets, big_rocks, med_rocks)
        handle_rocks(big_rocks, med_rocks, ship)
        draw_window(ship, ship_bullets, big_rocks, med_rocks, score, destroyed)
        

    pygame.quit()

if __name__ == "__main__":
    main()