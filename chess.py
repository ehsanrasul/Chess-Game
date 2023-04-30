# Ehsan 20i-1812

import copy
import random

board = [[" " for i in range(8)] for j in range(8)]   # creating board here

myCheck=0
AIsCheck=0


#This function takes in the current board state as input and evaluates 
#it based on the points assigned to each piece on the board. It iterates through 
#each square on the board, checks if it has a white or black piece, and adds or 
#subtracts the piece's point value accordingly. The final evaluation value is returned.
def evaluation(board):
    eval=0
    for i in range(0,8):
        for j in range(0,8):
            if board[i][j].color=="white":
                eval=eval+board[i][j].points
            elif board[i][j].color=="black":
                eval=eval-board[i][j].points
    return eval 


def printBoard(board):
    str1 = "  "
    xGrid = ["a", "b", "c", "d", "e", "f", "g", "h"]
    for i in range(0, len(xGrid)):
        str1 = str1 + " - " + xGrid[i]
    print("\t\t\t\t\t\t"+grid.green+str1+grid.RESET)
    for i,b in enumerate(board):
        print("\t\t\t\t\t\t"+grid.red+str(8-i)+grid.RESET, end=" ")
        printRow(b)


def printRow(b):

    str1=""
    for i in range(0,len(b)):
        str1=str1+ " - "+b[i].printPiece()
    print(str1)


#This function updates the castling rights after
#a move has been made. If a king or rook has moved, the 
#corresponding castling rights for that player are updated accordingly
def updateCastlingRights(peice):
    if peice.getName() == 'k' :
        currCastlingRight.bk = False
        currCastlingRight.bq = False

    if peice.getName() == 'r' :
        x, y = peice.getCoordinates()
        if x == 0 and y == 0:
            currCastlingRight.bk = False
        elif x == 0 and y == 7:
            currCastlingRight.bq = False

    elif peice.getName() == 'K':
        currCastlingRight.wk = False
        currCastlingRight.wq = False



class grid:          
    green='\033[91m'
    red='\033[93m'
    yellow='\033[0;36m'
    RESET='\033[0m'


# castling rights class, givrs castling rights to user and AI. queen side and king side
class CastlingRights:
    def __init__(self,wk,bk,wq,bq):
        self.wk = wk
        self.bk = bk
        self.wq = wq
        self.bq = bq

castling_pieces = ['r','R','K','k']
currCastlingRight = CastlingRights(True,True,True,True)   # initial castling rights
castleRightsLog = [CastlingRights(currCastlingRight.wk, currCastlingRight.bk, currCastlingRight.wq,currCastlingRight.bq)]   # log of castling rights


#This function moves the rook and king pieces for castling,
#updating the board accordingly, and returns the new position of the rook.
def castleMovement(endCol, startcol, endRow,startRow):
    if  startcol - endCol == 2:  # king side castle
        board[endRow][endCol + 1] = board[endRow][endCol - 1]
        board[endRow][endCol - 1] = chessPiece(None, "`", 0, 0, endRow, endCol - 1)
        board[endRow][endCol] = board[endRow][startcol]
        board[endRow][startcol] = chessPiece(None, "`", 0, 0, endRow, startcol)
        return endRow, endCol + 1

    else:  # queen side castle
        board[endRow][endCol - 1] = board[endRow][endCol + 2]
        board[endRow][endCol + 2] = chessPiece(None, "`", 0, 0, endRow, endCol + 2)
        board[endRow][endCol] = board[endRow][startcol]
        board[endRow][startcol] = chessPiece(None, "`", 0, 0, endRow, startcol)
        return endRow, endCol + 2



def kingsideCastleMoves(x, y):

    if board[x][y - 1].getName() == '.' and board[x][y - 2].getName() == '.':
        if board[x][y - 1].attacked == False and board[x][y - 2].attacked == False:
            mov = castleMovement(y - 2, y, x, x)
            return mov[0],mov[1]
    return None


def queenSideCastleMoves(x, y):
    if board[x][y + 1].getName() == '.' and board[x][y + 2].getName() == '.' and board[x][y + 3].getName() == '.':
        if board[x][y + 1].attacked == False and board[x][y + 2].attacked == False:
            mov = castleMovement(y + 2, y, x, x)
            return mov[0], mov[1]
    return None

