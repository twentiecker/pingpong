import pygame
from pygame.locals import *
import random
from pygame.sprite import Sprite, Group, spritecollide, groupcollide
import time

class GameSprite(Sprite):
    def __init__(self, image_path, image_size, x, y, speed_x, speed_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image_path), image_size)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self, image_path, image_size, x, y, speed_x, speed_y):
        super().__init__(image_path, image_size, x, y, speed_x, speed_y)
        self.score = 0
        self.stunned_until = 0
        self.fired_bullet = False  # Track if a bullet has been fired

    def l_update(self):
        # Check if player is stunned
        if pygame.time.get_ticks() < self.stunned_until:
            return  # Skip movement if player is stunned

        keys = pygame.key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed_y
        if keys[K_s] and self.rect.y < window_size[1] - self.image.get_height():
            self.rect.y += self.speed_y

    def r_update(self):
        # Check if player is stunned
        if pygame.time.get_ticks() < self.stunned_until:
            return  # Skip movement if player is stunned

        keys = pygame.key.get_pressed()
        if keys[K_UP] and self.rect.y > 0:
            self.rect.y -= self.speed_y
        if keys[K_DOWN] and self.rect.y < window_size[1] - self.image.get_height():
            self.rect.y += self.speed_y

    def update(self):
        global inactive
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        if self.rect.x < 0 and score_l == end_score:
            inactive = True
            window.blit(r_win, r_win.get_rect(center=(window_size[0]/2, window_size[1]/2)))
        elif self.rect.x > window_size[0] - self.image.get_width() and score_r == end_score:
            inactive = True
            window.blit(l_win, l_win.get_rect(center=(window_size[0]/2, window_size[1]/2)))

        if self.rect.y > window_size[1] - self.image.get_height() or self.rect.y < 0:
            self.speed_y *= -1

        if self.rect.colliderect(l_racket.rect) or self.rect.colliderect(r_racket.rect):
            self.speed_x *= -1

    def fire(self, direction):
        if direction == "l" and not self.fired_bullet:
            bullets.add(Bullet("bullet.png", bullet_size, self.rect.x + self.rect.width, self.rect.y + self.rect.height/2-10,10,0))
            self.fired_bullet = True  # Mark that the bullet has been fired
        if direction == "r" and not self.fired_bullet:
            print(f"Peluru pemain kanan dibuat di posisi: {self.rect.x}, {self.rect.y}")
            bullets.add(Bullet("bullet.png", bullet_size, self.rect.x, self.rect.y + self.rect.height/2-10,-10,0))
            self.fired_bullet = True

class Bullet(GameSprite):
    def __init__(self, image_path, image_size, x, y, speed_x, speed_y):
        super().__init__(image_path, image_size, x, y, speed_x, speed_y)

    def update(self):
        super().update()
        global l_bullet, r_bullet
        if self.rect.x > window_size[0]:
            self.kill()
            l_racket.fired_bullet = False  # Reset bullet firing for left player
        elif self.rect.x < 0:
            self.kill()
            r_racket.fired_bullet = False  # Reset bullet firing for right player

# Initialization
pygame.init()
back = (200, 255, 255)  # Background color
window_size = (600, 500)  # (width, height)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('"Ping-Pong"ahh game')

clock = pygame.time.Clock()
FPS = 60

# Font
text_color = (255, 255, 0)
font = pygame.font.Font(None, 70)
l_win = font.render('LEFT PLAYER WINS', True, text_color)
r_win = font.render('RIGHT PLAYER WINS', True, text_color)
font1 = pygame.font.Font(None, 32)

# Sprites
racket_size = (50, 150)
ball_size = (50, 50)
bullet_size = (40,40)
l_racket = Player('racket.png', racket_size, 30, 200, 0, 5)
r_racket = Player('racket.png', racket_size, 520, 200, 0, 5)
ball = Player('tenis_ball.png', ball_size, 275, 225, 4, 4)

bullets = Group()

# Initialize scores
score_l = 0
score_r = 0
end_score = 35
stun_duration = 1500

# Game Loop
game = True
inactive = False
while game:
    for e in pygame.event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_d:
                l_racket.fire("l")

            if e.key == K_LEFT:
                r_racket.fire("r")

    if not inactive:
        window.fill(back)
        
        # Update game objects
        l_racket.l_update()
        r_racket.r_update()
        ball.update()
        bullets.update()

        # Check if player is hit by bullet
        if spritecollide(l_racket, bullets, True):
            l_racket.stunned_until = pygame.time.get_ticks() + stun_duration
            r_racket.fired_bullet = False  # Reset bullet firing for right player


        if spritecollide(r_racket, bullets, True):
            r_racket.stunned_until = pygame.time.get_ticks() + stun_duration
            l_racket.fired_bullet = False  # Reset bullet firing for left player

        # Check collisions
        if ball.rect.x < 0:
            score_r += 1
            ball.rect.x = window_size[0] / 2
            ball.rect.y = window_size[1] / 2
            ball.speed_x *= -1
            if score_r >= end_score:
                inactive = True
                window.blit(r_win, r_win.get_rect(center=(window_size[0] / 2, window_size[1] / 2)))
        elif ball.rect.x > window_size[0] - ball.image.get_width():
            score_l += 1
            ball.rect.x = window_size[0] / 2
            ball.rect.y = window_size[1] / 2
            ball.speed_x *= -1
            if score_l >= end_score:
                inactive = True
                window.blit(l_win, l_win.get_rect(center=(window_size[0] / 2, window_size[1] / 2)))
        
        # Draw game objects
        l_racket.draw(window)
        r_racket.draw(window)
        ball.draw(window)
        bullets.draw(window)
        
        # Score display
        score_left = font1.render(f'Left Player Score: {score_l}', True, text_color)
        score_right = font1.render(f'Right Player Score: {score_r}', True, text_color)
        window.blit(score_left, (10, 10))
        window.blit(score_right, (window_size[0] - 240, 10))
    
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
