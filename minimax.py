WIN_POS = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
           (0, 3, 6), (1, 4, 7), (2, 5, 8),
           (0, 4, 8), (2, 4, 6)]

# Visualization of WIN_POS
"""
X X X   . . .   . . .
. . .   X X X   . . .
. . .   . . .   X X X

X . .   . X .   . . X
X . .   . X .   . . X
X . .   . X .   . . X

X . .       . . X
. X .       . X .
. . X       X . .

"""


# iterates over WIN_POS to check if one of the players has won,
# if not then checks if it's a draw.
def game_over(x_plays: set, o_plays: set):
    for pos in WIN_POS:
        if pos[0] in x_plays and pos[1] in x_plays and pos[2] in x_plays:
            # X won
            return True
        if pos[0] in o_plays and pos[1] in o_plays and pos[2] in o_plays:
            # O won
            return True

    # draw
    if len(x_plays) == 4 and len(o_plays) == 5 or len(x_plays) == 5 and len(o_plays) == 4:
        return True

    # game is not over yet
    return False


# this doesn't need a comment because it's pretty self explanatory however I made the longest comment on it explaining
# that it doesn't need a comment. congratulations, you've played yourself.
def can_play(x_plays, o_plays, i):
    return False if i in x_plays or i in o_plays else True


class Play:
    def __init__(self, x_plays: set, o_plays: set):
        self.x_plays = x_plays
        self.o_plays = o_plays
        self.children = []  # list of Play containing all possible moves
        self.generate_children()
        self.value = minimax(self.depth(), True if len(x_plays) > len(o_plays) else False, self)

    # calculate static value
    # returns -1 if X wins in this play,
    # 1 if O wins in this play,
    # and 0 if it is a draw.
    def sv(self):
        for pos in WIN_POS:
            if pos[0] in self.x_plays and pos[1] in self.x_plays and pos[2] in self.x_plays:
                # X won
                return -1
            if pos[0] in self.o_plays and pos[1] in self.o_plays and pos[2] in self.o_plays:
                # O won
                return 1
        # draw
        return 0

    # generate all possible plays
    def generate_children(self):
        if not game_over(self.x_plays, self.o_plays):
            # generate all possible O plays if it's O's turn (X is more than O on board)
            if len(self.x_plays) > len(self.o_plays):
                for i in range(9):
                    if not (i in self.o_plays) and not (i in self.x_plays):
                        new_o_plays = self.o_plays.copy()
                        new_o_plays.add(i)
                        self.children.append(Play(self.x_plays, new_o_plays))

            # generate all possible X plays if it's X's turns (O is equal to X on board)
            else:
                for i in range(9):
                    if not (i in self.x_plays) and not (i in self.o_plays):
                        new_x_plays = self.x_plays.copy()
                        new_x_plays.add(i)
                        self.children.append(Play(new_x_plays, self.o_plays))

    def depth(self):
        return 9 - len(self.x_plays) - len(self.o_plays)


# Minimax algorithm: minimizing maximum loss.
def minimax(depth: int, maximizer: bool, play: Play):
    # end game or leaf node
    if depth == 0 or game_over(play.x_plays, play.o_plays):
        return play.sv()

    # the maximizer always looks for maximum value between nodes
    if maximizer:
        # set value to -infinity, because all numbers are bigger than -infinity
        play.value = float('-inf')
        # look for node with biggest value and return it
        for node in play.children:
            play.value = max(play.value, minimax(depth - 1, False, node))
        return play.value

    # the minimizer always looks for minimum value between nodes
    else:  # minimizer
        # set value to infinity, because all numbers are smaller than infinity
        play.value = float('inf')
        # look for node with smallest value and return it
        for node in play.children:
            play.value = min(play.value, minimax(depth - 1, False, node))
        return play.value