def getCastlingMoves(x, y, type_k,val):
    if (type_k == "K" and currCastlingRight.wk) or (type_k == "k" and currCastlingRight.bk and val[0] == 0 and val[1] == 0):
        print("inside")
        moves = kingsideCastleMoves(x, y)

    elif (type_k == "K" and currCastlingRight.wq) or (type_k == "k" and currCastlingRight.bq  and val[0] == 0 and val[1] == 7):
        print("inside")
        moves = queenSideCastleMoves(x, y)
    return moves


def getIntialRows(color):
    names=["r","n","b","k","q","b","n","r"]
    points=[5,3,3,500,9,3,3,5]
    row=[]
    for i,n in enumerate(names):    
        if color=="white":
            row.append(chessPiece(color,n.upper(),points[i],0,7,i))
        else:
            row.append(chessPiece(color, n, points[i], 0,0,i))
    return row


def initialize_board(board):
    board[0]=getIntialRows("black")
    board[7]=getIntialRows("white")
    board[1]=[chessPiece("black","p",1,0,1,i) for i in range(0,len(board[1]))]
    board[6]=[chessPiece("white","P",1,0,6,i) for i in range(0,len(board[6]))]
    for i in range(2,6):
        board[i]=[chessPiece(None,"`",0,0,i,j) for j in range(0,len(board[i]))]



#This function takes in the position of a black pawn on a chess board and returns a list of all
#possible moves for that pawn, including attacking moves and pawn promotions if applicable
def blackPawn(position):
    next=[]
    moves = [(position[0] + 1, position[1] -1) ,(position[0] + 1, position[1]) ,(position[0] + 1, position[1] +1) ]
    for i,m in enumerate(moves):
        if m[0]>7 or m[0]<0 or m[1]>7 or m[1]<0 :
            continue
        if i!=1:
            if  board[m[0]][m[1]].color!=None and board[m[0]][m[1]].color!="black":
                next.append([(m[0],m[1]),board[position[0]][position[1]]])
        else:
            if board[m[0]][m[1]].getName() == "`":
                next.append([(m[0],m[1]), board[position[0]][position[1]]])
    if position[0] == 1:
        if board[position[0] + 1][position[1]] .getName() == "`" and board[position[0] + 2][position[1]].getName() == "`":
            next.append([(position[0] + 2,position[1]),board[position[0]][position[1]]])
    return next



def moveWhitePawn(position):
    next = []
    moves = [(position[0] - 1, position[1] - 1), (position[0] - 1, position[1]), (position[0] - 1, position[1] + 1)]
    for i, m in enumerate(moves):
        if m[0] > 7 or m[0] < 0 or m[1] > 7 or m[1] < 0:
            continue
        if i != 1:
            if board[m[0]][m[1]].color != None and board[m[0]][m[1]].color != "white":# add coord where it can attack

                next.append([(m[0], m[1]), board[position[0]][position[1]]])
        else:
            if board[m[0]][m[1]].getName() == "`":

                next.append([(m[0], m[1]), board[position[0]][position[1]]])

    if position[0] == 6:

        if board[position[0] - 1][position[1]].name == "`" and board[position[0] - 2][position[1]].name == "`":

            next.append([(position[0] - 2, position[1]), board[position[0]][position[1]]])

    return next

def Rook(position):
    next=[]
    x=position[0]
    y=position[1]
    moves = [
        [[x - i, y] for i in range(1, x + 1)],  # up
        [[x, y - i] for i in range(1, y + 1)],#left
        [[x + i, y] for i in range(1, 8 - x)],  # down
        [[x, y + i] for i in range(1, 8 - y)],#right
             ]

    for dir in moves:
        for m in dir:
            if m[0] > 7 or m[0] < 0 or m[1] > 7 or m[1] < 0:#check if valid
                dir.remove(m)
                continue
            if board[m[0]][m[1]].name =="`":#movement
                next.append([(m[0],m[1]),board[position[0]][position[1]]])
            else:
                    if board[m[0]][m[1]].color != board[position[0]][position[1]].color:#attacking point
                        next.append([(m[0], m[1]), board[position[0]][position[1]]])
                    break
    return next


def Bishop(position):
    x=position[0]
    y=position[1]
    next=[]
    moves = [
    [[x + i, y + i] for i in range(1, 8)],
    [[x - i, y - i] for i in range(1, 8)],
    [[x + i, y - i] for i in range(1, 8)],
    [[x - i, y + i] for i in range(1, 8)]

    ]

    for dir in moves:
        for m in dir:
            if m[0] > 7 or m[0] < 0 or m[1] > 7 or m[1] < 0:
                dir.remove(m)
                continue
            if board[m[0]][m[1]].name =="`":
                next.append([(m[0],m[1]),board[position[0]][position[1]]])
            else:
                    if board[m[0]][m[1]].color != board[position[0]][position[1]].color:
                        next.append([(m[0], m[1]), board[position[0]][position[1]]])
                    break
    return next


