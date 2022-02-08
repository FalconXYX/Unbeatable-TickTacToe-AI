
import pygame, time, sys
import numpy as np
from pygame.locals import *
import random
black = (0,0,0)
white = (250,250,250)
pygame.init()

ximg = pygame.image.load('x.png')
oimg = pygame.image.load('o.png')

turn = 0
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
        self.middle = False
        self.center = False
        self.corner = False
        self.show = False
    def draw(self,player,win):
        if(player == 1):
            win.blit(ximg, (self.x,self.y))

        else:
            win.blit(oimg, (self.x,self.y))
    def showbox(self,win):
        win.blit(img1, (self.x,self.y))
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
    global player,arraybox, turn
    print("hit")

    if(arraybox[row][columb].clicked == False):
        if(player == 1):
            arraybox[row][columb].value = 0

            playernum = 2
            arraybox[row][columb].draw(player, display)
        elif(player == 2):
            arraybox[row][columb].value = 1
            arraybox[row][columb].draw(player, display)

            playernum = 1
        player = playernum
        arraybox[row][columb].boxclicked()
        turn +=1
def beside(input,num):
    cellx = np.where(arraybox == input)
    cellx = cellx[0]
    celly = np.where(arraybox == input)
    celly = celly[1]
    neigboors = []
    ncordsx = int(cellx)
    ncordsy = int(celly)
    try:
        ncordsx = int(cellx+num)
        ncordsy = int(celly)
        thing = arraybox[ncordsx][ncordsy]
        neigboors.append(thing)
    except:
        pass
    try:
        ncordsx = int(cellx-num)
        ncordsy = int(celly)
        if(ncordsx>-1):
            thing = arraybox[ncordsx][ncordsy]
            neigboors.append(thing)
    except:
        pass
    try:
        ncordsx = int(cellx)
        ncordsy = int(celly-num)
        if (ncordsy > -1):
            thing = arraybox[ncordsx][ncordsy]
            neigboors.append(thing)
    except:
        pass
    try:
        ncordsx = int(cellx)
        ncordsy = int(celly+num)
        thing = arraybox[ncordsx][ncordsy]
        neigboors.append(thing)
    except:
        pass
    neigboors = list(dict.fromkeys(neigboors))
    return neigboors
def diag(input, li1):
    n=[input]
    li2 = beside(input,2)
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    li_dif = [i for i in li_dif + n if i not in li_dif or i not in n]

    li_dif = [li_dif]
    li_dif.append(li2[0])
    li_dif.append(li2[1])
    print(li_dif)
    return li_dif

        

def turn2adj(input):
    global arraybox
    global player
    for cell in input:
        if (cell.value == 10):
            adjacent = beside(cell, 1)

            for cells in adjacent:

                if (cells.corner == True and cells.value == 10 and player == 1):

                    x = str(np.argwhere(arraybox == cells))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    clicked(w, l, 1)
    return current


def turn0(m,ce,co,mine,enemy,empty):
    if (turn == 0):
        rand = random.randint(0, 3)
        x = str(np.argwhere(arraybox == co[rand]))
        w = int(x[2])
        l = int(x[4])
        current = arraybox[w][l]
        mine.append(current)
        clicked(w, l, 1)
def turn2(m,ce,co,mine,enemy,empty):
    thing = 0
    if (turn == 2):
        # 1 beside
        if(thing == 0):
            adjacent = beside(mine[0], 1)
            for cell in adjacent:
                if (cell.value == 1 and player == 1):
                    enemy.append(cell)
                    current = turn2adj(adjacent)
                    mine.append(current)
                    return


        # 2 beside
        adjacent = beside(mine[0], 2)
        for cell in adjacent:
            if (cell.value == 1):
                enemy.append(cell)
                for cell in adjacent:
                    if (cell.value == 10):
                        x = str(np.argwhere(arraybox == cell))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(cell)
                        clicked(w, l, 1)
                        return

        d = diag(mine[0], co)
        adjacent = beside(d[0], 1)
        for cell in adjacent:
            if (cell.value == 1):
                enemy.append(cell)
                r = random.randint(1,2)
                x = str(np.argwhere(arraybox == d[r]))
                w = int(x[2])
                l = int(x[4])
                current = arraybox[w][l]
                mine.append(d[r])
                clicked(w, l, 1)
                return
        d = diag(mine[0], co)
        cell = d[0]
        if (cell[0].value == 1):
            enemy.append(cell)
            r = random.randint(1,2)
            x = str(np.argwhere(arraybox == d[r]))
            w = int(x[2])
            l = int(x[4])
            current = arraybox[w][l]
            mine.append(d[r])
            clicked(w, l, 1)
        if (ce.value == 1):
            d = diag(mine[0], co)
            enemy.append(ce)
            r = random.randint(1, 2)
            x = str(np.argwhere(arraybox == d[0]))
            w = int(x[2])
            l = int(x[4])
            current = arraybox[w][l]
            mine.append(d[0])
            clicked(w, l, 1)
            return



