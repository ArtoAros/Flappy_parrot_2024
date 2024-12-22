import pygame, random, time
from pygame.locals import *
from database import Database


# VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing = 'assets/audio/wing.wav'
hit = 'assets/audio/hit.wav'

pygame.mixer.init()
db = Database()



class Bird(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.images = [pygame.image.load('assets/sprites/pixil-frame-up-last.png').convert_alpha(),
                       pygame.image.load('assets/sprites/pixil-frame-mid-last.png').convert_alpha(),
                       pygame.image.load('assets/sprites/pixil-frame-0-2.png').convert_alpha()]

        self.speed = SPEED

        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/pixil-frame-up-last.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.ima
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        # UPDATE HEIGHT
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]


class Pipe(pygame.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):

    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pygame.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


def show_game_over(score, screen):
    font = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 77)
    game_over_text = font2.render("Game Over", True, (255, 0, 0))
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    retry_text = font.render("Press SPACE to Restart", True, (255, 255, 255))
    exit_text = font.render("Press ESC to Exit", True, (255, 255, 255))

    screen.blit(game_over_text, (SCREEN_WIDTH / 2 - game_over_text.get_width() / 2, SCREEN_HEIGHT / 4))
    # screen.blit(score_text, (SCREEN_WIDTH / 2 - score_text.get_width() / 2, SCREEN_HEIGHT / 2))
    screen.blit(retry_text, (SCREEN_WIDTH / 2 - retry_text.get_width() / 2, SCREEN_HEIGHT / 2.05))
    screen.blit(exit_text, (SCREEN_WIDTH / 2 - exit_text.get_width() / 2, SCREEN_HEIGHT / 1.1))
    pygame.display.update()


