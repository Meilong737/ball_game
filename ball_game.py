import pygame # load pygame keywords
import sys # let python use file system
import os # help python identify your OS
import time
import csv
'''
Variables
'''
filename="fame.csv"
name=""
GAMEOVER=1import pygame # load pygame keywords
import sys # let python use file system
import os # help python identify your OS
import time
import csv
'''
Variables
'''
filename="fame.csv"
name=""
GAMEOVER=1
ALPHA=(0, 0, 0)
BLUE  = (25, 25, 200)
RED = (255, 0, 0)
BLACK = (23, 23, 23)
PURPLE = (150, 0, 150)
WHITE = (254, 254, 254)
worldx = 1200
worldy = 730
fps   = 50 # frame rate
ani   = 4   # animation cycles
steps=5
ALPHA=(0, 0, 0)
BLUE  = (25, 25, 200)
RED = (255, 0, 0)
BLACK = (23, 23, 23)
PURPLE = (150, 0, 150)
WHITE = (254, 254, 254)
worldx = 1200
worldy = 730
fps   = 50 # frame rate
ani   = 4   # animation cycles
steps=5
'''
Objects
'''
class Player (pygame.sprite.Sprite):
    def __init__ (self, x, y, imgfile="bat.png"):
        (sizex, sizey)=(75,75)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('img',imgfile)).convert()
        img = pygame.transform.scale(img,(sizex, sizey))
        img.convert_alpha()     # optimise alpha
        img.set_colorkey(ALPHA) # set alpha
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.sizey=sizey
        self.sizex=sizex
        self.movex=0
        self.movey=0
        self.score=0
        
    def control(self,x,y):
        self.movex += x
        self.movey += y
        
    def update(self):
        self.rect.x = self.rect.x + self.movex
        self.rect.y = self.rect.y + self.movey
        if self.rect.x < 0:
            self.rect.x =worldx
        if self.rect.x > worldx:
            self.rect.x =0
        collidelist=pygame.sprite.spritecollide(self,ball_list,False)
        for ball in collidelist:
            self.score+=1
            
    def reset(self, lvl):
          self.score=0
          self.movex=0
          self.movey=0
          if lvl==2:
              self.rect.x=600
              self.rect.y=650
class Ball (pygame.sprite.Sprite):
    def __init__ (self, x, y, imgfile="ball.png"):
        (sizex, sizey)=(25,25)
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join('img',imgfile)).convert()
        img = pygame.transform.scale(img,(sizex, sizey))
        img.convert_alpha()     # optimise alpha
        img.set_colorkey(ALPHA) # set alpha
        self.image = img
        self.rect  = self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.sizey=sizey
        self.sizex=sizex
        self.speed=5
        self.movex=self.speed
        self.movey=self.speed
        
    def update(self):
        self.rect.x+=self.movex
        self.rect.y+=self.movey
        if self.rect.x < 0:
            self.movex=-self.movex
        if self.rect.x >worldx:
            self.movex=-self.movex
        if self.rect.y <0:
            self.movey=-self.movey
        if self.rect.y >worldy:
            pygame.event.post(pygame.event.Event(GAMEOVER,{}))
            
        collidelist=pygame.sprite.spritecollide(self,player_list,False)
        for player in collidelist:
            
            self.speed+=1
            self.movey=-self.speed
            if self.movex >0:
                self.movex=self.speed
            else:
                self.movex=-self.speed
    
    def reset(self, lvl):
          
        if lvl==1:
            self.rect.x=600
            self.rect.y=50
            self.speed=5
            self.movex=self.speed
            self.movey=self.speed

