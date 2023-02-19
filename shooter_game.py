from pygame import *
from random import *
from time import time as timer

lost = 0
score = 0


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, lenght_x, lenght_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (lenght_x, lenght_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x < 620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('note.png', self.rect.centerx, self.rect.top, -15, 15, 20)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 720)
            lost += 1

class Ast(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 720)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


bullets = sprite.Group()

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -50, randint(1, 3), 80, 50)
    monsters.add(monster)

window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

mixer.init()
mixer.music.load('requiem.mp3')
mixer.music.play()
shot = mixer.Sound('fire.ogg')

font.init()
font1 = font.SysFont('Times New Roman', 36)
font2 = font.SysFont('Times New Roman', 72)

player = Player('mozart.png', 5, 400, 10, 80, 100)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Ast('asteroid.png', randint(30, 670), -50, randint(1, 2), 80, 50)
    asteroids.add(asteroid)

lives = 5
rel_time = False
num_fire = 0


clock = time.Clock()
FPS = 60
finish = False
game = True
while game:
    for e in event.get():
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 10 and rel_time == False:
                    num_fire += 1
                    player.fire()
                    shot.play()
                if num_fire >= 10 and rel_time == False:
                    timer1 = timer()
                    rel_time = True
        if e.type == QUIT:
            game = False
    if not finish:
        window.blit(background, (0, 0))
        text_lose = font1.render('Пропущено:' + str(lost), 1, (255, 255, 255))
        text_win = font1.render('Счет:' + str(score), 1, (255, 255, 255))
        text_lives = font1.render('Жизней:' + str(lives), 1, (255, 255, 0))
        window.blit(text_lose, (10, 50))
        window.blit(text_win, (10, 20))
        window.blit(text_lives, (500, 20))
        player.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        player.reset()
        monsters.draw(window)
        bullets.draw(window)
        asteroids.draw(window)
        if rel_time == True:
            timer2 = timer()
            if timer2 - timer1 < 3:
                text_reload = font1.render('Перезарядка...', 1, (255, 0, 0))
                window.blit(text_reload, (250, 400))
            else:
                num_fire = 0
                rel_time = False
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for s in sprites_list:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -50, randint(1, 3), 80, 50)
            monsters.add(monster)
        if lives <= 0 or lost >= 10:
            finish = True
            lose_game = font2.render('YOU LOSE', 1, (255, 0, 0))
            window.blit(lose_game, (200, 200))
        if  sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, asteroids, True)
            lives -= 1
        if score >= 30:
            finish = True
            win_game = font2.render('YOU WIN', 1, (0, 185, 0))
            window.blit(win_game, (200, 200))
        display.update()
    clock.tick(FPS)