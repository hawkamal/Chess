"""
to collect user data
"""

import pygame as p
import chessengine
import ai

WIDTH = HIGHT = 512
#c = WIDTH
#r = HIGHT
DIMENSION = 8
SQ_size = WIDTH // DIMENSION
max_fps = 15  # for animation
# Creating a rect object with (x, y) coordinates (c * SQ_size, r * SQ_size) and dimensions (SQ_size, SQ_size)
#rect = p.rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size)
images = {}



def loadimages():
    pieces = ['bB', 'bK', 'bN', 'bp', 'bQ', 'bR', 'wB', 'wK', 'wN', 'wp', 'wQ', 'wR']
    for piece in pieces:
        images[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_size, SQ_size))


def main():
    p.init()
    screen = p.display.set_mode((WIDTH, HIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = chessengine.gamestate()
    validemoves = gs.getvaildemoves()
    movemade = False
    loadimages()
    running = True
    sqselected = ()
    playerclicks = []
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handeller
            elif e.type == p.MOUSEBUTTONDOWN:
                locetaion = p.mouse.get_pos()
                col = locetaion[0] // SQ_size
                row = locetaion[1] // SQ_size
                if sqselected == (row, col):
                    sqselected = ()
                    playerclicks = []
                  
                else:
                    sqselected = (row, col)
                    playerclicks.append(sqselected)

                if len(playerclicks) == 2:
                  move = chessengine.move(playerclicks[0], playerclicks[1], gs.board)
                  print(move.getChessnotation())
                  if move in validemoves:
                     gs.makemove(move)
                     movemade = True
                     sqselected = () #reset user clickes
                     playerclicks = []
                  else:
                    playerclicks = [sqselected]
           

                  


            elif e.type == p.KEYDOWN:
              if e.type == p.K_z: #undo when clicking z
                gs.undomove()
                movemade = True

        if movemade:
          validemoves = gs.getvaildemoves()
          movemade = False



        drawgamestate(screen, gs)
        clock.tick(max_fps)
        p.display.flip()


def drawgamestate(screen, gs):
    drawBoard(screen)  # draw squres
    drawPieces(screen, gs.board)


def drawBoard(screen):
    colors = [p.Color(192, 192, 192), p.Color(105,139,105)]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r + c) % 2)]
            p.draw.rect(screen, color, p.Rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size))



def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(images[piece], p.Rect(c * SQ_size, r * SQ_size, SQ_size, SQ_size))




if __name__ == "__main__":
    main()


