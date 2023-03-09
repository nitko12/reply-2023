import sys

test_file_name = sys.argv[1]
sol_file_name = sys.argv[2]

with open(test_file_name, "r") as test_file:
    [w, h, sn] = [int(x) for x in test_file.readline().strip().split()]
    # print(w)
    # print(h)
    # print(sn)
    snake_lengths = [int(x) for x in test_file.readline().strip().split()]
    # print(snake_lengths)
    field = [test_file.readline().strip().split() for i in range(h)]
    # print(field)

    visited = [[-1 for j in range(w)] for i in range(h)]

final_score = 0

with open(sol_file_name, "r") as sol_file:
    for idx, sl in enumerate(snake_lengths):
        [sx, sy, *moves] = sol_file.readline().strip().split()
        sx = int(sx)
        sy = int(sy)

        if len(moves) < sl - 1:
            raise Exception(f"There are less moves than needed for snake {idx}")

        if sy < 0 or sy >= h or sx < 0 or sx >= w:
            raise Exception(f"Starting position [{sx}, {sy}] out of range [0-{w-1}, 0-{h-1}]")
        if field[sy][sx] == '*':
            raise Exception(f"Snake {idx} cannot start at the wormhole [{sx}, {sy}].")

        move_idx = 0
        moves_done = 0

        final_score += int(field[sy][sx])

        print(f"Snake {idx}:\t", end="")
        print(int(field[sy][sx]), end=" ")
        
        while moves_done < sl - 1:
            if (field[sy][sx] != '*' and visited[sy][sx] != -1):
                raise Exception(f"Snake {idx} stepped on the same spot as snake {visited[sy][sx]} - [{sx}, {sy}].")

            visited[sy][sx] = idx
            move = moves[move_idx]
            if move == 'D':
                sy = (sy + 1) % h
            elif move == 'U':
                sy = (sy - 1 + h) % h
            elif move == 'R':
                sx = (sx + 1) % w
            elif move == 'L':
                sx = (sx - 1 + w) % w
            else:
                raise Exception(f"Unknown token for snake {idx} on move {move_idx} (0-indexed, after starting coordinates).")

            if field[sy][sx] == '*':
                sx = int(moves[move_idx + 1])
                sy = int(moves[move_idx + 2])
                if field[sy][sx] != '*':
                    raise Exception(f"Snake {idx} tried to teleport to [{sx}, {sy}] which is not a wormhole.")

                move_idx += 3
            else:
                final_score += int(field[sy][sx])
                print(int(field[sy][sx]), end=" ")
                move_idx += 1

            moves_done += 1

        print("")
        print(f"Snake {idx} finished on [{sx}, {sy}] which has value of {field[sy][sx]}.")

        if move_idx != len(moves):
            raise Exception(f"There are more moves than needed for snake {idx}.")


if final_score < 0:
    raise Exception(f"Final score is {final_score}, which is less than zero!")

print(f"Final score is {final_score}")