def King(position):
    x=position[0]
    y=position[1]
    next=[]
    for col in range(0,3):
        for row in range(0,3):
            if (x - 1 + col>-1 and x - 1 + col<8 and y - 1 + row>-1and y - 1 + row<8):
                if board[x - 1 + col][y - 1 + row].name =="`" :
                        next.append([(x-1+col,y-1+row),board[position[0]][position[1]]])
                else:
                    if board[x - 1 + col][y - 1 + row].color != board[x][y].color:
                        # board[x - 1 + col][y - 1 + row].attacked = 1
                        next.append([(x - 1 + col,y - 1 + row), board[position[0]][position[1]]])
    return next


class chessPiece:
    def __init__(self,color,name,points,attacked,x,y):
        self.color=color
        self.name=name
        self.points=points
        self.attacked=attacked
        self.coordinates=(x,y)
        self.moved = False

        if name in castling_pieces:
            self.castlingRights = True
        else:
            self.castlingRights = False

    def printPiece(self):
        return self.name
    def getName(self):
        return self.name
    def setName(self,name):
        self.name=name
    def setMoved(self, moved):
        self.moved = moved
    def getMoved(self):
        return self.moved
    def setCastlingRights(self):
        return self.moved
    def getCoordinates(self):
        return self.coordinates[0], self.coordinates[1]


def checkCheckof(exp,color):
    player="True"
    k=""
    if color=="black":
        player=True
        k="k"
    elif color=="white":
        player=False
        k="K"

    list1=getAllMoves(exp,player)
    kingCoordinates=getCoordinatesOfKing(k,exp)
    if(kingCoordinates in list1):
            return True
    else:
        return False


def Knight(position):
    x=position[0]
    y=position[1]
    next=[]
    for i in range(-2, 3):
        for col in range(-2, 3):
            # print("----",i ** 2 + col ** 2)
            if i ** 2 + col ** 2 == 5:
                # print(i,col)
                if (x + i>-1 and  y + col >-1 and  y + col <8 and x + i<8):
                    if board[x + i][y + col] =="`":
                        next.append([(x + i,y + col), board[x][y]])
                    else:
                        if board[x + i][y + col].color != board[x][y].color:
                            next.append([(x + i, y + col), board[x][y]])
    return next



def Queen(position):

    next=[]
    x=position[0]
    y=position[1]
    moves = [
        [[x - i, y] for i in range(1, x + 1)],
        [[x, y - i] for i in range(1, y + 1)],
        [[x + i, y] for i in range(1, 8 - x)],
        [[x, y + i] for i in range(1, 8 - y)],
             ]

    for dir in moves:
        for m in dir:
            if m[0] > 7 or m[0] < 0 or m[1] > 7 or m[1] < 0:
                dir.remove(m)
                continue
            if board[m[0]][m[1]].name =="`":
                # board[m[0]][m[1]].name= "m"
                next.append([(m[0],m[1]),board[position[0]][position[1]]])
            else:
                    if board[m[0]][m[1]].color != board[position[0]][position[1]].color:
                        # board[m[0]][m[1]].attacked = 1
                        next.append([(m[0], m[1]), board[position[0]][position[1]]])
                    break
    x=position[0]
    y=position[1]

    moves = [
    [[x + i, y + i] for i in range(1, 8)],
    [[x - i, y - i] for i in range(1, 8)],
    [[x + i, y - i] for i in range(1, 8)],
    [[x - i, y + i] for i in range(1, 8)]

    ]

    for dir in moves:
        for m in dir:
            if m[0] > 7 or m[0] < 0 or m[1] > 7 or m[1] < 0:
                dir.remove(m)
                continue
            if board[m[0]][m[1]].name =="`":
                # board[m[0]][m[1]].name= "m"
                next.append([(m[0],m[1]),board[position[0]][position[1]]])
            else:
                    if board[m[0]][m[1]].color != board[position[0]][position[1]].color:
                        # board[m[0]][m[1]].attacked = 1
                        next.append([(m[0], m[1]), board[position[0]][position[1]]])
                    break
    return next



