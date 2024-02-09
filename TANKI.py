import pygame
from pygame.locals import *
import os
import time
import sys
from random import*

SCREEN_WIDTH = 844
SCREEN_HEIGHT = 800
screen_width=844
screen_height=800
playerX=350
playerY=680

pygame.init()
game_screen=pygame.display.set_mode((screen_width, screen_height))
game_over_screen=pygame.display.set_mode((screen_width, screen_height))
set_screen=pygame.display.set_mode((screen_width, screen_height))
screen=pygame.display.set_mode((screen_width, screen_height))

enem_tanks=[]
bullets_tank=[]
bullets_enem=[]
Massiv_enemy=[]
blocks=[]
platforms = []

over=False
flag_sh=False
minus=False
Block_kill=False
shooting=True
shooting_en=False
RIGHT=LEFT=UP=DOWN=True
running=True
the_end=False

time=10000
pygame.time.set_timer(pygame.USEREVENT, time)

player_up=pygame.image.load("player.png").convert_alpha()
player_down=pygame.image.load("player_down.png").convert_alpha()
player_right=pygame.image.load("player_right.png").convert_alpha()
player_left=pygame.image.load("player_left.png").convert_alpha()
enemy= pygame.image.load("enemy1_down.png").convert_alpha()
enemy_right=pygame.image.load("enemy1_right.png").convert_alpha()
enemy_left=pygame.image.load("enemy1_left.png").convert_alpha()
enemy_up=pygame.image.load("enemy1.png").convert_alpha()
ammo = pygame.image.load("ammo.png")
flag=pygame.image.load("flag.png")
flag_rect=flag.get_rect(center=(350, 750))

surf_flag = pygame.Surface((50, 50))
surf_flag_rect=surf_flag.get_rect(center=(350, 750))

entities = pygame.sprite.Group() # Все объекты

way=1
kolvo_tankov=20
lives=3
kol=0
MOVE_SPEED=6

level=['             ',
       ' - - - - - - ',
       ' - - - - - - ',
       ' - - - - - - ',
       ' - - - - - - ',
       ' - -     - - ',
       '     - -     ',
       '- --     -- -',
       '     - -     ',
       ' - - - - - - ',
       ' - - - - - - ',
       ' - - - - - - ',
       ' - - --- - - ',
       '             ',
       ' ---     --- ',
       '             ',
       ' - -     - - ',]

CLOCK = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('opensans', 75)
bg = pygame.Surface((1346, 1600))
rect=bg.get_rect(center=(0, 0))
rect_acc=pygame.draw.rect(game_screen, (128, 128, 128), (700, 0, 210, 800))

white=(255, 255, 255)
black=(0, 0, 0)
gray=(50, 50, 50)
red=(255, 0, 0)
green=(0, 255, 0)
blue=(0, 0, 255)
yellow=(255, 255, 0)
ryellow=(28, 28, 28)
PLATFORM_WIDTH = 47
PLATFORM_HEIGHT = 47
PLATFORM_COLOR = "#FF6262"
font = "DAYPBL__.ttf"
FPS=20

def text_format(message, textFont, textSize, textColor):
    newFont=pygame.font.Font(textFont, textSize)
    newText=newFont.render(message, 0, textColor)
    return newText