def draw_main_menu(screen, clock, game_running, main_menu, reset_game):
    BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (400, 600))

    font = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 77)
    title_text = font2.render("Flappy Bird", True, (255, 255, 255))
    start_button_text = font.render("Press SPACE to start", True, (255, 255, 255))
    results_button_text = font.render("View Results", True, (255, 255, 255))
    exit_button_text = font.render("Exit (ESC)", True, (255, 255, 255))

    outline_title = font2.render("Flappy Bird", True, (0, 0, 0))
    outline_start = font.render("Press SPACE to start", True, (0, 0, 0))
    outline_results = font.render("Flappy Bird", True, (0, 0, 0))
    outline_exit = font.render("Flappy Bird", True, (0, 0, 0))


    highscores_rect = pygame.Rect(SCREEN_WIDTH // 2 - results_button_text.get_width() // 2, 480,
                                  results_button_text.get_width(), results_button_text.get_height())

    exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - exit_button_text.get_width() // 2, 540, exit_button_text.get_width(),
                            exit_button_text.get_height())

    screen.blit(BACKGROUND, (0, 0))

    # screen.blit(outline_title, (SCREEN_WIDTH // 2 - outline_title.get_width() // 2 - 1, SCREEN_HEIGHT / 4 - 1))
    # screen.blit(outline_title, (SCREEN_WIDTH // 2 - outline_title.get_width() // 2 - 1, SCREEN_HEIGHT / 4 + 1))
    # screen.blit(outline_title, (SCREEN_WIDTH // 2 - outline_title.get_width() // 2 + 1, SCREEN_HEIGHT / 4 - 1))
    # screen.blit(outline_title, (SCREEN_WIDTH // 2 - outline_title.get_width() // 2 + 1, SCREEN_HEIGHT / 4 + 1))

    # screen.blit(outline_start, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2 - 1, SCREEN_HEIGHT / 2.05 - 1))
    # screen.blit(outline_start, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2 - 1, SCREEN_HEIGHT / 2.05 + 1))
    # screen.blit(outline_start, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2 + 1, SCREEN_HEIGHT / 2.05 - 1))
    # screen.blit(outline_start, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2 + 1, SCREEN_HEIGHT / 2.05 + 1))

    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT / 4))
    screen.blit(start_button_text, (SCREEN_WIDTH // 2 - start_button_text.get_width() // 2, SCREEN_HEIGHT / 2.05))
    screen.blit(results_button_text, (SCREEN_WIDTH // 2 - results_button_text.get_width() // 2, 480))
    screen.blit(exit_button_text, (SCREEN_WIDTH // 2 - exit_button_text.get_width() // 2, 540))

    pygame.display.update()
    flag_to_quit = False
    flag_to_draw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if highscores_rect.collidepoint(event.pos):
                flag_to_draw = True
                main_menu = False
                break
            elif exit_rect.collidepoint(event.pos):
                flag_to_quit = True
                break
        elif event.type == KEYDOWN:
            if event.key == K_SPACE:  # Start game
                game_running = True
                reset_game = True
                main_menu = False
            elif event.key == K_ESCAPE:  # Exit game
                pygame.quit()
                quit()

    return reset_game, game_running, main_menu, flag_to_draw, flag_to_quit

def draw_results(screen, main_menu, db):
    BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (400, 600))

    font = pygame.font.Font(None, 40)
    font2 = pygame.font.Font(None, 67)
    top_text = font2.render("TOP", True, (255, 255, 255))

    top_scores = db.get_top_scores(5)  # Возвращает список из пяти лучших результатов

    # Отрисовываем фон
    screen.blit(BACKGROUND, (0, 0))
    screen.blit(top_text, (SCREEN_WIDTH // 2 - top_text.get_width() // 2, SCREEN_HEIGHT / 7.3))

    # Отрисовываем результаты
    y_start = SCREEN_HEIGHT * 1.7 / 7
    step = 0.5 / 7
    for i, sc in enumerate(top_scores, start=1):
        text = font.render(f"{i}. Score: {sc}", True, (255, 255, 255))
        screen.blit(text, (27, y_start + (i - 1) * SCREEN_HEIGHT * step))

    exit_button_text = font.render("Exit (ESC)", True, (255, 255, 255))
    exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - exit_button_text.get_width() // 2, 540, exit_button_text.get_width(),
                            exit_button_text.get_height())
    screen.blit(exit_button_text, (SCREEN_WIDTH // 2 - exit_button_text.get_width() // 2, 540))

    pygame.display.update()
    showing_highscores = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            db.close()
            pygame.quit()
            quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if exit_rect.collidepoint(event.pos):
                showing_highscores = False
                main_menu = True
                break
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:  # Exit to main menu
                showing_highscores = False
                main_menu = True
                break

    return showing_highscores, main_menu

score = 0
game_running = False
main_menu = True
reset_game = False
showing_highscores = False

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()

bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()

for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

score = 0

while True:
    if main_menu:
        clock.tick(15)
        reset_game, game_running, main_menu, showing_highscores, flag_to_quit = draw_main_menu(screen, clock, game_running, main_menu, reset_game)
        if flag_to_quit:
            pygame.quit()
            break

    if showing_highscores:
        clock.tick(15)
        showing_highscores, main_menu = draw_results(screen, main_menu, db)

    if reset_game:
        bird_group = pygame.sprite.Group()
        bird = Bird()
        bird_group.add(bird)

        ground_group = pygame.sprite.Group()

        for i in range(2):
            ground = Ground(GROUND_WIDTH * i)
            ground_group.add(ground)

        pipe_group = pygame.sprite.Group()
        for i in range(2):
            pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        clock = pygame.time.Clock()

        score = 0

        reset_game = 0

    if game_running:
        clock.tick(15)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                quit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE or event.key == K_UP:
                    bird.bump()
                    pygame.mixer.music.load(wing)
                    pygame.mixer.music.play()
                if event.key == K_ESCAPE:
                    main_menu = True
                    game_running = False

        screen.blit(BACKGROUND, (0, 0))

        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDTH - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            score += 0
            pipe_group.remove(pipe_group.sprites()[0])
            score += 1
            pipes = get_random_pipes(SCREEN_WIDTH + 200)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        bird_group.update()
        ground_group.update()
        pipe_group.update()

        bird_group.draw(screen)
        pipe_group.draw(screen)
        ground_group.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 10, 10))

        pygame.display.update()

        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            pygame.mixer.music.load(hit)
            pygame.mixer.music.play()
            time.sleep(1)
            show_game_over(score, screen)

            db.add_score(score)  ## вот здесь

            # Wait for user input to restart or quit
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        quit()
                    if event.type == KEYDOWN:
                        if event.key == K_SPACE:
                            score = 0
                            bird.rect[1] = SCREEN_HEIGHT / 2
                            bird.speed = SPEED
                            bird_group.update()
                            pipe_group.empty()
                            pipes = get_random_pipes(SCREEN_WIDTH)
                            pipe_group.add(pipes[0])
                            pipe_group.add(pipes[1])
                            game_running = True
                            waiting = False
                        elif event.key == K_ESCAPE:
                            waiting = False
                            main_menu = True
                            game_running = False

pygame.quit()