'''
Setup
'''
clock = pygame.time.Clock()
pygame.init()
world    = pygame.display.set_mode([worldx,worldy])
player=Player(600, 650)
player_list = pygame.sprite.Group()
player_list.add(player)
ball=Ball(600, 50)
ball_list=pygame.sprite.Group()
ball_list.add(ball)
lvl=1
'''
Game Loop
'''
def playgame(bestscores,name):
    main=True
    player.reset(lvl)
    ball.reset(lvl)

    while main == True:
        for event in pygame.event.get():
            if event.type==GAMEOVER:
                time.sleep(1)
                main=False
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
                main = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left')
                    player.control(-steps,0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right')
                    player.control(steps,0)
                if event.key == ord('q'):
                    savescores(filename,bestscores)
                    pygame.quit()
                    sys.exit()
                    main=False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    print('left stop')
                    player.control(steps,0)
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    print('right stop')
                    player.control(-steps,0)
        world.fill(BLUE)
        player_list.update()
        player_list.draw(world) # draw player
        ball_list.update()
        ball_list.draw(world) # draw player
        largeFont=pygame.font.SysFont("arial",50)
        text=largeFont.render("score: "+str(player.score),1,WHITE)
        world.blit(text,(10,10))
        
        pygame.display.flip()
        clock.tick(fps)
    bestscores=gameover(player.score,bestscores,name)
    return bestscores

def loadscores(name):
    with open (name,'r') as inputstream:
        csvr=csv.reader(inputstream,dialect='excel')
        bestscores=[]
        for (score,name) in csvr :
            bestscores.append((int(score),name))
    return bestscores
    
def savescores(filename,scores):
   with open (filename,'w') as inputstream :
       csvw=csv.writer(inputstream,dialect='excel')
       for row in scores:
           csvw.writerow(row)
           
def gameover(newscore,bestscores,newname):
    main=True
    newpos=len(bestscores)
    for pos,(score,name) in enumerate(bestscores):
        if newscore>score:
            newpos=pos
            break
    bestscores=bestscores[:newpos]+[(newscore,newname)]+bestscores[newpos:]
    while main ==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                main = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    main =False
        world.fill(PURPLE)
        y=50
        largeFont=pygame.font.SysFont("arial",35)
        for (score,name) in bestscores[:5]:
            text=largeFont.render(str(score)+" "+ name,1,WHITE)
            world.blit(text,(500,y))
            y+=50
            
            
        pygame.display.flip()
        clock.tick(fps)    
    return bestscores

def entername():
    main=True
    name=""
    abc=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ']
    while main ==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                main = False
            if event.type == pygame.KEYDOWN:
                main=False
                for ch in abc:
                    if event.key==ord(ch):
                        name+=ch
                        main=True
                        
                    
        world.fill(PURPLE)
        largeFont=pygame.font.SysFont("arial",35)
        text=largeFont.render("enter your name",1,WHITE)
        world.blit(text,(50,50))
        smallFont=pygame.font.SysFont("freemono",30)
        text=smallFont.render(">" +name,0,WHITE)
        world.blit(text,(50,100))
        pygame.display.flip()
        clock.tick(fps)
    return name
def fame():
    main=True
    
    while main ==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                main = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    main =False
        world.fill(PURPLE)
        y=50
        largeFont=pygame.font.SysFont("arial",35)
        for (score,name) in bestscores[:5]:
            text=largeFont.render(str(score)+" "+ name,1,WHITE)
            world.blit(text,(500,y))
            y+=50
        pygame.display.flip()
        clock.tick(fps)
def instructions():
    main=True
    
    while main ==True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit();sys.exit()
                main = False
            if event.type == pygame.KEYDOWN:
                if event.key == ord('q'):
                    main=False
        world.fill(PURPLE)
        largeFont=pygame.font.SysFont("arial",35)
        textstring="The aim of the game is to keep the ball going for as long as possible.After each point the speed of the ball goes faster.. .The left arrow and a makes you go left.The right arrow and d makes you go right. If you press a and the left arrow at the same time you go faster.It is the same for the d and the right arrow.You can go through the walls.When you enter your name DO NOT press shift as you will exit that screen.. .Good luck!."
        textlist=textstring.split(".")
        y=50
        for t in textlist:
            text=largeFont.render(t,1,WHITE)
            world.blit(text,(50,y))
            y+=50
        pygame.display.flip()
        clock.tick(fps)
'''
Menu
'''
bestscores=loadscores(filename)
main=True

while main == True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()
            main = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == ord ('h'):
                print ('hall of fame')
                fame()
            if event.key == ord('e'):
                print("enter name")
                name=entername()
            if event.key == ord ('i'):
                print('instructions')
                instructions()
            if event.key == ord('p'):
                print('play')
                pygame.event.clear()
                bestscores=playgame(bestscores,name=name)
            if event.key == ord('q'):
                savescores(filename,bestscores)
                pygame.quit()
                sys.exit()
                main=False
    world.fill(PURPLE)
    largeFont=pygame.font.SysFont("arial",35)
    text=largeFont.render("Bat and Ball Game by Evelyn Hyland ",1,WHITE)
    world.blit(text,(350,50))
    text=largeFont.render("(P)lay ",0,WHITE)
    world.blit(text,(200,200))
    text=largeFont.render("(Q)uit",1,WHITE)
    world.blit(text,(200,150))
    text=largeFont.render("(I)nstructions",0,WHITE)
    world.blit(text,(200,250))
    text=largeFont.render("(H)all of Fame",1,WHITE)
    world.blit(text,(200,300))
    text=largeFont.render("(E)nter Name",0,WHITE)
    world.blit(text,(200,350))
    text=largeFont.render("Good luck "+name+"!",1,WHITE)
    world.blit(text,(200,450))
    
    pygame.display.flip()
    clock.tick