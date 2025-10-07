"""

RUN: python3 test_seed.py
"""

import copy
import random
import game  # import your game.py functions

def assert_eq(a, b, msg=""):
    if a != b:
        raise AssertionError(f"Assertion failed: {a} != {b}. {msg}")

# --- Core deterministic tests ---
def board_from_rows(rows):
    return [r[:] for r in rows]

def test_single_merge_per_move():
    row = [2, 2, 2, 0]
    result = game.mergeOneRowLeft(row)
    assert_eq(result, [4, 2, 0, 0], "Single merge per move failed.")

def test_merge_directions():
    board = [
        [2, 2, 4, 4],
        [0, 0, 0, 0],
        [2, 0, 2, 0],
        [4, 4, 8, 8],
    ]
    left_result = game.merge_left(copy.deepcopy(board))
    right_result = game.merge_right(copy.deepcopy(board))
    up_result = game.merge_up(copy.deepcopy(board))
    down_result = game.merge_down(copy.deepcopy(board))

    assert_eq(left_result[0], [4, 8, 0, 0], "Left merge failed.")
    assert_eq(right_result[0], [0, 0, 4, 8], "Right merge failed.")
    assert_eq(up_result[0][0] != 0, True, "Up merge failed.")
    assert_eq(down_result[-1][-1] != 0, True, "Down merge failed.")

def test_no_spawn_on_illegal_move():
    board = [
        [2, 4, 8, 16],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]
    before = copy.deepcopy(board)
    after = game.merge_left(copy.deepcopy(board))
    assert_eq(after, before, "Illegal move changed the board unexpectedly.")

def test_game_over():
    board = [
        [2, 4, 2, 4],
        [4, 2, 4, 2],
        [2, 4, 2, 4],
        [4, 2, 4, 2],
    ]
    assert_eq(game.noMoves(board), True, "Game over not detected correctly.")

def test_pick_new_value():
    vals = {game.pickNewValue() for _ in range(50)}
    assert vals.issubset({2, 4}), f"Unexpected tile values: {vals}"

# --- Randomized legality + determinism tests ---
def random_board(seed=0):
    random.seed(seed)
    board = [[0] * 4 for _ in range(4)]
    game.addNewValue(board)
    game.addNewValue(board)
    return board

def apply_move(board, move):
    """Call the appropriate move function."""
    move = move.lower()
    if move == "a":
        return game.merge_left(copy.deepcopy(board))
    if move == "d":
        return game.merge_right(copy.deepcopy(board))
    if move == "w":
        return game.merge_up(copy.deepcopy(board))
    if move == "s":
        return game.merge_down(copy.deepcopy(board))
    return board

def simulate_sequence(seed=0, moves=100):
    """Run random move sequences and ensure legality + determinism."""
    random.seed(seed)
    dirs = ["w", "a", "s", "d"]

    def play_once():
        board = random_board(seed)
        for _ in range(moves):
            m = random.choice(dirs)
            before = copy.deepcopy(board)
            after = apply_move(board, m)
            if after != before:
                # legal move → new tile should be added
                game.addNewValue(after)
            board = after
            if game.noMoves(board):
                break
        return board

    b1 = play_once()
    b2 = play_once()
    assert_eq(b1, b2, "Game state not deterministic between runs.")

def run_all_tests():
    print("Running deterministic function tests...")
    test_single_merge_per_move()
    test_merge_directions()
    test_no_spawn_on_illegal_move()
    test_game_over()
    test_pick_new_value()
    print("Core deterministic tests passed.\n")

    print("Running random legality + determinism simulation...")
    simulate_sequence(seed=24, moves=100)
    simulate_sequence(seed=99, moves=150)
    print("Random legality & determinism tests passed.\n")

    print("All tests passed successfully.")

if __name__ == "__main__":
    run_all_tests()
