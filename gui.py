#Didn't bother commenting pygame stuff, just a front end for interaction between AI and Grid class

from lib.Grid import Grid, Moves
from lib.AI import AI
import pygame
import sys
import math
from pygame.locals import *
import time
import copy

game = Grid()
AI_ENABLED = True #Choose whether AI is enabled or not
Ai = AI(multi_core=False) #Parralel processing is not supported on windows with pygame :( (Awesome speeds on linux + i7 8700k)
N_GAMES = 50 #Number of games to simulate per move, high number = better but slower AI (Eg. 400 has 100% chance of getting 2048 from my experience)
pygame.init()
pygame.display.set_caption('2048 - MADE BY PARAS')
SIZE = (600, 600)
SCREEN = pygame.display.set_mode(SIZE)
pygame.font.init()
BOX_SIZE = (SIZE[0]/game.cols(), SIZE[1]/game.rows())
COLOURS = {
    0: (255, 255, 255),
    2: (109, 232, 166),
    4: (109, 232, 214),
    8: (109, 199, 232),
    16: (109, 160, 232),
    32: (109, 123, 232),
    64: (121, 109, 232),
    128: (152, 109, 232),
    256: (203, 109, 232),
    512: (232, 109, 203),
    1024: (232, 109, 146),
    2048: (232, 109, 109),
    "other": (247, 54, 54)
}

def render_text(text, x_pos, y_pos, size):
    FONT = pygame.font.SysFont('Arial', size)
    text = FONT.render(str(text), True, (0, 0, 0))
    SCREEN.blit(text, (x_pos - text.get_width()/2, y_pos - text.get_height()/2))

alive = True

def main():
    global alive
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYUP and alive and not AI_ENABLED:
                if event.key == K_LEFT or event.key == K_a:
                    if not game.move(Moves.LEFT): alive = False
                elif event.key == K_RIGHT or event.key == K_d:
                    if not game.move(Moves.RIGHT): alive = False
                elif event.key == K_UP or event.key == K_w:
                    if not game.move(Moves.UP): alive = False
                elif event.key == K_DOWN or event.key == K_s:
                    if not game.move(Moves.DOWN): alive = False

        SCREEN.fill((255, 255, 255))
        
        if AI_ENABLED and alive:
            if not game.move(Ai.next_move(game, N_GAMES)):
                print(f"Finished with a score of: {game.score()}")
                alive = False

        for row in enumerate(game):
            for cell in enumerate(row[1]):
                if cell[1] != 0:
                    if cell[1] in COLOURS: colour = COLOURS[cell[1]]
                    else: colour = COLOURS["other"]
                    pygame.draw.rect(SCREEN, colour, (BOX_SIZE[0] * cell[0], BOX_SIZE[1] * row[0], BOX_SIZE[0], BOX_SIZE[1]))
                    render_text(cell[1], BOX_SIZE[0] * cell[0] + BOX_SIZE[0]/2, BOX_SIZE[1] * row[0] + BOX_SIZE[1]/2, int(BOX_SIZE[1]/4))

        for row in range(1, game.rows()):
            pygame.draw.line(SCREEN, 0, (0, row*(SIZE[1] / game.rows()) -1.5), (SIZE[0], row*(SIZE[1] / game.rows()) - 1.5), 3)
        for col in range(1, game.cols()):
            pygame.draw.line(SCREEN, 0, (col*(SIZE[0] / game.cols()) -1.5, 0), (col*(SIZE[0] / game.cols()) -1.5, SIZE[1]), 3)

        pygame.display.flip()

if __name__ == "__main__":
    main()
