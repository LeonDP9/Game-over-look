#Создай собственный Шутер!

from pygame import *
from random import *
from time import time as timer

lost = 0 #счётчик
points = 0 #очки

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, size_1 = 65, size_2 = 65):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_1, size_2))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and self.rect.x < win_width - 65:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.x, self.rect.y, 10, 10, 40)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > win_height:
            self.rect.x = randint(0, win_width - 65)
            self.rect.y = 0
            global lost 
            lost += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

player = Player('rocket.png', 285, 400, 10)

win_width = 700
win_height = 500

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy('ufo.png', randint(0, win_width - 65), -65, randint(1, 5), 65, 40)
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy('asteroid.png', randint(30, win_width - 30), -40, 80, 50, randint(1, 7))
    asteroids.add(asteroid)

bullets = sprite.Group()

window = display.set_mode((win_width, win_height))
display.set_caption('Шутер')
background = transform.scale(image.load('galaxy.jpg'), (win_width, win_height))

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

time = time.Clock()

run = True
finish = False
rel_fire = False
num_fire = 0

font.init()
font1 = font.SysFont('Arial', 36)

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                    if num_fire < 5 and rel_fire == False:
                        num_fire = num_fire + 1
                        player.fire()
                        fire_sound.play()
                    if num_fire >= 5 and rel_fire == False:
                        last_time = timer()
                        rel_fire = True
    if finish != True:
        window.blit(background, (0, 0))
        player.update()
        monsters.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.update()
        bullets.draw(window)
        if rel_fire == True:
            now_time = timer()
            if now_time - last_time <= 3:
                reload = Font2.render('Wait reload', 1, (150, 0, 0))
                window.blit(reload, 260, 460)
            else:
                num_fire = 0
                real_fire = False
        sprite_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in range(len(sprite_list)):
            monster = Enemy('ufo.png', randint(0, win_width - 65), -65, randint(1, 5), 65, 40)
            monsters.add(monster)
            points += 1
        if points >= 10:
            finish = True
            text_win = font1.render('YOU WIN!', True, (255, 255, 255))
            window.blit(text_win, (280, 200))
        if lost > 3 or sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            finish = True
            text_lose = font1.render('YOU LOSE!', True, (255, 255, 255))
            window.blit(text_lose, (280, 200))
        text_lose = font1.render('Пропущено: ' + str(lost), 1, (255, 255, 255))
        text_point = font1.render('Счёт: ' + str(points), 1, (255, 255, 255))
        window.blit(text_lose, (20, 50))
        window.blit(text_point, (20, 20))

    display.update()
else:
    finish = False
    points = 0
    lost = 0
    num_fire = 0
    time.tick(40)