class Game_Over():
    def __init__(self, title, width, height):
        self.title = title
        self.width = screen_width
        self.height = screen_height
        set_screen = pygame.display.set_mode((width, height))
        set_screen.fill((44, 51, 55))
        pygame.display.set_caption(title)
        pygame.display.update()
        CLOCK.tick(FPS)
        pygame.display.set_caption("GAME OVER")
        real_time=0

    def the_end(self):
        global lives
        global kolvo_tankov
        global flag_sh
        global over
        game_over_screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("GAME OVER")
        wof=""
        selected="main menu"
        X=0
        Y=0

        main_img1=pygame.image.load("font0.png")
        place_main1=main_img1.get_rect(topleft=(0, 0))

        while 1:
            if lives==0 and kolvo_tankov!=0 or flag_sh:
                wof="You failed."
                X=290
                Y=260
                over=True
            elif lives!=0 and kolvo_tankov==0:
                wof="Congratulations! You won."
                X=90
                Y=260
                over=True
            elif not flag_sh:
                wof="You failed."
                X=290
                Y=260
                over=True
            game_over_screen.blit(main_img1, place_main1)
            text_game_over=text_format("Game Over", font, 80, yellow)
            text_count=text_format(wof, font, 45, yellow)
            game_over_screen.blit(text_game_over, (180, 100))
            game_over_screen.blit(text_count, (X, Y))
            for i in pygame.event.get():
                if i.type==pygame.QUIT:
                    pygame.init()
                    pygame.quit()
                    quit()
                if i.type==pygame.KEYDOWN:
                    if i.key==pygame.K_UP:
                            selected="main menu"
                    elif i.key==pygame.K_DOWN:
                            selected="quit"

                    if i.key==pygame.K_RETURN:
                        if selected=="main menu":
                            pygame.init()
                            main_menu()
                            pygame.quit()
                            quit()
                        if selected=="quit":
                            pygame.quit()
                            quit()

            if selected=="main menu":
                text_men=text_format("MAIN MENU", font, 50, yellow)
            else:
                text_men = text_format("MAIN MENU", font, 50, white)

            if selected=="quit":
                text_quit=text_format("QUIT", font, 50, yellow)
            else:
                text_quit=text_format("QUIT", font, 50, white)

            game_screen.blit(text_men, (280, 460))
            game_screen.blit(text_quit, (350, 500))
            pygame.display.update()
            CLOCK.tick(FPS)


class Game:
    def __init__(self, title, width, height):
        self.title = title
        self.width = screen_width
        self.height = screen_height
        game_screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        pygame.display.update()
        CLOCK.tick(FPS)
        pygame.display.set_caption("TANKS")

    def game_start(self):
        game_over=False
        while not game_over:
            main()
            for i in pygame.event.get():
                if i.type==pygame.QUIT:
                    pygame.init()
                    pygame.quit()
                    quit()


class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("BR.png")
        self.image.set_colorkey((255, 255, 255))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

BrickX=[]
BrickY=[]
bullets_of_player = pygame.sprite.Group()
bullets_of_enemies = pygame.sprite.Group()
bullets_of_flag = pygame.sprite.Group()

way_for_bullet="none"

