import chess

board = chess.Board()
sensors = [[r<2 or r>5 for _ in range(8)] for r in range(8)]

new_sensors = [[r<2 or r>5 for _ in range(8)] for r in range(8)]

new_sensors[1][3] = False
new_sensors[3][3] = True

def file_to_letter(f):
    return chr(ord('a') + f)

lift: tuple[int, int] = (0, 0)
drop: tuple[int, int] = (0, 0)

for i in range(8):
    for j in range(8):
        if sensors[i][j] and not new_sensors[i][j]:
            print(f"Sensor at ({i}, {j}) disabled")
            lift = [i, j]
        elif not sensors[i][j] and new_sensors[i][j]:
            print(f"Sensor at ({i}, {j}) enabled")
            drop = [i, j]

board.push(chess.Move.from_uci(f"{file_to_letter(lift[1])}{8-lift[0]}{file_to_letter(drop[1])}{8-drop[0]}"))
print(board)