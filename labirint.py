from pygame import *
import pygame

win_width = 700
win_height = 500
display.set_caption('A Light Behind the Maze')
window = display.set_mode((win_width, win_height))
bgcolor = (0, 0, 0)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_x_speed, player_y_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.x_speed = player_x_speed
        self.y_speed = player_y_speed
    def update(self):
        self.rect.x += self.x_speed
        platforms_touched = [w for w in walls if self.rect.colliderect(w.rect)]
        for p in platforms_touched:
            if self.x_speed > 0:
                self.rect.right = p.rect.left
            elif self.x_speed < 0:
                self.rect.left = p.rect.right
        self.rect.x = max(0, min(self.rect.x, win_width - self.rect.width))
        self.rect.y += self.y_speed
        platforms_touched = [w for w in walls if self.rect.colliderect(w.rect)]
        for p in platforms_touched:
            if self.y_speed > 0:
                self.rect.bottom = p.rect.top
            elif self.y_speed < 0:
                self.rect.top = p.rect.bottom
        self.rect.y = max(0, min(self.rect.y, win_height - self.rect.height))
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.right, self.rect.centery, 40, 35, 15)
        bullets.add(bullet)

class Wall:
    def __init__(self, rect_width, rect_height, rect_x, rect_y, color):
        self.x = rect_x
        self.y = rect_y
        self.width = rect_width
        self.height = rect_height
        self.color = color
        self.rect = Rect(self.x, self.y, self.width, self.height)
    def draw(self):
        pygame.draw.rect(window, self.color, self.rect)

class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
        self.side = 'left'
    def update(self):
        if self.rect.x <= 420:
            self.side = 'right'
        if self.rect.x >= win_width - self.rect.width:
            self.side = 'left'
        if self.side == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__(player_image, player_x, player_y, size_x, size_y)
        self.speed = player_speed
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > win_width:
            self.kill()

COLOR_RECT = (255, 255, 255)
w1 = Wall(300, 30, 100, 200, COLOR_RECT)
w2 = Wall(30, 400, 400, 100, COLOR_RECT)
w3 = Wall(300, 30, 0, 350, COLOR_RECT)

walls = [w1, w2, w3]
hero = Player('You.png', 5, win_height - 80, 95, 90, 0 , 0)

hero_right = transform.scale(image.load('You.png'), (95, 90))
hero_left = transform.flip(hero_right, True, False)
hero_facing_right = True

bullets = sprite.Group()
monsters = sprite.Group()
monster1 = Enemy('Enemy.png', win_width - 80, 150, 80, 80, 5)
monster2 = Enemy('Enemy.png', win_width - 80, 280, 80, 80, 5)
monsters.add(monster1, monster2)
final_sprite = GameSprite('light.png', win_width - 85, win_height - 70, 80, 70)

finish = False
run = True

while run:
    time.delay(50)
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_a or e.key == K_LEFT:
                hero.x_speed = -10
                hero_facing_right = False
            elif e.key == K_d or e.key == K_RIGHT:
                hero.x_speed = 10
                hero_facing_right = True
            elif e.key == K_w or e.key == K_UP:
                hero.y_speed = -10
            elif e.key == K_s or e.key == K_DOWN:
                hero.y_speed = 10
            elif e.key == K_SPACE:
                hero.fire()
        elif e.type == KEYUP:
            if e.key in (K_a, K_d, K_LEFT, K_RIGHT):
                hero.x_speed = 0
            if e.key in (K_w, K_s, K_UP, K_DOWN):
                hero.y_speed = 0
    if not finish:
        window.fill(bgcolor)
        hero.update()                
        bullets.update()
        monsters.update()
        sprite.groupcollide(monsters, bullets, True, True)
        sprite.groupcollide(bullets, sprite.Group(), True, True)
        for bullet in bullets:
            for wall in walls:
                if bullet.rect.colliderect(wall.rect):
                    bullet.kill()
                    break
        if hero_facing_right:
                hero.image = hero_right
        else:
                hero.image = hero_left
        
        hero.reset()
        bullets.draw(window)
        w1.draw()
        w2.draw()
        w3.draw()
        final_sprite.reset()
        monsters.draw(window)
        if sprite.spritecollide(hero, monsters, False):
            finish = True
            img = image.load('Ending1.jpg')
            d = img.get_width() / img.get_height()
            window.fill((255, 255, 255))
            window.blit(transform.scale(img, (int(win_height * d), win_height)), (-95, 5))
        elif sprite.collide_rect(hero, final_sprite):
            finish = True
            img = image.load('Ending2.jpg')
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
    display.update()