class Bullet(pygame.sprite.Sprite):
    def __init__(self, xB, yB, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image=surf
        self.image.set_colorkey((255, 255, 255))
        self.rect=self.image.get_rect(center=(xB, yB))
        self.add(group)
        self.speed=10

    def update(self, who):
        if self.rect.x<=670 and self.rect.x>=0 and self.rect.y<=800 and self.rect.y>=0:
            if who=="pl":
                self.collide_pl()
                self.go_player_bullet()
                self.over()

            if who=="en":
                self.collide_en()
                self.go_enemy_bullet()
                self.over()

            if who=="fl":
                self.flag_shoot()
                self.collide_fl()
                self.over()
        else:
            self.kill()

    def over(self):
        global over
        if over:
            self.kill()

    def go_enemy_bullet(self):
            if enemm.image==enemy_left:
                    self.rect.x-=self.speed
            elif enemm.image==enemy_right:
                    self.rect.x+=self.speed
            elif enemm.image==enemy_up:
                    self.rect.y-=self.speed
            elif enemm.image==enemy:
                    self.rect.y+=self.speed

    def flag_shoot(self):
        self.rect.x-=self.speed

    def go_player_bullet(self):
        if player.image==player_left:
                self.rect.x-=self.speed
        elif player.image==player_right:
                self.rect.x+=self.speed
        elif player.image==player_up:
                self.rect.y-=self.speed
        elif player.image==player_down:
                self.rect.y+=self.speed

    def collide_pl(self):
        global kolvo_tankov
        global over
        for p in blocks:
            if pygame.sprite.collide_rect(self, p):
                Block_kill=True
                entities.remove(p)
                blocks.remove(p)
                self.kill()

        for e in group_of_enemies:
            if pygame.sprite.collide_rect(self, e):
                group_of_enemies.remove(e)
                kolvo_tankov-=1
                self.kill()
        if kolvo_tankov==0:
            over=True
            game_over= Game_Over('TANKS', screen_width, screen_height)
            game_over.the_end()

    def collide_en(self):
        global lives
        global playerX
        global playerY
        global over
        for e in blocks:
                if pygame.sprite.collide_rect(self, e):
                    self.kill()
        if pygame.sprite.collide_rect(self, player):
            self.kill()
            lives-=1
            playerX=350
            playerY=680

        if lives==0:
            over=True
            game_over= Game_Over('TANKS', screen_width, screen_height)
            game_over.the_end()

    def collide_fl(self):
        global flag
        global over
        if surf_flag_rect.contains(self):
            self.kill()
            game_over=True
            flag_sh=True
            over=True
            game_over= Game_Over('TANKS', screen_width, screen_height)
            game_over.the_end()




group_of_enemies = pygame.sprite.Group()
enemyX=32
enemyY=32

class Enemies(pygame.sprite.Sprite):
    def __init__(self, x, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image=surf
        self.image.set_colorkey((255, 255, 255))
        self.rect=self.image.get_rect(center=(enemyX, enemyY))
        self.add(group)
        enem_tanks.append(self.rect)
        self.speed=3

    def update(self):
        rr=rl=True
        self.collide()
        if self.rect.y<282:
            self.image=enemy
            self.image.set_colorkey((255, 255, 255))
            self.rect.y+=self.speed
        if self.rect.y>=282 and self.rect.x<225:
            self.image=enemy_right
            self.image.set_colorkey((255, 255, 255))
            self.rect.x+=self.speed

        if self.rect.x>=225 and self.rect.y<330:
            self.image=enemy
            self.image.set_colorkey((255, 255, 255))
            self.rect.y+=self.speed
        elif self.rect.y>=330 and self.rect.x<417:
            self.image=enemy_right
            self.image.set_colorkey((255, 255, 255))
            self.rect.x+=self.speed
        elif self.rect.x>=417 and self.rect.y<725:
            self.image=enemy
            self.image.set_colorkey((255, 255, 255))
            self.rect.y+=self.speed
        if self.rect.y>=725 and self.rect.x>350:
            self.image=enemy_left
            self.image.set_colorkey((255, 255, 255))
            self.shoot_flag()

    def collide(self):
        global lives
        global playerX
        global playerY
        if pygame.sprite.collide_rect(self, player): # если есть пересечение платформы с игроком
            minus=True
            lives-=1
            playerX=350
            playerY=680
            self.kill()
        if lives==0:
            game_over= Game_Over('TANKS', screen_width, screen_height)
            game_over.the_end()

    def shoot(self):
        bullet_en=Bullet(self.rect.centerx, self.rect.centery, ammo, bullets_of_enemies)
        bullet_en.update("en")

    def shoot_flag(self):
        bullet_fl=Bullet(self.rect.centerx, self.rect.centery, ammo, bullets_of_flag)
        bullet_fl.update("fl")

enemm=Enemies(randint(50, 600), enemy, group_of_enemies)


class UserTank(pygame.sprite.Sprite):
    xtank=0
    ytank=0
    MOVE_SPEED=6
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = player_up
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(playerX, playerY))

    def move(self, left, right, up, down, blocks):

        if up:
            self.image.set_colorkey((255, 255, 255))
            self.image = player_up
            way_for_bullet="up"
            shooting=False
            if (self.rect.centery>=32):
                self.ytank = -MOVE_SPEED

        if down:
            self.image.set_colorkey((255, 255, 255))
            self.image = player_down
            way_for_bullet="down"
            shooting=False
            if (self.rect.centery<=783):
                self.ytank = MOVE_SPEED # Лево = x- n

        if left:
            self.image.set_colorkey((255, 255, 255))
            self.image = player_left
            way_for_bullet="left"
            shooting=False
            if (self.rect.centerx>=32):
                self.xtank = -MOVE_SPEED

        if right:
            self.image.set_colorkey((255, 255, 255))
            self.image = player_right
            way_for_bullet="right"
            shooting=False
            if (self.rect.centerx<=615):
                self.xtank = MOVE_SPEED

        if not(left or right): # стоим, когда нет указаний идти
            self.xtank = 0
        if not(up or down): # стоим, когда нет указаний идти
            self.ytank = 0

        self.rect.y += self.ytank
        self.collide(0, self.ytank, blocks)

        self.rect.x += self.xtank
        self.collide(self.xtank, 0, blocks)

    def collide(self, xtank, ytank, blocks):
        for p in blocks:
            if pygame.sprite.collide_rect(self, p): # если есть пересечение платформы с игроком

                if xtank > 0:                      # если движется вправо
                    self.rect.right = p.rect.left # то не движется вправо

                if xtank < 0:                      # если движется влево
                    self.rect.left = p.rect.right # то не движется влево

                if ytank > 0:
                    self.rect.bottom = p.rect.top


                if ytank < 0:                      # если движется вверх
                    self.rect.top = p.rect.bottom # то не движется вверх

    def shoot(self):
        bullet=Bullet(self.rect.centerx, self.rect.centery, ammo, bullets_of_player)
        bullet.update("pl")

player = UserTank()
def game():
    global kolvo_tankov
    global lives
    pygame.init()
    game_over=False
    pygame.display.set_caption("TANKS")
    ground=pygame.image.load("main_play.png")
    place_ground=ground.get_rect(topleft=(0, 0))
    kolX=[]
    kolY=[]
    kol=0
    prov=1
    left = right = False # по умолчанию - стоим
    up = False
    down=False
    x=y=0 # координаты
    br=Block(x, y)

    for row in level: # вся строка
        for col in row: # каждый символ
            x += PLATFORM_WIDTH
            if col == "-":
                kol+=1
                BrickX.append(x)
                BrickY.append(y)
                br=Block(x, y)
                entities.add(br)
                blocks.append(br)
             #блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT    #то же самое и с высотой
        x = 0
    total_level_width  = len(level[0])*PLATFORM_WIDTH # Высчитываем фактическую ширину уровня
    total_level_height = len(level)*PLATFORM_HEIGHT

##  ENEMIES на платформе
    pX=614
    pY=50
    enem_pl=pygame.image.load("enemy2.png")
    enem_pl.set_colorkey((255, 255, 255))
    lives=3

    while 1 and not game_over:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                sys.exit()
                pygame.init()
                pygame.quit()
                quit()
            if i.type == KEYDOWN and i.key == K_UP:
                up = True
            if i.type == KEYDOWN and i.key == K_LEFT:
                left = True
            if i.type == KEYDOWN and i.key == K_RIGHT:
                right = True
            if i.type == KEYDOWN and i.key == K_DOWN:
                down = True
            if i.type == KEYUP and i.key == K_UP:
                up = False
            if i.type == KEYUP and i.key == K_RIGHT:
                right = False
            if i.type == KEYUP and i.key == K_LEFT:
                left = False
            if i.type == KEYUP and i.key == K_DOWN:
                down = False
            elif i.type==pygame.KEYDOWN:
                if i.key==pygame.K_SPACE:
                    shooting=True
                    player.shoot()
            ##ПРИ НАЖАТИИ НА ПРОБЕЛ СТРЕЛЯЕТ
            elif i.type == pygame.USEREVENT:
                enemm=Enemies(randint(50, 600), enemy, group_of_enemies)
                Massiv_enemy.append(enemm)

        player.move(left, right, up, down, blocks)
##      Стреляет enemy
        for k in Massiv_enemy:
            if k.rect.x==player.rect.x or k.rect.y==player.rect.y:
                k.shoot()
        game_screen.blit(ground, place_ground)
        rect_acc=pygame.draw.rect(game_screen, (128, 128, 128), (700, 0, 200, 800))
        blick=pygame.image.load("grey1.png")
        place_blick=blick.get_rect(topleft=(670, 0))
        game_screen.blit(blick, place_blick)
        pygame.time.delay(20)
        bg.fill((0, 0, 0))

##ПРОРИСОВКА объектов на серой панели
        pl_en=enem_pl.get_rect(center=(750, 160))
        game_screen.blit(enem_pl, pl_en)
        text_kolv1=text_format("There are ", font, 25, yellow)
        text_kolv2=text_format(str(kolvo_tankov), font, 25, red)
        text_kolv2_2=text_format(" tanks", font, 25, yellow)
        text_kolv3=text_format("to  kill ", font, 25, yellow)
        game_screen.blit(text_kolv1, (690, 30))
        game_screen.blit(text_kolv2, (695, 60))
        game_screen.blit(text_kolv2_2, (730, 60))
        game_screen.blit(text_kolv3, (695, 90))
        text_life1=text_format("You have ", font, 25, yellow)
        text_life2=text_format(str(lives), font, 25, red)
        text_life3=text_format(" lives ", font, 25, yellow)
        game_screen.blit(text_life1, (690, 280))
        game_screen.blit(text_life2, (750, 310))
        game_screen.blit(text_life3, (716, 340))

##ПРОРИСОВКА ВРАГОВ В ИГРЕ
##        game_screen.blit(bg, rect)
        game_screen.blit(player.image, player.rect)
        game_screen.blit(surf_flag, surf_flag_rect)
        game_screen.blit(flag, flag_rect)
        group_of_enemies.draw(game_screen)
        group_of_enemies.update()

##ПРОРИСОВКА ПУЛИ
        bullets_of_player.draw(game_screen)
        bullets_of_player.update("pl")
        bullets_of_enemies.draw(game_screen)
        bullets_of_enemies.update("en")
        bullets_of_flag.draw(game_screen)
        bullets_of_flag.update("fl")

##ПРОРИСОВККА кирпичных панелей
        for e in entities:
            screen.blit(e.image, e.rect)
        pygame.display.update()

##Если минус=True, количество жизней уменьшается на 1
        if minus:
            lives-=1
        if lives==0 or kolvo_tankov==0:
                game_over
    if game_over:
        the_end=True

def main():

    global kolvo_tankov
    global lives
    global blocks
    global group_of_enemies
    global bullets_of_enemies
    global bullets_of_player
    global bullets_of_flag
    global playerX
    global playerY
    global flag_sh
    global over

    for a in group_of_enemies:
        a.kill()
        group_of_enemies.remove(a)
    for b in bullets_of_enemies:
        b.kill()
        bullets_of_enemies.remove(b)
    for c in bullets_of_player:
        c.kill()
        bullets_of_player.remove(c)
    for d in bullets_of_flag:
        d.kill()
        bullets_of_flag.remove(d)

    kolvo_tankov=20
    lives=3
    playerX=350
    playerY=680
    flag_sh=False
    over=False

    if not the_end:
        game()
    else:
        Game_Over()

class Setting:
    def __init__(self, title, width, height):
        self.title = title
        self.width = screen_width
        self.height = screen_height
        set_screen = pygame.display.set_mode((width, height))
        set_screen.fill((44, 51, 55))
        pygame.display.set_caption(title)
        pygame.display.update()
        CLOCK.tick(FPS)
        pygame.display.set_caption("SETTINGS")
        real_time=0

    def nastroyki(self):
        global time
        sett=True
        selected_set="medium"
        the_time=10
        real_time=the_time
        main_img1=pygame.image.load("font0.png")
        place_main1=main_img1.get_rect(topleft=(0, 0))
        while sett:
            for i in pygame.event.get():
                if i.type==pygame.QUIT:
                    pygame.init()
                    main_menu()
                    pygame.quit()
                    quit()
                if i.type==pygame.KEYDOWN:
                    if selected_set=="easy":
                         if i.key==pygame.K_DOWN:
                            selected_set="medium"
                    elif selected_set =="medium":
                        if i.key==pygame.K_DOWN:
                            selected_set="hard"
                        elif i.key==pygame.K_UP:
                            selected_set="easy"
                    elif selected_set == "hard":
                        if i.key==pygame.K_UP:
                            selected_set="medium"
                    if i.key==pygame.K_RETURN:
                        if selected_set=="easy":
                            time=15000
                            pygame.init()
                            main_menu()
                            pygame.quit()
                            quit()
                        if selected_set=="medium":
                            time=10000
                            pygame.init()
                            main_menu()
                            pygame.quit()
                            quit()
                        if selected_set=="hard":
                            the_time=5000
                            pygame.init()
                            main_menu()
                            pygame.quit()
                            quit()
            set_screen.fill((44, 51, 55))
            title=text_format("SETTINGS", font, 90, yellow)
            title_under=text_format("SETTINGS", font, 93, (204, 168, 23))

            if selected_set=="easy":
                text_easy=text_format("EASY", font, 75, yellow)
            else:
                text_easy = text_format("EASY", font, 75, white)

            if selected_set=="medium":
                text_medium=text_format("MEDIUM", font, 75, yellow)
            else:
                text_medium = text_format("MEDIUM", font, 75, white)

            if selected_set=="hard":
                text_hard=text_format("HARD", font, 75, yellow)
            else:
                text_hard = text_format("HARD", font, 75, white)
            title_rect1=title.get_rect()
            undertitle_rect=title_under.get_rect()
            easy_rect=text_easy.get_rect()
            medium_rect=text_medium.get_rect()
            hard_rect=text_hard.get_rect()
            main_img1.set_colorkey((255, 255, 255))
            screen.blit(main_img1, place_main1)
            instruction=text_format("Choose the difficulty of the level", font, 20, yellow)
            place=instruction.get_rect(center=(400, 550))
            set_screen.blit(title_under, (screen_width/2 - (undertitle_rect[2]/2), 80))
            set_screen.blit(title, (screen_width/2 - (title_rect1[2]/2), 80))
            set_screen.blit(text_easy, (screen_width/2 - (easy_rect[2]/2), 300))
            set_screen.blit(text_medium, (screen_width/2-(medium_rect[2]/2), 360))
            set_screen.blit(text_hard, (screen_width/2 - (hard_rect[2]/2), 420))
            set_screen.blit(instruction, place)
            pygame.display.update()
            CLOCK.tick(FPS)
            pygame.display.set_caption("Settings")

def main_menu():
    menu=True
    selected="start"

    main_img1=pygame.image.load("font0.png")
    place_main1=main_img1.get_rect(topleft=(0, 0))

    while menu:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                quit()
            if event.type==pygame.KEYDOWN:
                if selected=="start":
                    if event.key==pygame.K_DOWN:
                        selected="settings"
                elif selected =="settings":
                    if event.key==pygame.K_DOWN:
                            selected="quit"
                    elif event.key==pygame.K_UP:
                            selected="start"
                elif selected == "quit":
                    if event.key==pygame.K_UP:
                            selected="settings"
                if event.key==pygame.K_RETURN:
                    if selected=="start":
                        game = Game('TANKS', screen_width, screen_height)
                        game.game_start()
                        main()
                    if selected=="settings":
                        game1= Setting('TANKS', screen_width, screen_height)
                        game1.nastroyki()
                    if selected=="quit":
                        pygame.quit()
                        quit()
        screen.fill((44, 51, 55))
        title=text_format("TANKS", font, 92, yellow)
        title_under=text_format("TANKS", font, 95, (204, 168, 23))

        main_img1.set_colorkey((255, 255, 255))
        screen.blit(main_img1, place_main1)

        if selected=="start":
            text_start=text_format("START", font, 75, yellow)
        else:
            text_start = text_format("START", font, 75, white)

        if selected=="settings":
            text_settings=text_format("SETTINGS", font, 75, yellow)
        else:
            text_settings = text_format("SETTINGS", font, 75, white)

        if selected=="quit":
            text_quit=text_format("EXIT", font, 75, yellow)
        else:
            text_quit = text_format("EXIT", font, 75, white)

        title_rect=title.get_rect()
        undertitle_rect=title_under.get_rect()
        start_rect=text_start.get_rect()
        setting_rect=text_settings.get_rect()
        quit_rect=text_quit.get_rect()
        screen.blit(title_under, (screen_width/2 - (undertitle_rect[2]/2), 80))
        screen.blit(title, (screen_width/2 - (title_rect[2]/2), 80))
        screen.blit(text_start, (screen_width/2 - (start_rect[2]/2), 300))
        screen.blit(text_settings, (screen_width/2-(setting_rect[2]/2), 360))
        screen.blit(text_quit, (screen_width/2 - (quit_rect[2]/2), 420))
        pygame.display.update()
        CLOCK.tick(FPS)
        pygame.display.set_caption("TANKS")

if __name__ == "__main__":
    pygame.init()
    main_menu()
    pygame.quit()
    quit()


