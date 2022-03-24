class Board:
    #board object initialization depending on input computer either chooses moves for X or O
    def __init__(self, state, player):
        self.state = state
        print('dev 2')
        if player == 'X':
            self.player = 'X' 
            self.opponent = 'O'
        else:
            self.player = 'O' 
            self.opponent = 'X'
        
    # object method to detect X/O win or draw
    def evaluate(self):
        
        # check rows for win
        for row in range(3):
            if (self.state[row][0] == self.state[row][1] and self.state[row][1] == self.state[row][2]) :       
                if (self.state[row][0] == self.player) :
                    return 10
                elif (self.state[row][0] == self.opponent) :
                    return -10
        
        # check columns for win
        for col in range(3):
            if (self.state[0][col] == self.state[1][col] and self.state[1][col] == self.state[2][col]) :       
                if (self.state[0][col] == self.player) :
                    return 10
                elif (self.state[0][col] == self.opponent) :
                    return -10
        
        # check diagonals for win
        if (self.state[0][0] == self.state[1][1] and self.state[1][1] == self.state[2][2]):           
            if (self.state[0][0] == self.player) :
                return 10
            elif (self.state[0][0] == self.opponent) :
                return -10
        
        if (self.state[0][2] == self.state[1][1] and self.state[2][0] == self.state[1][1]):
            if (self.state[1][1] == self.player):
                return 10   
            elif (self.state[1][1] == self.opponent):
                return -10
        return 0
        
       
                
                
                
    # method to detect if any moves are left to play           
    def isMovesLeft(self):
        for i in range(3):
            for j in range(3):
                 if (self.state[i][j] == '_') :         
                     return True
        return False
        
    # minimax function to find optimal move
    def minimax(self, depth, isMax):
        score = self.evaluate()
        
        # if computer player wins
        if (score == 10) :
            return score
        # if opponent player  wins               
        if (score == -10) :
            return score  
        # if no moves left return draw   
        if (self.isMovesLeft() == False) :
            return 0
            
        # if maximizers move
        if (isMax) :
            best = -1000
            print(self.state)
            for i in range(3) :
                for j in range(3):
                    
                    # if move is available calculate score and next move
                    if (self.state[i][j]=='_') :
                        
                        #take move
                        self.state[i][j] = self.player
                        
                        # recursive call to minimax function, best either equals new move score or old one
                        best = max( best, (self.minimax(depth+1, False)))
                    	 
                    	 # undo most recent move
                        self.state[i][j] = '_'
            # return best score
            return best
        else :
            # else minimizers move
            
            best = 1000
            
            for i in range(3) :
                for j in range(3):
                    
                    # if move is available calculate score and next move
                    if (self.state[i][j] == '_'):
                    
                        #take move
                        self.state[i][j] = self.opponent
                        
                        # recursive call to minimax function, best either equals new move score or old one
                        best = min(best, (self.minimax( depth+1, True)))
                        
                        # undo most recent move
                        self.state[i][j] = '_'
                        
            return best



    #pilot function for minimax algorithm
    def findBestMove(self) :
        
        bestVal = -1000
        bestMove = (-1, -1)
        for i in range(3):
            for j in range(3):
                if (self.state[i][j] == '_'):
                    self.state[i][j] = self.player
                    moveVal = self.minimax(0, False)
                    self.state[i][j] = '_'
                    
                    if (moveVal > bestVal) :
                        bestMove = (i,j)
                        bestVal = moveVal
        return bestMove            

           
         
                                                 
                        
                    
                    
                    

