from pygame import *
clock = time.Clock()
window  = display.set_mode((700,500))
display.set_caption('Догонялки')

mixer.init()
mixer.music.load('jungles.ogg')
mixer.music.play()
#задай фон сцены
background = transform.scale(image.load('background.jpg'),(700,500))
game = True
FPS = 60
win_width = 700
win_height = 500
class GameSprite():
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))




class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width -80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed

class Enemy(GameSprite):
    direction = 'left'
    def update(self):
        if self.rect.x <= 470:
            self.direction = 'right'
        if self.rect.x >= 615:
            self.direction = 'left'
        
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed
    
class Wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3, wall_x,wall_y,wall_wight,wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_wight
        self.height = wall_height
        self.image = Surface((self.width,self.height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

wall1 = Wall(0,0,0,150,150,10,270)
wall2 = Wall(0,0,0,150,20,10,130)
wall3 = Wall(0,0,0,150,20,325,10)
wall4 = Wall(0,0,0,255,150,10,130)
wall8 = Wall(0,0,0,255,280,10,200)
wall5 = Wall(0,0,0,255,480,200,10)
wall6 = Wall(0,0,0,445,180,10,300)
wall7 = Wall(0,0,0,350,50,10,350)

player = Player("hero.png", 50, 300, 4)
kiborg = Enemy('cyborg.png', 550, 200, 2)
final = GameSprite('treasure.png', 500, 400, 2)

font.init()
font = font.Font(None, 70)
win = font.render(  'YOU WIN!', True, (255,215,0))
lose = font.render(  'YOU LOSE!', True, (255,215,0))
finish = False

start_ticks = time.get_ticks()
full_time = 20


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:
        seconds = round((time.get_ticks()-start_ticks)/1000,0)


        window.blit(background,(0,0))
        wall1.draw_wall()
        wall2.draw_wall()
        wall3.draw_wall()
        wall4.draw_wall()
        wall5.draw_wall()
        wall6.draw_wall()
        wall7.draw_wall()
        wall8.draw_wall()

        player.update()
        kiborg.update()
        
        
        player.reset()
        kiborg.reset()
        final.reset()

    #"Проигрыш"
    if sprite.collide_rect(player, kiborg)  or sprite.collide_rect(player, wall1) or sprite.collide_rect(player, wall3) or sprite.collide_rect(player, wall4): 
        finish = True
        window.blit(lose, (200, 200))
        #kick.play()

    #Ля ты победил
    if sprite.collide_rect(player, final):
        finish = True
        window.blit(win,(200,200))
        #money.play()

    time_timer = full_time - seconds
    if time_timer == 0:
        finish = True
        window.blit(lose, (200, 200))

    time_label = font.render(str(time_timer), True, (255,255,255))
    window.blit(time_label, (10, 10))

    display.update()
    clock.tick(FPS)