def result(board, action):

    result_board = copy.deepcopy(board)

    curr_player = copy.deepcopy(action[1])

    (i, j) = action[0]

    result_board[i][j] = curr_player
    oldcoordinates = curr_player.coordinates  

    blank=chessPiece(None,"`",0,0,oldcoordinates[0],oldcoordinates[1])

    result_board[oldcoordinates[0]][oldcoordinates[1]]=blank


    result_board[i][j].coordinates = action[0]

    if result_board[i][j].coordinates[0]==0 and result_board[i][j].name=="P":
        result_board[i][j].name="Q"
        result_board[i][j].points = 9
    elif result_board[i][j].coordinates[0]==7 and result_board[i][j].name=="p":
        result_board[i][j].name="q"
        result_board[i][j].points = 9

    return result_board

initialize_board(board)
printBoard(board)


def isValidPiece(old):
    if(board[old[0]][old[1]].color!=None and board[old[0]][old[1]].color!="white"):# our assumption: white=AI and black=User
        return True
    else:
        return False


def getPieceAt(old):
    return board[old[0]][old[1]]


def getCoordinatesOfKing(name,b):
    for i in range(0,8):
        for j in range(0,8):
            if b[i][j].name==name:
                return b[i][j].coordinates


def getLegalmoves(piece):
    lmoves = []
    val = None
    if piece.name == "p":
        moves = blackPawn(piece.coordinates)
    elif piece.name=="r":
        moves = Rook(piece.coordinates)
    elif piece.name == "b":
        moves = Bishop(piece.coordinates)
    elif piece.name == "n":
        moves = Knight(piece.coordinates)
    elif piece.name == "q":
        moves = Queen(piece.coordinates)
    elif piece.name == "k":
        moves = King(piece.coordinates)

    for m in moves:
        lmoves.append(m[0])
    return lmoves



#Function to check if a king is in checkmate by getting all possible
#moves for the opponent's pieces (if the AI's king is in check) or the 
#AI's pieces (if the opponent's king is in check). If the king is in check and 
#has no available moves to get out of check, it returns True. Otherwise, it returns False.
def checkCheckmate(board):
    list1=getAllMoves(board,True)
    kingCoordinates=getCoordinatesOfKing("k",board)
    if(kingCoordinates in list1):
        print("black king is in check")
        myCheck=1
        list2=King(kingCoordinates)
        if list2==[]:
            print("White Wins")
            return True
        else:
            myCheck=0
    list1 = getAllMoves(board, False)
    kingCoordinates = getCoordinatesOfKing("K",board)
    if (kingCoordinates in list1):
        print("My king is in check")
        AIsCheck=1
        list2 = King(kingCoordinates)
        if list2 == []:
            print("I Won")
            return True
        else:
            AIsCheck=0
    return False



def gameEnd(board):
    if checkCheckmate(board):
        return True
    else:
        return False


def getAllMoves(board,max_player):
    allActions=[]

    if max_player==True:
        for i in range(0,8):
            for j in range(0, 8):
                actions=[]
                if(board[i][j].name=="P"):
                    actions = moveWhitePawn((i, j))
                elif (board[i][j].name == "R"):
                    actions = Rook((i, j))
                elif (board[i][j].name == "N"):
                    actions = Knight((i, j))
                elif (board[i][j].name == "B"):
                    actions = Bishop((i, j))
                elif (board[i][j].name == "K"):
                    actions = King((i, j))
                elif (board[i][j].name == "Q"):
                    actions = Queen((i, j))
                elif(board[i][j].name == "`"):
                    continue
                if (board[i][j].name != "`"and (board[i][j].name.isupper())):
                    for a in actions:
                        if(len(a)>2):
                            print("er22",board[i][j].name)
                        allActions.append(a)
    elif max_player==False:
        for i in range(0,8):
            for j in range(0, 8):
                if(board[i][j].name=="p"):
                    actions = blackPawn((i, j))
                elif (board[i][j].name == "r"):
                    actions = Rook((i, j))
                elif (board[i][j].name == "n"):
                    actions = Knight((i, j))
                elif (board[i][j].name == "b"):
                    actions = Bishop((i, j))
                elif (board[i][j].name == "k"):
                    actions = King((i, j))
                elif (board[i][j].name == "q"):
                    actions = Queen((i, j))
                elif(board[i][j].name == "`"):
                    continue
                if (board[i][j].name != "`" and (board[i][j].name.islower())):
                    for a in actions:
                        allActions.append(a)
    return allActions



