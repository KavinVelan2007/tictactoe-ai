import pygame

pygame.init()
pygame.font.init()

class Game:

    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width,self.height))
        self.font = pygame.font.SysFont('comicsans',150)
        self.small_font = pygame.font.SysFont('comicsans',30)
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.ai = 'O'
        self.human = 'X'
        self.scores = {self.ai: 1,
                       self.human: -1,
                       'Tie': 0}
        self.turn = self.human
        self.MIN = -float('inf')
        self.MAX = float('inf')

    def main(self):
        run = True
        while run:
            if self.turn == self.ai and not self.checkWinner():
                self.bestMove()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    key = pygame.mouse.get_pressed()
                    if key[0]:
                        x,y = pygame.mouse.get_pos()
                        col,row = x // (self.width // 3),y // (self.height // 3)
                        if self.board[row][col] == '':
                            if self.turn == self.human and not self.checkWinner():
                                self.board[row][col] = self.human
                                self.turn = self.ai
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.width,self.height)

            self.draw(self.display)

        pygame.quit()

    def bestMove(self):
        bestScore = -float("inf")
        move = (0,0)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == '':
                    self.board[row][col] = self.ai
                    score = self.minimax(self.board,0,False,self.MIN,self.MAX)
                    self.board[row][col] = ''
                    if score > bestScore:
                        bestScore = score
                        move = (row,col)
        
        row,col = move
        self.board[row][col] = self.ai
        self.turn = self.human
                    
    def minimax(self,board,depth,isMaximizing,alpha,beta):
        result = self.checkWinner()
        if result:
            return self.scores.get(result)
        if isMaximizing:
            bestScore = -float("inf")
            for row in range(len(board)):
                for col in range(len(board[row])):
                    if board[row][col] == '':
                        board[row][col] = self.ai
                        score = self.minimax(board,depth + 1,False,alpha,beta)
                        board[row][col] = ''
                        bestScore = max(score,bestScore)
                        alpha = max(alpha,score)
                        if alpha >= beta:
                            break
            return bestScore
        else:
            bestScore = float("inf")
            for row in range(len(board)):
                for col in range(len(board[row])):
                    if board[row][col] == '':
                        board[row][col] = self.human
                        score = self.minimax(board,depth + 1,True,alpha,beta)
                        board[row][col] = ''
                        bestScore = min(score,bestScore)
                        beta = min(beta,score)
                        if alpha >= beta:
                            break
            return bestScore
        
    def checkWinner(self):
        board = self.board
        winner = None
        #Vertical
        for i in range(3):
            if board[0][i] == board[1][i] == board[2][i]:
                if board[0][i] != '':
                    winner = board[0][i]
        #Horizontal
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2]:
                if board[i][0] != '':
                    winner = board[i][0]
        #Diagonal
        if board[0][0] == board[1][1] == board[2][2] or board[0][2] == board[1][1] == board[2][0]:
            if board[1][1] != '':
                winner = board[1][1]
        openSpots = 0
        for i in board:
            for j in i:
                if j == '':
                    openSpots = 1
                    break
        if winner is None and not openSpots:
            return 'Tie'
        else:
            return winner

    def draw(self,win):
        win.fill((255,255,255))
        for x in range(0,self.width,self.width // 3):
            pygame.draw.line(win,(0,0,0),(x,0),(x,self.height),5)
        for y in range(0,self.height,self.height // 3):
            pygame.draw.line(win,(0,0,0),(0,y),(self.width,y),5)
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == 'X':
                    x,y = col * (self.width // 3),row * (self.height // 3)
                    pygame.draw.line(win,(0,0,0),(x,y),(x + self.width // 3,y + self.height // 3),8)
                    pygame.draw.line(win,(0,0,0),(x + self.width // 3,y),(x,y + self.height // 3),8)
                elif self.board[row][col] == 'O':
                    x,y = col * (self.width // 3) + (self.width // 3 // 2),row * (self.height // 3) + (self.height // 3 // 2)
                    pygame.draw.circle(win,(0,0,0),(x,y),self.width // 3 // 2,5)
        self.displayText(win,self.font,self.small_font)
        pygame.display.update()

    def displayText(self,win,font,small_font):
        text = small_font.render('Press \'r\' to Restart',True,(255,0,0))
        win.blit(text,(10,0))
        winner = self.checkWinner()
        if winner:
            if winner == self.ai:
                text = font.render(f'{winner} Won!',True,(255,0,0))
                win.blit(text,(140,250))
            elif winner == self.human:
                text = font.render(f'{winner} Won!',True,(0,0,255))
                win.blit(text,(140,250))
            elif winner == 'Tie':
                text = font.render(winner,True,(255,0,0))
                win.blit(text,(250,250))

game = Game(750,750)
game.main()
