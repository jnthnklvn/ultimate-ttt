class UltimateTicTacToe(Game):

    ## variaveis iniciais e de configuração
    ## win_resul armazena as posições de todas as vitorias
    win_resul = [(0,4,8),(2,4,6)]
    win_resul += [(i, i+3, i+6) for i in range(3)]
    win_resul += [(i*3, i*3+1, i*3+2) for i in range(3)]
    
    def __init__(self, h=3, v=3, k=3):
        self.h = h
        self.v = v
        self.k = k
        
        ## last_move indica em qual quadrado deverá ser a proxima jogada(-1 significa qualquer lugar)
        self.last_move = -1
        ## moves contem todos os espaços livre para movimentos
        self.moves = [(i,j) for i in range(9)
                for j in range(9)]
        moves_now = self.moves.copy() ## será atualizada de acordo com a ultima jogada
        
        self.cont = 0
        
        board = [['F']*9 for _ in range(9)]
        
        self.initial = GameState(to_move='X', utility=0, board=board, moves=moves_now)

    ## recebe estado e movimento e retorna um estado com a atualização do movimento
    def result(self, state, move):
        if move not in state.moves:
            return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                             utility=self.compute_utility(state.board, move, state.to_move),
                             board=state.board, moves=state.moves)
        (x, y) = move
        board = state.board.copy()
        board[x][y] = state.to_move
        
        if(self.small_win(board[x])):
            for idx in self.moves:
                (i, j) = idx
                if (i==x):
                    print(idx, "idx removido")
                    print(self.moves)
                    self.moves.remove(idx)
        else:
            ##print(move)
            print(move, "move removido")
            self.moves.remove(move)
        
        self.last_move = self.next_move(board, y)
        moves_now = self.actions(state)
        
        print(self.moves)
        print(moves_now)
        self.display(state)
        
        self.cont +=1
        print(self.cont)
        return GameState(to_move=('O' if state.to_move == 'X' else 'X'),
                         utility=self.compute_utility(board, move, state.to_move),
                         board=board, moves=moves_now)

    ## imprime o tabuleiro
    def display(self, state):
        for h in range(3):
            print("-"*25)
            for i in range(3):
                line = "| "
                for j in range(3):
                    line += state.board[j+h*3][i*3] + " " + state.board[j+h*3][i*3+1] + " " + state.board[j+h*3][i*3+2] + " | "
                print(line)
        print("-"*25 +"\n")
    
    ## verifica se há vencedor num dado quadrado
    def small_win(self, square):
        for i in self.win_resul:
            (x, y, z) = i
            square_x = square[x]
            ## print(i)
            if(square_x == square[y] == square[z]) and (square_x != 'F'):
                return True
        return False

    ## verifica se há vencedor no tabuleiro
    def big_win(self, board):
        for i in self.win_resul:
            (x, y, z) = i
            small_x = self.small_win(board[x])
            if(small_x == self.small_win(board[y]) == self.small_win(board[z])) and (small_x != 'F'):
                return True
        return False

    ## verifica se o quadrado está todo preenchido
    def small_draw(self, square):
        for i in square:
            if(i=='F'):
                return False
        return True
    
    ## verifica empate no tabuleiro
    def big_draw(self, board):
        for i in board:
            if not(self.small_draw(i) or self.small_win(i)):
                return False
        return True

    ## verifica se no quadrado indicado pela ultima jogada há vitoria ou empate, caso haja last_move passa a ser -1
    def next_move(self, board, last_move):
        target_square = board[last_move]
        if(self.small_win(target_square) or self.small_draw(target_square)):
            print(self.small_win(target_square), self.small_draw(target_square))
            return -1
        else:
            return last_move
    
    def eval_function(self, state, player):
            v = 0
            oponent = 'O' if player == 'X' else 'X'
            
            for x in range(0, 9):
                for y in range(0, 9):
                    if state.board[x][y] == player:
                        v += 2 if (y % 2) == 1 else 3 if (not (x == 0)) else 4
                    elif state.board[x][y] == oponent:
                        v -= 2 if (y % 2) == 1 else 3 if (not (x == 0)) else 4
            u = self.utility(state, player)
            return u if not u == 0 else v

    ## redefine os movimentos legais de acordo com a ultima jogada
    def actions(self, state):
        if (self.last_move == -1):
            return self.moves
        else:
            moves_now = []
            for i in self.moves:
                x, _ = i
                if(x==self.last_move):
                    moves_now.append(i)
            return moves_now

    ## verifica se existe determinado elemento em uma lista
    def contains(self, array, el):
        for i in array:
            if (i==el):
                return True
        return False
    
    ## recebe o tabuleiro, as posições da jogada e o jogador, e retorna se a jogada é válida
    ## x é o numero do quadrado a ser jogado e y a posição nele
    def player_move(self, board, move, player):
        (x, y) = move
        if(self.contains(self.moves, move)):
            board[x][y] = player
            return True, board
        else:
            return False, board

    ## retorna o valor de utilidade do estado. 1, -1, 0 (vitoria, derrota e nenhum)
    def utility(self, state, player):
        return state.utility if player == 'X' else -state.utility
    
    ## calcula valor de utilidade
    def compute_utility(self, board, move, player):
        (x, y) = move
        true, board  = self.player_move(board, move, player)
        if(true and self.small_win(board[x])):
            if(self.big_win(board)):
                return 1000 ## utilidade para grande vitoria
            return 200 ## utilidade para pequena vitoria
        return 0 ## utilidade caso não haja vitoria
    
    ## verifica se o jogo acabou
    def terminal_test(self, state):
        return len(state.moves) == 0