from game import Game

sensors = [[r<2 or r>5 for _ in range(8)] for r in range(8)]

new_sensors = [[r<2 or r>5 for _ in range(8)] for r in range(8)]

new_sensors[1][3] = False
new_sensors[3][3] = True

lift: tuple[int, int] = (0, 0)
drop: tuple[int, int] = (0, 0)

for i in range(8):
    for j in range(8):
        if sensors[i][j] and not new_sensors[i][j]:
            lift = [i+1, j+1]
        elif not sensors[i][j] and new_sensors[i][j]:
            drop = [i+1, j+1]

game = Game()
game.move(lift, drop)
game.move([7, 3], [5, 3])
game.move([4, 4], [5, 3])

print(game.board)