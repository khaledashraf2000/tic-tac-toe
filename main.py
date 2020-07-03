from math import floor
import pygame

# initialize
pygame.init()
pygame.display.set_caption("tic tac toe")

# constants
WIDTH, HEIGHT = 300, 300
BG_COLOR = (255, 255, 255)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
FPS = 60
WIN_POS = [(0, 1, 2), (3, 4, 5), (6, 7, 8),
           (0, 3, 6), (1, 4, 7), (2, 5, 8),
           (0, 4, 8), (2, 4, 6)]

# loading assets
GRID = pygame.image.load("assets/grid_img.png")
FONT = pygame.font.Font("assets/PressStart2P.ttf", 40)


def get_part_of_grid(i):
    # [(x1, x2), (y1, y2)]
    return [(0 + 100 * (i % 3), 100 + 100 * (i % 3)), (0 + 100 * floor(i / 3), 100 + 100 * floor(i / 3))]


def get_index_of_grid(x, y):
    for i in range(9):
        pos = get_part_of_grid(i)
        if pos[0][0] <= x <= pos[0][1] and pos[1][0] <= y <= pos[1][1]:
            return i


def main():
    # {X, O} = {1, 0}
    player = 1
    x_plays = []
    o_plays = []
    running = True

    def can_play(i):
        return False if i in x_plays or i in o_plays else True

    def isover():
        for pos in WIN_POS:
            if pos[0] in x_plays and pos[1] in x_plays and pos[2] in x_plays:
                return True
            if pos[0] in o_plays and pos[1] in o_plays and pos[2] in o_plays:
                return True

        if len(x_plays) == 4 and len(o_plays) == 5 or len(x_plays) == 5 and len(o_plays) == 4:
            return True

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

    def draw_screen():
        SCREEN.fill(BG_COLOR)
        SCREEN.blit(GRID, (0, 0))
        draw_players()
        pygame.display.update()

    while running:
        draw_screen()

        if isover():
            running = False

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    (x, y) = pygame.mouse.get_pos()
                    if 0 <= x <= 300 and 0 <= y <= 300:
                        i = get_index_of_grid(x, y)
                        if can_play(i):
                            if player == 1:
                                x_plays.append(i)
                            else:
                                o_plays.append(i)
                            # switch player
                            player = (player + 1) % 2

            if event.type == pygame.QUIT:
                running = False

        CLOCK.tick(FPS)


main()