def turn4(m,ce,co,mine,enemy,empty):
    if(turn == 4):
        for x in range(0,3):
            if((arraybox[x][0].value+arraybox[x][1].value+arraybox[x][2].value)==10):
                templist = [arraybox[x][0],arraybox[x][1],arraybox[x][2]]
                for y in templist:
                    if(y.value == 10):
                        x = str(np.argwhere(arraybox == y))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(y)
                        clicked(w, l, 1)
                        return
        for x in range(0, 3):
                if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 10):
                    templist = [arraybox[0][x], arraybox[1][x], arraybox[2][x]]
                    for y in templist:
                        if (y.value == 10):
                            x = str(np.argwhere(arraybox == y))
                            w = int(x[2])
                            l = int(x[4])
                            current = arraybox[w][l]
                            mine.append(y)
                            clicked(w, l, 1)
                            return
        if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 10):
            templist = [arraybox[0][0], arraybox[1][1], arraybox[2][2]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 10):
            templist = [arraybox[0][2], arraybox[1][1], arraybox[2][0]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        #block
        for x in range(0,3):
            if((arraybox[x][0].value+arraybox[x][1].value+arraybox[x][2].value)==12):
                templist = [arraybox[x][0],arraybox[x][1],arraybox[x][2]]
                for y in templist:
                    if(y.value == 10):
                        x = str(np.argwhere(arraybox == y))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(y)
                        clicked(w, l, 1)
                        return
        for x in range(0, 3):
                if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 12):
                    templist = [arraybox[0][x], arraybox[1][x], arraybox[2][x]]
                    for y in templist:
                        if (y.value == 10):
                            x = str(np.argwhere(arraybox == y))
                            w = int(x[2])
                            l = int(x[4])
                            current = arraybox[w][l]
                            mine.append(y)
                            clicked(w, l, 1)
                            return
        if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 12):
            templist = [arraybox[0][0], arraybox[1][1], arraybox[2][2]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 12):
            templist = [arraybox[0][2], arraybox[1][1], arraybox[2][0]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return

        for box in co:
            if(box.value == 10):
                boxes = beside(box,1)
                t = True
                for b in boxes:
                    if(b.value == 1):
                        t == False
                if(t):
                    x = str(np.argwhere(arraybox == box))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(box)
                    clicked(w, l, 1)
                    return

def turn6(m,ce,co,mine,enemy,empty):
    if(turn == 6):


        for x in range(0,3):
            if((arraybox[x][0].value+arraybox[x][1].value+arraybox[x][2].value)==10):
                templist = [arraybox[x][0],arraybox[x][1],arraybox[x][2]]
                for y in templist:
                    if(y.value == 10):
                        x = str(np.argwhere(arraybox == y))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(y)
                        clicked(w, l, 1)
                        return
        for x in range(0, 3):
                if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 10):
                    templist = [arraybox[0][x], arraybox[1][x], arraybox[2][x]]
                    for y in templist:
                        if (y.value == 10):
                            x = str(np.argwhere(arraybox == y))
                            w = int(x[2])
                            l = int(x[4])
                            current = arraybox[w][l]
                            mine.append(y)
                            clicked(w, l, 1)
                            return
        if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 10):
            templist = [arraybox[0][0], arraybox[1][1], arraybox[2][2]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 10):
            templist = [arraybox[0][2], arraybox[1][1], arraybox[2][0]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        # block
        for x in range(0, 3):
            if ((arraybox[x][0].value + arraybox[x][1].value + arraybox[x][2].value) == 12):
                templist = [arraybox[x][0], arraybox[x][1], arraybox[x][2]]
                for y in templist:
                    if (y.value == 10):
                        x = str(np.argwhere(arraybox == y))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(y)
                        clicked(w, l, 1)
                        return
        for x in range(0, 3):
            if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 12):
                templist = [arraybox[0][x], arraybox[1][x], arraybox[2][x]]
                for y in templist:
                    if (y.value == 10):
                        x = str(np.argwhere(arraybox == y))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(y)
                        clicked(w, l, 1)
                        return
        if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 12):
            templist = [arraybox[0][0], arraybox[1][1], arraybox[2][2]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 12):
            templist = [arraybox[0][2], arraybox[1][1], arraybox[2][0]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return


def turn8(m,ce,co,mine,enemy,empty):
    if(turn == 8):
        for x in range(0,3):
            if((arraybox[x][0].value+arraybox[x][1].value+arraybox[x][2].value)==10):
                templist = [arraybox[x][0],arraybox[x][1],arraybox[x][2]]
                for y in templist:
                    if(y.value == 10):
                        x = str(np.argwhere(arraybox == y))
                        w = int(x[2])
                        l = int(x[4])
                        current = arraybox[w][l]
                        mine.append(y)
                        clicked(w, l, 1)
                        return
        for x in range(0, 3):
                if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 10):
                    templist = [arraybox[0][x], arraybox[1][x], arraybox[2][x]]
                    for y in templist:
                        if (y.value == 10):
                            x = str(np.argwhere(arraybox == y))
                            w = int(x[2])
                            l = int(x[4])
                            current = arraybox[w][l]
                            mine.append(y)
                            clicked(w, l, 1)
                            return
        if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 10):
            templist = [arraybox[0][0], arraybox[1][1], arraybox[2][2]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
        if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 10):
            templist = [arraybox[0][2], arraybox[1][1], arraybox[2][0]]
            for y in templist:
                if (y.value == 10):
                    x = str(np.argwhere(arraybox == y))
                    w = int(x[2])
                    l = int(x[4])
                    current = arraybox[w][l]
                    mine.append(y)
                    clicked(w, l, 1)
                    return
                # block
        for x in range(0, 3):
                    if ((arraybox[x][0].value + arraybox[x][1].value + arraybox[x][2].value) == 12):
                        templist = [arraybox[x][0], arraybox[x][1], arraybox[x][2]]
                        for y in templist:
                            if (y.value == 10):
                                x = str(np.argwhere(arraybox == y))
                                w = int(x[2])
                                l = int(x[4])
                                current = arraybox[w][l]
                                mine.append(y)
                                clicked(w, l, 1)
                                return
        for x in range(0, 3):
                    if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 12):
                        templist = [arraybox[0][x], arraybox[1][x], arraybox[2][x]]
                        for y in templist:
                            if (y.value == 10):
                                x = str(np.argwhere(arraybox == y))
                                w = int(x[2])
                                l = int(x[4])
                                current = arraybox[w][l]
                                mine.append(y)
                                clicked(w, l, 1)
                                return
        if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 12):
                    templist = [arraybox[0][0], arraybox[1][1], arraybox[2][2]]
                    for y in templist:
                        if (y.value == 10):
                            x = str(np.argwhere(arraybox == y))
                            w = int(x[2])
                            l = int(x[4])
                            current = arraybox[w][l]
                            mine.append(y)
                            clicked(w, l, 1)
                            return
        if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 12):
                    templist = [arraybox[0][2], arraybox[1][1], arraybox[2][0]]
                    for y in templist:
                        if (y.value == 10):
                            x = str(np.argwhere(arraybox == y))
                            w = int(x[2])
                            l = int(x[4])
                            current = arraybox[w][l]
                            mine.append(y)
                            clicked(w, l, 1)
                            return






