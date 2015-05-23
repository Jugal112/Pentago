'''
Created on May 11, 2015

@author: Jugal112
'''
from Player import Player
import re
import copy
import sys
import random;
class GameBoard:
        
    player1 = Player("player1","B")
    player2 = Player("player2","W")
    #computer = False means to turn the AI off. when it's True,
    #then player 1 can play the computer.
    computer = False;
    turn = 0
    matrix = [["-" for z in range(6)] for z in range(6)];
    moves=[]
    
    '''
    display the board.
    '''
    def display(self, mtrx = matrix):
        print "+---1---+---2---+"
        for i in self.matrix[0:3]:
            print ("| " + " ".join(i[0:3]) + " | " + " ".join(i[3:6]) + " |")
        print "+-------+-------+"
        for i in self.matrix[3:6]:
            print ("| " + " ".join(i[0:3]) + " | " + " ".join(i[3:6]) + " |")
        print "+---3---+---4---+"
            
    def set(self, x, y, p):
        self.matrix[x][y]=p
    
    '''
    rotate the board.
    '''
    def rotate(self, gameBlock, direction):
        if (direction=="L"):
            rotatedMatrix=copy.deepcopy(self.matrix);
            rowOffset = ((gameBlock-1)/2)*3 ;
            colOffset = ((gameBlock-1)%2)*3 ;
            for i in range(0, 3):
                for j in range(0, 3):
                    self.matrix[3-j-1+rowOffset][i+colOffset] = rotatedMatrix[i+rowOffset][j+colOffset]

        elif (direction=="R"):
            rotatedMatrix=copy.deepcopy(self.matrix);
            rowOffset = ((gameBlock-1)/2)*3 ;
            colOffset = ((gameBlock-1)%2)*3 ;
            for i in range(0, 3):
                for j in range(0, 3):
                    self.matrix[i+rowOffset][j+colOffset] = rotatedMatrix[3-j-1+rowOffset][i+colOffset]
    '''
    prompt user for a move.
    '''
    def getCommand(self, Player):
        print Player.name
        s = raw_input("What move would you like to make?").upper()
        while (not (self.checkInput(s))):
            s = raw_input("That's not a legal move. Try again.").upper()
            
        if s=="P":
            self.menu(p=1)
        else:
            self.makeMove(s, Player);
    
    def makeMove(self, s, Player):
        coordinates = self.parseMove(s);
        tileRow = coordinates[0];
        tileCol = coordinates[1];
        if (not self.validMove(tileRow,tileCol)):
            print "You cannot go there"
            self.getCommand(Player)
        else:
            self.set(tileRow, tileCol, Player.token)
            self.whoWon(self.checkWin());
            self.rotate(int(s[4]),s[5]);
            self.moves.append(s)
            self.whoWon(self.checkWin());
    '''
    Parse the move so that I can deal with coordinates rather than
    game board actions and make this more mathematical.
    '''
    def parseMove(self, s):
        rowOffset = ((int(s[0])-1)%2)*3;
        colOffset = ((int(s[0])-1)/2)*3 ;
        tileCol = (int(s[2])-1)%3 + rowOffset;
        tileRow = (int(s[2])-1)/3 + colOffset;
        return [tileRow, tileCol]
    
    '''
    Check if the move is valid by seeing if that spot on the board
    is taken.
    ''' 
    def validMove(self, tileRow, tileCol):
        if (self.matrix[tileRow][tileCol]==self.player1.token) or (self.matrix[tileRow][tileCol]==self.player2.token):
            return False
        else:
            return True
    
    '''
    Start a new game
    '''
    def newGame(self):
        self.player1.name = raw_input("Player 1. Enter your name")
        if self.computer==False:
            self.player2.name = raw_input("Player 2. Enter your name")
        else:
            self.player2.name = "AI"
        self.playGame()
        
    '''
    load the game in from the text file.
    '''
    def loadGame(self):
        f = open("savedGame.txt", "r")
        self.player1.name = f.readline().rstrip('\n')
        self.player2.name = f.readline().rstrip('\n')
        self.player1.token = f.readline().rstrip('\n')
        self.player2.token = f.readline().rstrip('\n')
        self.computer = True if f.readline()=="True" else False;
        self.turn = int(f.readline().rstrip('\n'))
        for i in range(0,6):
            self.matrix[i]=list(f.readline().upper().rstrip('\n'));
        self.whoWon(self.checkWin())
        self.playGame()
        pass
    
    '''
    Save the game down to  text file.
    '''
    def saveGame(self):
        f = open('savedGame.txt', "w")
        f.write(self.player1.name+"\n");
        f.write(self.player2.name+"\n");
        f.write(self.player1.token+"\n");
        f.write(self.player2.token+"\n");
        f.write(str(self.computer));
        f.write(str(self.turn)+"\n")
        for i in self.matrix:
            f.write("".join(i)+"\n");
        for i in self.moves:
            f.write(i+"\n");
        f.close();
        pass
    
    '''
    quit game
    '''
    def quit(self):
        sys.exit();
    
    '''
    check board for all possible ways of winning with a row of 5.
    return the tuple of winners so that the whoWon() function can
    determine what to do.
    
    This function is separated because I need it for the AI to
    check if it wins.
    '''
    def checkWin(self):
        p1=False;
        p2=False;
        #check rows
        for i in self.matrix:
            if (i[0]==i[1]==i[2]==i[3]==i[4]) or (i[1]==i[2]==i[3]==i[4]==i[5]):
                if i[3]==self.player1.token:
                    p1=True;
                elif i[3]==self.player2.token:
                    p2=True
        #check columns
        rotatedMatrix = copy.deepcopy(self.matrix);
        for i in range(0, 6):
            for j in range(0, 6):
                rotatedMatrix[i][j] = self.matrix[6-j-1][i]
        for i in rotatedMatrix:
            if (i[0]==i[1]==i[2]==i[3]==i[4]) or (i[1]==i[2]==i[3]==i[4]==i[5]):
                if i[3]==self.player1.token:
                    p1=True;
                elif i[3]==self.player2.token:
                    p2=True
        #check diagonals
        m = self.matrix
        if m[0][0]==m[1][1]==m[2][2]==m[3][3]==m[4][4] or m[1][1]==m[2][2]==m[3][3]==m[4][4]==m[5][5]:
            if m[3][3]==self.player1.token:
                p1=True;
            elif m[3][3]==self.player2.token:
                p2=True;        
        if m[0][5]==m[1][4]==m[2][3]==m[3][2]==m[4][1] or m[1][4]==m[2][3]==m[3][2]==m[4][1]==m[5][0]:
            if m[3][2]==self.player1.token:
                p1=True;
            elif m[3][2]==self.player2.token:
                p2=True;
        if m[0][5]==m[1][4]==m[2][3]==m[3][2]==m[4][1] or m[1][4]==m[2][3]==m[3][2]==m[4][1]==m[5][0]:
            if m[3][2]==self.player1.token:
                p1=True;
            elif m[3][2]==self.player2.token:
                p2=True;
        if m[0][1]==m[1][2]==m[2][3]==m[3][4]==m[4][5]:
            if m[2][3]==self.player1.token:
                p1=True;
            elif m[2][3]==self.player2.token:
                p2=True;
        if m[1][0]==m[2][1]==m[3][2]==m[4][3]==m[5][4]:
            if m[3][2]==self.player1.token:
                p1=True;
            elif m[3][2]==self.player2.token:
                p2=True;
        if m[0][4]==m[1][3]==m[2][2]==m[3][1]==m[4][0]:
            if m[2][2]==self.player1.token:
                p1=True;
            elif m[2][2]==self.player2.token:
                p2=True;
        if m[1][5]==m[2][4]==m[3][3]==m[4][2]==m[5][1]:
            if m[3][3]==self.player1.token:
                p1=True;
            elif m[3][3]==self.player2.token:
                p2=True;
                
        return(p1, p2);
        #check for tie or winner        
    '''
    see if the game is a tie or if just one player one and
    then display the appropriate message
    '''
    def whoWon(self,(p1, p2)):
        if p1==True or p2==True:
            self.display();
            if p1==True and p2==True:
                print self.player1.name,"and",self.player2.name,"tied!"
                self.quit();
            elif p1==True:
                print self.player1.name, "wins!"
                self.quit();
            elif p2==True:
                print self.player2.name, "wins!"
                self.quit();
    
    '''
    display the menu to start the game and let the player choose what
    they want to do.
    '''    
    def menu(self, p=0):
        choices=["1","2","3","4"]
        print "1) New Game"
        print "2) Load Game"
        print "3) Save Game"
        print "4) Quit"
        if p==1:
            choices.append("5")
            print "5) Resume Game"
        response=None;
        while (choices.count(response)==0):
            response = raw_input("Please select an item from the menu.")
        print "You chose",response
        if(response=="1"):
            self.menu2()
        elif(response=="2"):
            self.loadGame()
        elif(response=="3"):
            self.saveGame()
        elif(response=="4"):
            self.quit()
        elif(response=="5"):
            self.playGame()
    
    '''
    submenu to choose AI or another human player
    '''        
    def menu2(self):
        choices=["1","2"];
        print "1)Player vs Player"
        print "2)Player vs AI"
        response=None;
        while (choices.count(response)==0):
            response = raw_input("Please select an item from the menu.")
        if(response=="2"):
            self.computer = True
        self.newGame();
    '''
    start the game and prompt player 2 or the computer
    for their move depending on what player 1 chose to play
    '''    
    def playGame(self):
        p=None
        while(True):
            self.display()
            if self.turn%2==0:
                p = self.player1;
                self.getCommand(p)
            else:
                p = self.player2;
                if self.computer is False:
                    self.getCommand(p)
                else:
                    self.AIMakeMove();
            self.turn+=1;
    
    '''
    check input if its a valid move for the player's sake.
    '''
    def checkInput(self,s):
        isGood=False
        move = re.compile(r"[1-4][/][1-9] [1-4][R|L]")
        if move.match(s):
            isGood=True
        elif s=="P":
            isGood=True
        return isGood
    
    #===============================================
    #----------------------AI-----------------------
    #===============================================
    '''
    Generate all possible moves for the AI
    '''
    def generateMoves(self):
        movelist = [];
        for i in range(1,5):
            for j in range(1,10):
                for k in range(1,5):
                    for l in range(0,2):
                        move = str(i)+"/"+str(j)+" "+str(k)+["L","R"][l];
                        coordinates=self.parseMove(move);
                        if( self.validMove(coordinates[0], coordinates[1]) ):
                            movelist.append(move);
        return movelist;
        
    '''
    make a random move from the list of generated moves
    as long as they are valid (use validMove()) The AI
    will evaluate the gameboard and then make a move
    accordingly
    '''
    def AIMakeMove(self):
        print "AI making move...";
        p=self.player2;
        moves = self.generateMoves();
        r = random.randint(0,len(moves));
        self.makeMove(moves[r], p);
        
    
    