import pygame, time, sys
import numpy as np
from pygame.locals import *
import random, os, neat
global display
black = (0, 0, 0)
white = (250, 250, 250)
pygame.init()



class box():
    def __init__(self, x, y, l, w):
        self.x = x
        self.y = y
        self.value = 10
        self.clicked = False
        self.middle = False
        self.center = False
        self.corner = False
        self.show = False

    def draw(self, player, win):
        return self.x, self.y

    def showbox(self, win):
        win.blit(img1, (self.x, self.y))

    def boxclicked(self):
        self.clicked = True
class person():
    def __init__(self, emp):

        self.wins = 0
        self.losses = 0
        self.ties = 0
def makeboxes(t):
    for i in range(0, 3):
        t.append(box(i * 130 + 60, 70, 0, 0 ))
    for i in range(0, 3):
        t.append(box(i * 130 + 60, 200, 0, 0))
    for i in range(0, 3):
        t.append(box(i * 130 + 60, 380, 0, 0))
def Make2darray(t, ar, va):
    insert = []
    insert2 = []
    for x in range(0, 3):
        for i in range(0, 3):
            insert.append(t.pop(0))
            insert2.append(insert[0].value)
        if (x == 0):
            ar = np.array([insert])
            va.append([insert2])
        else:
            ar = np.append(ar, [insert], axis=0)
            va.append([insert2])
        insert = []
        insert2 = []
    return ar, va

def clicked(row, columb, playernum, d, t):
    global player, players, arraybox,ge, display, pyrun, turn


    if (arraybox[row][columb].clicked == False):
        count = 0
        
        ge[player].fitness += 0.1
        if (player == 0):

            arraybox[row][columb].value = 0

            playernum = 1
            x,y =  arraybox[row][columb].draw(player, display)
            ximg = pygame.image.load('x.png')

            display.blit(ximg, (x, y))



        elif (player == 1):
            arraybox[row][columb].value = 1
            oimg = pygame.image.load('o.png')
            playernum = 0
            x,y= arraybox[row][columb].draw(player, display)
            display.blit(oimg, (x, y))


        player = playernum

        arraybox[row][columb].boxclicked()
        t += 1
        turn =t

    else:

        ge[player].fitness -= 1
        print(ge[player].fitness)
        players.pop(player)
        ge.pop(player)
        nets.pop(player)


        ge[0].fitness += 0.1
        print(ge[0].fitness)
        players.pop(0)
        ge.pop(0)
        nets.pop(0)
        pyrun = False

def iswon(arraybox):

    row = []
    columb = []
    diag = []
    for x in range(0, 3):
        if ((arraybox[x][0].value + arraybox[x][1].value + arraybox[x][2].value) == 3):
            ge[1].fitness += 2
            ge[0].fitness -= 1.5

        if ((arraybox[x][0].value + arraybox[x][1].value + arraybox[x][2].value) == 0):
            ge[0].fitness += 2
            ge[1].fitness -= 1.5

    for x in range(0, 3):
        if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 3):
            ge[1].fitness += 2
            ge[0].fitness -= 1.5
        if ((arraybox[0][x].value + arraybox[1][x].value + arraybox[2][x].value) == 0):
            ge[0].fitness += 2
            ge[1].fitness -= 1.5


    if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 3):
        ge[1].fitness += 2
        ge[0].fitness -= 1.5

    if ((arraybox[0][0].value + arraybox[1][1].value + arraybox[2][2].value) == 0):
            ge[0].fitness += 2
            ge[1].fitness -= 1.5

    if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 3):
        ge[1].fitness += 2
        ge[0].fitness -= 1.5

    if ((arraybox[0][2].value + arraybox[1][1].value + arraybox[2][0].value) == 0):
            ge[0].fitness += 2
            ge[1].fitness -= 1.5
    if (turn == 9):
        print("Tie")
def main(genomes, config):

    global arraybox, player, valuearray, display, ge, players, nets, pyrun


    turn = 0
    pyrun = True

    display_width = 550
    display_height = 550
    display = pygame.display.set_mode((display_width, display_height))
    display.fill((black))
    player = 1

    pygame.draw.line(display, white, (50, 200), (450, 200))
    pygame.draw.line(display, white, (50, 380), (450, 380))
    pygame.draw.line(display, white, (180, 70), (180, 520))
    pygame.draw.line(display, white, (340, 70), (340, 520))




    t = []
    boxes = t
    arraybox = np.array([])
    valuearray = []
    makeboxes(t)
    arraybox, valuearray = Make2darray(t, arraybox, valuearray)
    pygame.display.set_caption("Tic Tac Toe")
    players = []
    ge = []
    nets = []

    for _, g in genomes:
        players.append(person(arraybox))
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        ge.append(g)
    while pyrun:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pyrun = False
        x, y = pygame.mouse.get_pos()
        corner = [arraybox[0][0], arraybox[0][2], arraybox[2][0], arraybox[2][2]]
        middle = [arraybox[0][1], arraybox[1][0], arraybox[1][2], arraybox[2][1]]
        center = arraybox[1][1]
        for pl in players:
            number = players.index(pl)
            p = [arraybox[0][0].value,arraybox[0][1].value,arraybox[0][2].value,arraybox[1][0].value,arraybox[1][1].value,arraybox[1][2].value,arraybox[2][0].value,arraybox[2][1].value,arraybox[2][2].value,]
            output = nets[number].activate(p)



            while True:
                if (output[0] >= 0.75 and output[0] <= 1):
                    clicked(0, 0, player, display, turn)
                    break
                elif (output[0] >= 0.5 and output[0] <= 0.75):
                    clicked(0, 1, player, display, turn)
                    break
                elif (output[0] >= 0.25 and output[0] <= 0.5):
                    clicked(0, 2, player, display, turn)
                    break

                elif (output[0] >= 0 and output[0] <= 0.25):
                    clicked(1, 0, player, display, turn)
                    break
                elif (output[0] >= -0.25 and output[0] <= 0):
                    clicked(1, 1, player, display, turn)
                    break
                elif (output[0] >= -0.5 and output[0] <= -0.25 ):
                    clicked(1, 2, player, display, turn)
                    break

                elif (output[0] >= -0.75 and output[0] <= -0.5):
                    clicked(2, 0, player, display, turn)
                    break
                elif (output[0] >= -0.9 and output[0] <= -0.75):
                    clicked(2, 1, player, display, turn)
                    break
                elif (output[0] >= -1.1 and output[0] <= -0.9):
                    clicked(2, 2, player, display, turn)
                    break
                else:
                    print(output[0], "f")


            pygame.display.update()


    iswon(arraybox)


def runsim(config_file):

    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)
    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)
    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(5))
    # Run for up to 5 generations.
    winner = p.run(main, 500)
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))



local_dir = os.path.dirname(__file__)

config_path = os.path.join(local_dir, 'config-feedforward.txt')
runsim(config_path)

pygame.quit()
quit()
