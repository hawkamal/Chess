"""
To save the user data

"""


class gamestate():
    def __init__(self):
        # board 8*8 - first letter = color - scenrd letter = type
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.whitetomove = True
        self.movelog = []
        self.whitekinglocation = (7, 4)
        self.blackkinglocation = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.pins = []
        self.checks = []


    def makemove(self, move):
        self.board[move.startrow][move.starlcol] = "--"
        self.board[move.endrow][move.endcol] = move.pieceMoved
        self.movelog.append(move)
        self.whitetomove = not self.whitetomove
        # update the kings moves
        if move.pieceMoved == "wK":
          self.whitekinglocation = (move.endrow, move.endcol)
        elif move.pieceMoved == "bK":
          self.blackkinglocation = (move.endrow, move.endcol)

    def undomove(self):
        if len(self.movelog) != 0:
            move = self.movelog.pop()
            self.board[move.startrow][move.starlcol] = move.pieceMoved
            self.board[move.endrow][move.endcol] = move.poececaptured
            self.whitetomove = not self.whitetomove
            if move.pieceMoved == "wK":
              self.whitekinglocation = (move.startrow, move.starlcol)
            elif move.pieceMoved == "bK":
              self.blackkinglocation = (move.startrow, move.starlcol)

    def getvaildemoves(self):
      moves = []
      self.incheck, self.pins, self.checks = self.checkforpinsandchecks()
      if self.whitetomove:
        kingrow = self.whitekinglocation[0]
        kingcol = self.whitekinglocation[1]
      else:
        kingrow = self.blackkinglocation[0]
        kingcol = self.blackkinglocation[1]

      if self.incheck:
        if len(self.checks) == 1: # only one check
          moves = self.getallpooseblemoves()
          check = self.checks[0]
          checkrow = check[0]
          checkcol = check[1]
          piecechicking = self.board[checkrow][checkcol]
          validesqurs = []
          if piecechicking[1] == "N":
            validesqurs = [(checkrow, checkcol)]
          else:
            for i in range(1, 8):
              validesqurs = (kingrow + check[2] * i, kingcol + check[3] * i)
              validesqurs.append(validesqurs)
              if validesqurs[0] == checkrow and validesqurs[1] == checkcol:
                break

        # make the moves
          for i in range(len(moves)-1, -1, -1):
            if moves[i].pieceMoved[1] != 'K':
              if not (moves[i].endrow, moves[i].endcol) in validesqurs:
                moves.remove(moves[i])
        else:
          self.getkingmoves(kingrow, kingcol, moves)

      else:
        moves = self.getallpooseblemoves()

      return moves



    def checkforpinsandchecks(self):
      pins = [] # when allied pins pieces
      checks = [] # where enemy is making check
      incheck = False
      if self.whitetomove:
        enemycolor = "b"
        allycolor = "w"
        startrow = self.whitekinglocation[0]
        starlcol = self.whitekinglocation[1]
      else:
        enemycolor = "w"
        allycolor = "b"
        startrow = self.blackkinglocation[0]
        starlcol = self.blackkinglocation[1]


      directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, 1), (-1, 1), (1, -1), (1, 1))
      for j in range(len(directions)):
        d = directions[j]
        posseblebin = ()
        for i in range(1, 8):
          endrow = startrow + d[0] * i
          endcol = starlcol + d[1] * i
          if 0 <= endrow < 8 and 0 <= endcol < 8:
            endPiece = self.board[endrow][endcol]
            if endPiece[0] == allycolor and endPiece != 'K':
                if posseblebin ==():
                    posseblebin = (endrow, endcol, d[0], d[1])
                else:
                  break
            elif endPiece[0] == enemycolor:
              type = endPiece[1]
              if (0 <= j <= 3 and type == R'') or\
                (4 <= j <= 7 and type == 'B') or\
                (i == 1 and type == 'P' and ((enemycolor == 'w' and 6 <= j <= 7) or       (enemycolor == 'b' and 4 <= j <= 5))) or\
                (type == 'Q') or (i == 1 and type == 'K'):
                  if posseblebin == ():
                    incheck = True
                    checks.append((endrow, endcol, d[0], d[1]))
                    break
                  else:
                    pins.append(posseblebin)
                    break
              else:
                break



      knightmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
      for n in knightmoves:
        endrow = startrow + n[0]
        endcol = starlcol + n[1]
        if 0 <= endrow < 8 and 0 <= endcol <8:
          endPiece = self.board[endrow][endcol]
          if endPiece[0] == enemycolor and endPiece[1] == 'N':
            incheck = True
            checks.append((endrow, endcol, n[0], n[1]))
      return incheck, pins, checks





    """
    will see if the player is in check
    """
    def incheck(self):
      if self.whitetomove:
        return self.squreunderattack(self.whitekinglocation[0], self.whitekinglocation[1])
      else:
        return self.squreunderattack(self.blackkinglocation[0], self.blackkinglocation[1])


    # if enemy can attack
    def squreunderattack(self, r, c):
      self.whitetomove = not self.whitetomove
      oppmoves = self.getallpooseblemoves()
      self.whitetomove = not self.whitetomove
      for move in oppmoves:
        if move.endrow == r and move.endcol == c: # sq is under attack
          return True

      return False







    def getallpooseblemoves(self):
        moves = []
        for r in range(len(self.board)):  # num of rows
            for c in range(len(self.board[r])):  # num of cols
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whitetomove) or (turn == 'b' and not self.whitetomove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getpawnmoves(r, c, moves)
                        print(moves)
                    elif piece == 'R':
                        self.getrookmoves(r, c, moves)
                    elif piece == 'N':
                        self.getknightmoves(r, c, moves)
                    elif piece == 'B':
                        self.getbeshhopmoves(r, c, moves)
                    elif piece == 'Q':
                        self.getqueenmoves(r, c, moves)
                    elif piece == 'K':
                        self.getkingmoves(r, c, moves)

        return moves

    # all pawn moves
    def getpawnmoves(self, r, c, moves):
        picepinned = False
        pindirection = ()
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
            picepinned = True
            pindirection = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break

        if self.whitetomove:  # whitw p moves
            if self.board[r - 1][c] == "--":  # sq p advanced
              if not picepinned or pindirection == (-1, 0):
                moves.append(move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2SQ p advanced
                    moves.append(move((r, c), (r - 2, c), self.board))

            if c - 1 >= 0:  # captured to left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy pice to captured
                   if not picepinned or pindirection == (-1, -1):
                    moves.append(move((r, c), (r - 1, c - 1), self.board))

            if c + 1 <= 7:  # caputered to the right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy pice to captured
                  if not picepinned or pindirection == (-1, 1):
                    moves.append(move((r, c), (r - 1, c + 1), self.board))




        else:
            if self.board[r + 1][c] == "--":  # sq p advanced
              if not picepinned or pindirection == (1, 0):
                moves.append(move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2SQ p advanced
                    moves.append(move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # captured to left
                if self.board[r + 1][c - 1][0] == 'w':  # enemy pice to captured
                  if not picepinned or pindirection == (1, -1):
                    moves.append(move((r, c), (r + 1, c - 1), self.board))

            if c + 1 <= 7:  # caputered to the right
                if self.board[r + 1][c + 1][0] == 'w':  # enemy pice to captured
                  if not picepinned or pindirection == (1, 1):
                    moves.append(move((r, c), (r + 1, c + 1), self.board))

                    # all rook moves

    def getrookmoves(self, r, c, moves):
        picepinned = False
        pindirection = ()
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
            picepinned = True
            pindirection = (self.pins[i][2], self.pins[i][3])
            if self.board[r][c][1] != 'Q':
              self.pins.remove(self.pins[i])
            break


        direcations = ((-1, 0), (0, -1), (1, 0), (0, 1))
        enemycoloure = "b" if self.whitetomove else "w"
        for d in direcations:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:  # on board
                  if not picepinned or pindirection == d or pindirection == (-d[0], -d[1]):
                    endPiece = self.board[endrow][endcol]
                    if endPiece == "--":  # empty space valide
                        moves.append(move((r, c), (endrow, endcol), self.board))

                    elif endPiece[0] == enemycoloure:  # enemy piece valide
                        moves.append(move((r, c), (endrow, endcol), self.board))
                        break
                    else:
                        break
                else:  # off board
                    break

    # all beshop moves
    def getbeshhopmoves(self, r, c, moves):
        picepinned = False
        pindirection = ()
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
            picepinned = True
            pindirection = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break



        direcations = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        enemycolor = "b" if self.whitetomove else "w"
        for d in direcations:
            for i in range(1, 8):
                endrow = r + d[0] * i
                endcol = c + d[1] * i
                if 0 <= endrow < 8 and 0 <= endcol < 8:  # on board
                  if not picepinned or pindirection == d or pindirection == (-d[0], -d[1]):
                    endPiece = self.board[endrow][endcol]
                    if endPiece == "--":  # empty space valide
                        moves.append(move((r, c), (endrow, endcol), self.board))
                    elif endPiece[0] == enemycolor:
                        moves.append(move((r, c), (endrow, endcol), self.board))
                        break

                    else:
                        break
                else:  # off board
                    break

    # all knight moves
    def getknightmoves(self, r, c, moves):
        picepinned = False
        for i in range(len(self.pins)-1, -1, -1):
          if self.pins[i][0] == r and self.pins[i][1] == c:
            picepinned = True
            pindirection = (self.pins[i][2], self.pins[i][3])
            self.pins.remove(self.pins[i])
            break


        knightmoves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        allycolor = "w" if self.whitetomove else "b"
        for m in knightmoves:
            endrow = r + m[0]
            endcol = c + m[1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:
              if not picepinned:
                endPiece = self.board[endrow][endcol]
                if endPiece[0] != allycolor:
                    moves.append(move((r, c), (endrow, endcol), self.board))

    # all queen moves
    def getqueenmoves(self, r, c, moves):
        self.getrookmoves(r, c, moves)
        self.getbeshhopmoves(r, c, moves)

    # all king moves
    def getkingmoves(self, r, c, moves):
        rowmoves = (-1, -1, -1, 0, 0, 1, 1, 1)
        colmoves = (-1, 0, 1, -1, 1, -1, 0, 1)
        kingmoves = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
        allycolor = "w" if self.whitetomove else "b"
        for i in range(8):
            endrow = r + kingmoves[i][0]
            endcol = c + kingmoves[i][1]
            if 0 <= endrow < 8 and 0 <= endcol < 8:  # on board
                endPiece = self.board[endrow][endcol]
                if endPiece != allycolor:  # empty space valide
                  if allycolor == 'w':
                    self.whitekinglocation = (endrow, endcol)
                  else:
                    self.blackkinglocation = (endrow, endcol)
                  incheck, pins, checks = self.checkforpinsandchecks()
                  if not incheck:
                    moves.append(move((r, c), (endrow, endcol), self.board))
                  if allycolor == 'w':
                    self.whitekinglocation = (r, c)
                  else:
                    self.blackkinglocation = (r, c)


class move():
    rankstorows = {"1": 7, "2": 6, "3": 5, "4": 4, "5": 3, "6": 2, "7": 1, "8": 0}
    rowstoranks = {v: k for k, v in rankstorows.items()}
    filstocol = {"a": 0, "b": 1, "c": 2, "d": 3, "e": 4, "f": 5, "g": 6, "h": 7}
    colstofiles = {v: k for k, v in filstocol.items()}

    def __init__(self, startSq, endSq, board):
        self.startrow = startSq[0]
        self.starlcol = startSq[1]
        self.endrow = endSq[0]
        self.endcol = endSq[1]
        self.pieceMoved = board[self.startrow][self.starlcol]
        self.poececaptured = board[self.endrow][self.endcol]
        self.moveID = (self.startrow * 1000 + self.starlcol * 100
                       + self.endrow * 10 + self.endcol)

    def __eq__(self, other):
        if isinstance(other, move):
            return self.moveID == other.moveID

    def getChessnotation(self):
        return self.getrankfile(self.startrow, self.starlcol) + self.getrankfile(self.endrow, self.endrow)

    def getrankfile(self, r, c):
        return self.colstofiles[c] + self.rowstoranks[r]