def minimax(board,depth,xGrida,beta,max_player):
    if depth==0 or gameEnd(board):
        return None,evaluation(board)

    moves=getAllMoves(board,max_player)

    if moves==[]:
        return None,

    best_move=random.choice(moves)
    if max_player:
        maxeval=-10000
        for move in moves:
            r_board=result(board,move)
            curr_eval=minimax(r_board,depth-1,xGrida,beta,False)[1]

            if curr_eval>maxeval:
                maxeval=curr_eval
                best_move=move

            xGrida=max(xGrida,curr_eval)
            if beta<=xGrida:
                break

        return best_move,maxeval
    else:
        mineval=10000
        for i,move in enumerate(moves):
            r_board = result(board, move)
            curr_eval = minimax(r_board, depth - 1, xGrida, beta, True)[1]
            if curr_eval<mineval:
                mineval=curr_eval
                best_move=move
            beta=min(beta,curr_eval)
            if beta<=xGrida:
                break
        return best_move,mineval



x1,y1,x2,y2=0,0,0,0
x_dictionary={'8':0,'7':1,'6':2,'5':3,'4':4,'3':5,'2':6,'1':7}
y_dictionary={'a':0,'b':1,'c':2,'d':3,'e':4,'f':5,'g':6,'h':7}
pieceDictionary={'p':"blackPawn",'r':"blackRook",'n':"blackKnight",'b':"blackBishop",'q':"blackQueen",'k':"blackKing",
                 'P':"whitePawn",'R':"whiteRook",'N':"whiteKnight",'B':"whiteBishop",'Q':"whiteQueen",'K':"whiteKing"}


def GetKey(val,dict):
   for key, value in dict.items():
      if val == value:
        #print(key)
        return key
   return "key doesn't exist"


while True:
    x1,y1=input("\nEnter the piece's coordinates(x,y) that you want to move: ")
    old=(x_dictionary[x1],y_dictionary[y1])


    while(not isValidPiece(old)):
        print("Wrong colored piece/blank selected")
        x1, y1=input("\nEnter the piece's coordinates(x,y) that you want to move: ")
        old=(x_dictionary[x1],y_dictionary[y1])

    piece=getPieceAt(old)
    x2,y2=input("Enter your move(x,y): ")
    new=(x_dictionary[x2],y_dictionary[y2]) 

    moves=getLegalmoves(piece)   

    print("USER Selected:"+pieceDictionary[piece.name])

    if piece.getName() == 'k' and (new[0] == 0 and new[1] == 0 ) or (new[0] == 0 and new[1] == 7):
        if piece.getMoved() == False and board[new[0]][new[1]].getMoved() == False:
            m = getCastlingMoves(piece.coordinates[0], piece.coordinates[1], "k" , new)
            if m is not None:
                piece.setMoved(True)
                board[new[0]][new[1]].setMoved(True)
                updateCastlingRights(piece)   
                castleRightsLog.append(
                    CastlingRights(currCastlingRight.wk, currCastlingRight.bk, currCastlingRight.wq, currCastlingRight.bq))
            else:
                print("You cannot castle")   
                x2, y2 = input("Enter your move(x,y): ")
                new = (x_dictionary[x2], y_dictionary[y2])
                while new not in moves:
                    print("Wrong input")
                    x2, y2 = input("Enter your move(x,y): ")
                    new = (x_dictionary[x2], y_dictionary[y2])
                board = result(board, [new, piece])

    else:
        while new not in moves:   
            print("Wrong input")
            x2, y2=input("Enter your move(x,y): ")
            new = (x_dictionary[x2], y_dictionary[y2])
        board = result(board, [new, piece])

    print(grid.yellow+"USER MOVE:"+pieceDictionary[piece.name]+" "+y2+x2+grid.yellow)

    printBoard(board)  

    if checkCheckmate(board): 
        break

    print("\n\n\n\t\t\t\t\t\t <------- AI's turn ------>")
    bestmove,val=minimax(board,4,-10000,10000,True)
    print(grid.green+"AI'S MOVE:"+pieceDictionary[bestmove[1].name]+" "+GetKey(bestmove[0][1],y_dictionary)+GetKey(bestmove[0][0],x_dictionary)+grid.RESET)
    board=result(board,bestmove)   
    printBoard(board)   
    if checkCheckmate(board):  
        break