def aiturn():
    global player,arraybox, turn
    corner = [arraybox[0][0],arraybox[0][2],arraybox[2][0],arraybox[2][2]]
    for cell in corner:
        cell.corner = True

    middle = [arraybox[0][1],arraybox[1][0],arraybox[1][2],arraybox[2][1]]
    for cell in middle:
        cell.middle == True
    center = arraybox[1][1]
    arraybox[1][1].center= True
    en = []
    m = []
    em = []
    for i in range(0, 3):
        for l in range(0, 3):
            if(arraybox[i][l].value == 10):
                em.append(arraybox[i][l])
    for i in range(0, 3):
        for l in range(0, 3):
            if(arraybox[i][l].value == 0):
                m.append(arraybox[i][l])
    for i in range(0, 3):
        for l in range(0, 3):
            if(arraybox[i][l].value == 1):
                en.append(arraybox[i][l])
    if(player ==1):
        print(turn)
        turn0(middle,center,corner,m,en,em)
        turn2(middle,center,corner,m,en,em)
        turn4(middle, center, corner, m, en, em)
        turn6(middle, center, corner, m, en, em)
        turn8(middle, center, corner, m, en, em)





pygame.display.set_caption("Tic Tac Toe")
def iswon():

    row = []
    columb = []
    diag = []
    for x in range(0,3):
        if((arraybox[x][0].value+arraybox[x][1].value+arraybox[x][2].value)==3):
            print("player 2 wins")
            time.sleep(10)
            sys.exit()
        if ((arraybox[x][0].value + arraybox[x][1].value + arraybox[x][2].value) == 0):
            print("player 1 wins")
            time .sleep(1)
            sys.exit()
    for x in range(0, 3):
        if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 3):
            print("player 2 wins")
            time.sleep(10)
            sys.exit()
        if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 0):
            print("player 1 wins")
            time.sleep(10)
            sys.exit()
    if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 3):
        print("player 2 wins")
        time.sleep(10)
        sys.exit()
    if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 0):
        print("player 1 wins")
        time.sleep(10)
        sys.exit()
    if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 3):
        print("player 2 wins")
        time.sleep(10)
        sys.exit()
    if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value)== 0):
        print("player 1 wins")
        time.sleep(10)
        sys.exit()
    if(turn == 9):
        print("Tie")
        time.sleep(10)
        sys.exit()
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            run  = False
    x, y = pygame.mouse.get_pos()
    aiturn()

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
    iswon()


pygame.quit()
quit()
