from math import floor
from minimax import Play, can_play, game_over
import pygame

# initialize
pygame.init()
pygame.display.set_caption("tic tac toe")

# loading assets
GRID = pygame.image.load("assets/grid_img.png")
FONT = pygame.font.Font("assets/PressStart2P.ttf", 40)

# constants
WIDTH, HEIGHT = 300, 300
BG_COLOR = (255, 255, 255)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60


def main():
    player = 1  # {X, O} = {1, 0}
    running = True
    x_plays = set()
    o_plays = set()

    # returns list of 2 tuples containing x and y ranges of i-th grid
    def get_part_of_grid(i):
        # [(x1, x2), (y1, y2)]
        return [(0 + 100 * (i % 3), 100 + 100 * (i % 3)), (0 + 100 * floor(i / 3), 100 + 100 * floor(i / 3))]

    # return index of grid which contains x, y
    def get_index_of_grid(x, y):
        for i in range(9):
            pos = get_part_of_grid(i)
            if pos[0][0] <= x <= pos[0][1] and pos[1][0] <= y <= pos[1][1]:
                return i

    # draws X and O plays on screen
    def draw_players():
        X = FONT.render("X", True, (0, 0, 0))
        O = FONT.render("O", True, (0, 0, 0))
        for i in x_plays:
            # draw X
            pos = get_part_of_grid(i)
            SCREEN.blit(X, (int(pos[0][0] + 50 - 40 / 2), int(pos[1][0] + 50 - 40 / 2)))
        for i in o_plays:
            # draw O
            pos = get_part_of_grid(i)
            SCREEN.blit(O, (int(pos[0][0] + 50 - 40 / 2), int(pos[1][0] + 50 - 40 / 2)))

    # updates screen
    def draw_screen():
        SCREEN.fill(BG_COLOR)
        SCREEN.blit(GRID, (0, 0))
        draw_players()
        pygame.display.update()

    # main loop
    while running:
        draw_screen()
        if game_over(x_plays, o_plays):
            running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    # if player is X (human)
                    if player == 1:
                        (x, y) = pygame.mouse.get_pos()
                        if 0 <= x <= 300 and 0 <= y <= 300:
                            i = get_index_of_grid(x, y)
                            if can_play(x_plays, o_plays, i):
                                x_plays.add(i)

                    # if player is O (computer)
                    else:
                        play = Play(x_plays, o_plays)
                        # searches for child with the value given to itself
                        for child in play.children:
                            if child.value == play.value:
                                # updates global positions of O with new child's positions
                                o_plays.update(child.o_plays)
                                break

                # switch player
                player = (player + 1) % 2

            # quit handling
            if event.type == pygame.QUIT:
                running = False

        CLOCK.tick(FPS)


main()
