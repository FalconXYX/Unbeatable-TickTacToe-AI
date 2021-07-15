
import pygame, time, sys
import numpy as np
from pygame.locals import *

black = (0,0,0)
white = (250,250,250)
pygame.init()

ximg = pygame.image.load('x.png')
oimg = pygame.image.load('o.png')


run = True
display_width = 500
display_height =550
display= pygame.display.set_mode((display_width, display_height))
display.fill((black))
player = 1
class box():
    def __init__(self,x,y,l,w,display):
        self.x = x
        self.y = y
        self.value = 10
        self.clicked = False
    def draw(self,player,win):

        if(player == 1):
            win.blit(ximg, (self.x,self.y))

        else:
            win.blit(oimg, (self.x,self.y))
    def boxclicked(self):
        self.clicked = True


t = []

def makeboxes():

    for i in range(0,3):
        t.append(box(i*130+60,70,0,0,display))
    for i in range(0,3):
        t.append(box(i*130+60,200,0,0,display))
    for i in range(0,3):
        t.append(box(i*130+60,380,0,0,display))
boxes = t
arraybox = np.array([])
def Make2darray():
    global arraybox
    insert = []
    for x in range(0, 3):
        for i in range(0,3):
            insert.append(t.pop(0))
        if (x == 0):
            arraybox = np.array([insert])
        else:
            arraybox = np.append(arraybox, [insert], axis=0)
        insert = []



makeboxes()
Make2darray()

def clicked(row, columb, playernum):
    global player,arraybox

    if(arraybox[row][columb].clicked == False):
        if(player == 1):
            arraybox[row][columb].value = 0

            playernum = 2
            arraybox[row][columb].draw(player, display)
        if(player == 2):
            arraybox[row][columb].value = 1
            arraybox[row][columb].draw(player, display)

            playernum = 1
        player = playernum
        arraybox[row][columb].boxclicked()




pygame.display.set_caption("Tick")
def iswon():
    row = []
    columb = []
    diag = []
    for x in range(0,3):
        if((arraybox[x][0].value+arraybox[x][1].value+arraybox[x][2].value)==3):
            print("player 2 wins")
            time.sleep(1)
            sys.exit()
        if ((arraybox[x][0].value + arraybox[x][1].value + arraybox[x][2].value) == 0):
            print("player 1 wins")
            time .sleep(1)
            sys.exit()
    for x in range(0, 3):
        if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 3):
            print("player 2 wins")
            time.sleep(1)
            sys.exit()
        if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 0):
            print("player 1 wins")
            time.sleep(1)
            sys.exit()
    if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 3):
        print("player 2 wins")
        time.sleep(1)
        sys.exit()
    if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 0):
        print("player 1 wins")
        time.sleep(1)
        sys.exit()
    if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 3):
        print("player 2 wins")
        time.sleep(1)
        sys.exit()
    if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value)== 0):
        print("player 1 wins")
        time.sleep(1)
        sys.exit()

while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run  = False
    x, y = pygame.mouse.get_pos()
    iswon()
    if event.type == pygame.MOUSEBUTTONDOWN:
        if(x>60 and x< 180 and y >70 and y< 200):
            clicked(0,0, player)
        if (x > 180 and x < 340 and y > 70 and y < 200):
            clicked(0, 1, player)
        if (x > 340 and x < 450 and y > 70 and y < 200):
            clicked(0, 2, player)

        if (x > 60 and x < 180 and y > 200 and y < 380):
            clicked(1, 0, player)
        if (x > 180 and x < 340 and y > 200 and y < 380):
            clicked(1, 1, player)
        if (x > 340 and x < 450 and  y > 200 and y < 380):
            clicked(1, 2, player)

        if (x > 60 and x < 180 and y > 380 and y < 520):
            clicked(2, 0, player)
        if (x > 180 and x < 340 and y > 380 and y < 520):
            clicked(2, 1, player)
        if (x > 340 and x < 450 and y > 380 and y < 520):
            clicked(2, 2, player)

    pygame.draw.line(display, white, (50, 200), (450, 200))
    pygame.draw.line(display, white, (50, 380), (450, 380))
    pygame.draw.line(display, white, (180, 70), (180, 520))
    pygame.draw.line(display, white, (340, 70), (340, 520))



    pygame.display.update()


pygame.quit()
quit()
