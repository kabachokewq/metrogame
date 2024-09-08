from pygame import *
from random import randint, random,choice
from time import time as timer
mixer.init()
fire_sound = mixer.Sound("bulletsound.mp3") 




wn = display.set_mode((640*1.5,243*1.5))
clock = time.Clock()
display.set_caption("Шутер")
font.init()
font1 = font.Font(None,36)
background = transform.scale(image.load("metro1.png"),(640*1.5,243*1.5))
background2 = transform.scale(image.load("metro2.png"),(640*1.5,243*1.5))
background3 = transform.scale(image.load("metro3.png"),(640*1.5,243*1.5))
w_e = 320
x_e= 240
enemy_l = []

for i in range(1,10):
    img = image.load(f"en/video_00{i}.png")
    scaled_img = transform.scale(img, (w_e, x_e))
    enemy_l.append(scaled_img)
    enemy_l.append(scaled_img)

enemy2_l = []

for i in range(6,17):
    img = image.load(f"enemy2img/enemy2_0{i}-removebg-preview.png")
    scaled_img = transform.scale(img, (w_e, x_e))
    enemy2_l.append(scaled_img)
    enemy2_l.append(scaled_img)


FPS = 65
class GameSprite(sprite.Sprite):
    def __init__(self,pl_image,pl_x,pl_y,size_x,size_y,pl_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pl_image), (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = pl_x
        self.rect.y = pl_y
        self.speed = pl_speed
        self.size_x = size_x
        self.count=0
    def reset(self):
        wn.blit(self.image,(self.rect.x,self.rect.y))
    def animation(self,list):
                self.count = (self.count + 1) % len(list)  
                wn.blit(list[self.count], (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 63:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < 1000 - self.size_x:
            self.rect.x += self.speed
        if keys[K_w] and self.rect.y > 20:
             self.rect.y -= self.speed*3
    def fire(self):
        bullet = Bullet("abullet.png", self.rect.centerx+42, self.rect.top+20,15,20, 5)
        bullets.add(bullet)

#enemyl = [transform.scale(  image.load(''), (70, 110)),
          #transform.scale(  image.load('pr1.png'), (70, 110)),]

class Enemy(GameSprite):
    
    
    def update(self):
        global lose
        

        self.rect.x += self.speed
        if self.rect.x > 0:
            self.rect.y = -50
            self.rect.x = randint(75,620)
            self.speed = randint(1,5)

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
            self.rect.x += self.speed
            if self.rect.x > 640*1.5:
                self.kill()

            
game = True
num_bul = 6
cur_bul = 0
fire_bul= True
hero = Player("hero.png", 100,150,132,132,5)
enemy1 = Enemy("en/video_001.png", 500,70,140,140,5)
enemy1_kill_img = Enemy("enemy1(2).png", 550,233,130,60,5)

enemy2 = Enemy("enemy2img/enemy2_06-removebg-preview.png", 500,100,100,80,5)
enemy2_kill_img = Enemy("enemy1(2).png", 550,233,130,60,5)
stone = Enemy("stone.png", enemy2.rect.centerx,enemy2.rect.centery,50,50,randint(2,7))



enemy1_show = 1
enemy1_kill = 0
enemy1_hp = 2
enemy2_hp = 2
enemy2_show = 1
enemy2_kill = 0
global last_time
last_time = 0 
hero_hp = 10
heart_x = 910
heart_list = []
for i in range(hero_hp):
    heart = GameSprite("heart.png",heart_x,10,25,25,0 )
    heart_list.append(heart)
    heart_x -=30
     

level1 = 1
level2 = 0

dir_list = [3,-3,2,-2,-4,4]
e2_dir = choice(dir_list)
print(e2_dir)

game_time = 55
start_time = timer()
finish = 0
while game:
    nowgame_time = timer()
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if cur_bul <= num_bul and fire_bul == False:
                    fire_sound.play()
                    hero.fire()
                    cur_bul +=1
                elif  cur_bul >= num_bul and fire_bul == False:
                    fire_bul = True
                    hero.fire()
                    last_time = timer()
    if hero.rect.y < 150:
         hero.rect.y +=5
         
    if level1:
        wn.blit(background,(0,0))
        text_score = font1.render("чАС"+str(game_time - int(nowgame_time - start_time)),1,(255,255,255))
        wn.blit(text_score,(10,20))
        hero.reset()
        hero.update()
        for heart in heart_list:
            heart.reset()
             
        if enemy1_show:
            enemy1.animation(enemy_l)
        if enemy1_kill:
            enemy1_kill_img.reset()
        
        rect_col = Rect(enemy1.rect.centerx+50,enemy1.rect.y,50,250)
        #draw.rect(wn,(34,23,56),rect_col)
        if hero.rect.colliderect(rect_col) and enemy1_show:
            hero_hp -=1
            if heart_list:
                heart_list.pop()
            
            hero.rect.x -=140       
        bullets.draw(wn)
        bullets.update()

        if fire_bul == True:
                now_time = timer()
                if now_time - last_time < 2:
                    reload = font1.render("RELOAD: ", 1,(160,25,2))
                    wn.blit(reload,(250,10))
                else:
                    fire_bul = False
                    cur_bul = 0




        collides_enemy = sprite.spritecollide(enemy1,bullets,True)
        if collides_enemy:
            enemy1_hp -=1
            
        if enemy1_hp <= 0:
            enemy1_kill = 1
            enemy1_show = 0

        if  610 < hero.rect.x   <670:
            level1 = False
            level2 = True
            enemy1_kill = 0
            enemy1_show =0
            enemy2_show =1 
            hero.rect.x = 100
            
    if level2:
        
        wn.blit(background2,(0,0))
        if fire_bul == True:
                now_time = timer()
                if now_time - last_time < 2:
                    reload = font1.render("RELOAD: ", 1,(160,25,2))
                    wn.blit(reload,(250,10))
                else:
                    fire_bul = False
                    cur_bul = 0
        collides_enemy = sprite.spritecollide(enemy2,bullets,True) 
        if collides_enemy:
            enemy2_hp -=1

        if hero.rect.colliderect(stone.rect):
            hero_hp -=1
            stone.rect.x = enemy2.rect.centerx
            stone.rect.y= enemy2.rect.centery
            stone.speed = randint(2,7)
            if heart_list:
                heart_list.pop()
            

        

        text_score = font1.render("чАС"+str(game_time - int(nowgame_time - start_time)),1,(255,255,255))
        wn.blit(text_score,(10,20))
        hero.reset()
        hero.update()
        stone.reset()
        stone.rect.x -= stone.speed
        for heart in heart_list:
             heart.reset()
        if stone.rect.x < 0:
             stone.rect.x = enemy2.rect.centerx
             stone.rect.y= enemy2.rect.centery
             stone.speed = randint(2,7)
        enemy2.rect.y -=e2_dir
        if enemy2.rect.y < 20 or enemy2.rect.y > 300:
             e2_dir = choice(dir_list)

        if enemy2_show:
            enemy2.animation(enemy2_l)
        bullets.draw(wn)
        bullets.update()
        

        if enemy2_hp <= 0:
            enemy2_kill = 1
            enemy2_show = 0
            if 610 < hero.rect.x <670:
                finish = 1
                level2 = 0
        if enemy2_kill:
            enemy2_kill_img.reset()
             
    if hero_hp <=0:
        level1 =0
        leve2 = 0
        wn.blit(background3,(0,0))
        fire_bul = 1
    if game_time - int(nowgame_time - start_time) <=0:
        level1 =0
        leve2 = 0
        wn.blit(background3,(0,0))
        fire_bul = 1
    if finish:
        level2 = 0
        level1  = 0
        wn.blit(background,(0,0))
        fire_bul = 1
    clock.tick(FPS)
    display.update()