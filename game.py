import chess

class Game:
    def __init__(self):
        self.board = chess.Board()
        self.moves = []
        
    def __file_to_letter(self, f):
        return chr(ord('a') + f)
        
    def move(self, lift, drop):
        uci = f"{self.__file_to_letter(lift[1])}{lift[0]}{self.__file_to_letter(drop[1])}{drop[0]}"
        move = chess.Move.from_uci(uci)

        # Get SAN *before* pushing the move
        san_move = self.board.san(move)

        self.board.push(move)
        self.moves.append(san_move)

        print(self.moves)