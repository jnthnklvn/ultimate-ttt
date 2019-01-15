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
        
        moves = ini_moves()
        
        self.initial = GameState(to_move='X', utility=0, board={}, moves=moves)

    ## cria e preenche o tabuleiro
    def create_board():
        board = []
        square = ['F', 'F', 'F', 'F', 'F', 'F', 'F', 'F', 'F']
        for i in range(9):
            board.append(square.copy())
        return board

    ## imprime o tabuleiro
    def display(board):
        for h in range(3):
            print("-"*25)
            for i in range(3):
                line = "| "
                for j in range(3):
                    line += board[j+h*3][i*3] + " " + board[j+h*3][i*3+1] + " " + board[j+h*3][i*3+2] + " | "
                print(line)
        print("-"*25)

    ## define todos os movimentos iniciais
    def ini_moves():
        for i in range(9):
            for j in range(9):
                moves.append((i,j))
    
    ## verifica se há vencedor num dado quadrado
    def small_win(square):
        for i in win_resul:
            (x, y, z) = i
            square_x = square[x]
            if(square_x == square[y] == square[z]) and (square[x] != 'L'):
                return square_x
        return 'L'

    ## verifica se há vencedor no tabuleiro
    def big_win(board):
        for i in win_resul:
            (x, y, z) = i
            small_x = small_win(board[x])
            if(small_x == small_win(board[y]) == small_win(board[z])) and (small_win(board[x]) != 'L'):
                return small_x
        return 'L'

    ## verifica se o quadrado está todo preenchido e retorna um boolean correspondente
    def small_full(square):
        for i in square:
            if(i=='L'):
                return False
        return True

    ## verifica se no quadrado indicado pela ultima jogada há vitoria ou empate, caso haja last_move passa a ser -1
    def next_move(board, last_move_now):
        target_square = board[last_move_now]
        if(small_win(target_square) or full_board(target_square)):
            return -1
        else:
            return last_move_now
    
    def eval_function(self, state, player):
            v = 0
            oponent = 'O' if player == 'X' else 'X'
            
            for x in range(0, 9):
                for y in range(0, 9):
                    if state[x][y] == player:
                        v += 2 if (y % 2) == 1 else 3 if (not (x == 0)) else 4
                    elif state[x][y] == oponent:
                        v -= 2 if (y % 2) == 1 else 3 if (not (x == 0)) else 4
            u = self.utility(state, player)
            return u if not u == 0 else v

    ## redefine os movimentos legais de acordo com a ultima jogada
    def actions(last_move_now):
        if (last_move_now == -1):
            return moves
        else:
            moves_now = []
            for i in moves:
                i = x, _
                if(x==last_move_now):
                    moves_now.append(i)
            return moves_now

    ## recebe o tabuleiro, as posições da jogada e o jogador, e retorna se a jogada é válida
    ## x é o numero do quadrado a ser jogado e y a posição nele
    def player_move(board, move, player, moves_now):
        (x, y) = move
        if(moves_now.contains((x,y))):
            ## last_move = y ## atualiza o ultimo movimento pra sabermos qual será o próximo quadrado a ser jogado
            board[x][y] = player
            next_move(board)
            return True, board
        else:
            return False, board
    
    ## retorna o valor de utilidade do estado. 1, -1, 0 (vitoria, derrota e nenhum)
    def utility(state, player):
        return state.utility if player == 'X' else -state.utility
    
    ## calcula valor de utilidade
    def compute_utility(board, move, player):
        (x, y) = move
        test, board  = player_move(board, move, player, actions(move))
        if(test and small_win(board[x])):
            if(big_win(board)):
                return 20 ## utilidade para grande vitoria
            return 1 ## utilidade para pequena vitoria
        return 0 ## utilidade caso não haja vitoria
    
    ## verifica se o jogo acabou
    def terminal_test():
        return utility > 8 or len(moves) == 0
