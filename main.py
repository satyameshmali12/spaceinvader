# target of making this game is it should not get hang

from email.mime import audio
import pygame
import sys
import random
# import au

pygame.init()

width = 900
height = 700

display = pygame.display.set_mode((width,height))
clock = pygame.time.Clock()

# loading all the images over here
player = pygame.image.load("images/player.png")
background = pygame.transform.scale(pygame.image.load("images/background.png"),(width,height))
bullet = pygame.image.load("images/bullet.png")
enemy = pygame.transform.scale(pygame.image.load("images/enemy.png"),(100,80))



def gameloop():
    playerx = 400
    playery = 600
    speedx = 0
    bulletlist = []
    maxbullet = 1
    bulletspeed = -16
    enemylist = []
    num_of_enemies = 6
    score = 0
    gameover = False
    enemy_increaser = 20
    # enemy_speed = 4

    # playmusic("background")
    while True:
        if score>enemy_increaser:
            num_of_enemies +=2
            enemy_increaser+=20
            maxbullet+=1
        if not pygame.mixer.music.get_busy():
            playmusic("background")
        if gameover:
            for e in pygame.event.get():
                keys = pygame.key.get_pressed()
                # keys = pygame.key.get_pressed
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_SPACE:
                        # gameover = False
                        gameloop()
                    
            display.fill("green")
            displaytext("Press space barrestart",150,100,display)
            displaytext(f"Score:-{score}",150,300,display)
        else:
            for e in pygame.event.get():
                keys = pygame.key.get_pressed()
                # keys = pygame.key.get_pressed
                if e.type == pygame.QUIT:
                    sys.exit()

                if e.type == pygame.KEYDOWN:

                    if keys[pygame.K_LEFT]:
                        speedx = -15

                    if keys[pygame.K_RIGHT]:
                        speedx = 15
                    
                    if e.key == pygame.K_SPACE:
                        if len(bulletlist)<maxbullet:
                            fire_bullet(bulletlist,playerx,playery)
                            # playmusic("background")

                if e.type == pygame.KEYUP:
                    if e.key == pygame.K_LEFT or pygame.K_RIGHT:
                        speedx = 0
            
            # filling with white color in to the display
            display.fill("white")

            display.blit(background,(0,0))

            # moving the player
            playerx+=speedx

            # displaying the player
            displayimage(player,playerx,playery)

            if len(bulletlist)>0:
                for i in range(len(bulletlist)):
                    bulletx = bulletlist[i]["bulletx"]
                    bullety = bulletlist[i]["bullety"]
                    displayimage(bullet,bulletx,bullety)
                    bulletlist[i].update({
                        "bullety":bullety+bulletspeed
                    })
                    if bullety<0:
                        bulletlist.remove(bulletlist[i])
                        break

            # adding the enemies in the enemy list with the help of the spawn enemy function
            if len(enemylist)<num_of_enemies:
                enemylist = spawnenemy(enemylist)

            # spawing and moving all the enemies over here the screen 

            
            for i in range(len(enemylist)):
                x = enemylist[i]["enemyx"]
                y = enemylist[i]["enemyy"]

                if enemylist[i]["speedy"]>0:
                    enemylist[i].update({
                        "speedy":0
                    })
                if enemylist[i]["enemyx"]>width-30:
                    enemylist[i].update({
                        "speedx":-enemylist[i]["speedx"],
                        "speedy":60
                    })
                if enemylist[i]["enemyx"]<15:
                    enemylist[i].update({
                        "speedx":-enemylist[i]["speedx"],
                        "speedy":60
                    })
                
                if enemylist[i]["enemyy"]>playery-80:
                    print("lose")
                    gameover=True
                displayimage(enemy,enemylist[i]["enemyx"],enemylist[i]["enemyy"])
                enemylist[i].update({
                    "enemyx":x+enemylist[i]["speedx"],
                    "enemyy":y+enemylist[i]["speedy"]
                })
            
            bulletlist,enemylist,score = checkcollision(bulletlist,enemylist,score)

            displaytext(f"You Score is:{score}",4,2,display)
        
        pygame.display.update()

        clock.tick(70)


def displayimage(file,playerx,playery):
    display.blit(file,(playerx,playery))

def playmusic(name):
    pygame.mixer.music.load(f"customaudio/{name}.wav")
    pygame.mixer.music.play()

def fire_bullet(bulletlist,playerx,playery):
    playmusic("laser")
    obj = {
        "bulletx":playerx+20,
        "bullety":playery-15
    }
    bulletlist.append(obj)
    return bulletlist

def spawnenemy(enemylist):
    num = random.randint(20,50)
    enemyx = random.randint(20,width-70)
    enemyy = 10
    obj = {
        "enemyx":enemyx+num,
        "enemyy":enemyy,
        "speedx":12,
        "speedy":0
    }
    enemylist.append(obj)

    return enemylist

def checkcollision(bulletlist,enemylist,score):
    # removelist = []s
    for i in range(len(bulletlist)):
        for j in range(len(enemylist)):
            if bulletlist[i]["bulletx"]>enemylist[j]["enemyx"] and bulletlist[i]["bulletx"]<enemylist[j]["enemyx"]+enemy.get_width() and bulletlist[i]["bullety"]>enemylist[j]["enemyy"] and bulletlist[i]["bullety"]<enemylist[j]["enemyy"]+enemy.get_height():
                playmusic("explosion")
                score+=1
                bulletlist.remove(bulletlist[i])
                enemylist.remove(enemylist[j])
                return [bulletlist,enemylist,score]
            
    return [bulletlist,enemylist,score]

def displaytext(text,x,y,display):
    font = pygame.font.SysFont(None,50)
    text = font.render(text,True,"black")
    display.blit(text,(x,y))


gameloop()


