import pygame
import random

class FlappyBirdGame:
    def __init__(self, window):
        self.window = window
        self.window_width = 1000
        self.window_height = 600
        self.window.fill((0, 0, 0))  # Черный фон
        self.bird_x = 50
        self.bird_y = 300
        self.bird_width = 20
        self.bird_height = 20
        self.bird_speed = 0
        self.gravity = 0.35

        self.pipe_width = 40
        self.pipe_speed = 3
        self.pipe_gap = 150
        self.game_over = False

        self.pipes = []
        self.pipe_frequency = 200
        self.pipe_counter = 0

        self.score = 0

        self.sky_image = pygame.image.load('sky.jpeg').convert()
        self.sky_image = pygame.transform.scale(self.sky_image, (self.window_width, self.window_height))
        self.sky_rect = self.sky_image.get_rect()

        self.texture = pygame.image.load("texture.jpeg").convert()
        self.font = pygame.font.Font(None, 36)

        self.play_again_button = pygame.Rect(self.window_width // 2 - 100, self.window_height // 2, 200, 50)
        self.main_menu_button = pygame.Rect(self.window_width // 2 - 100, self.window_height // 2 + 60, 200, 50)
        self.start_button = pygame.Rect(self.window_width // 2 - 100, self.window_height // 2 - 25, 200, 50)
        self.start_displayed = True  # Flag for showing the start screen

        self.run_game()

    def create_pipe(self):
        pipe_height = random.randint(50, self.window_height - 300)
        self.pipes.append({'x': self.window_width, 'height': pipe_height})

    def draw_game(self):
        self.window.blit(self.sky_image, self.sky_rect)
        if self.game_over:
            play_again_text = self.font.render('Играть снова', True, (255, 255, 255))
            play_again_rect = play_again_text.get_rect(center=self.play_again_button.center)
            self.window.blit(play_again_text, play_again_rect)

            main_menu_text = self.font.render('В главное меню', True, (255, 255, 255))
            main_menu_rect = main_menu_text.get_rect(center=self.main_menu_button.center)
            self.window.blit(main_menu_text, main_menu_rect)

            return True

        if self.start_displayed:
            pygame.draw.rect(self.window, (255, 255, 255), self.start_button)
            font = pygame.font.Font(None, 24)
            text = font.render('Press Space to Start', True, (0, 0, 0))
            text_rect = text.get_rect(center=self.start_button.center)
            self.window.blit(text, text_rect)

            return False

        # Отрисовываем птицу
        pygame.draw.rect(self.window, (0, 0, 0), (self.bird_x, self.bird_y, self.bird_width, self.bird_height))

        # Обрабатываем движение труб
        for pipe in self.pipes:
            upper_rect = pygame.Rect(pipe['x'], 0, self.pipe_width, pipe['height'])
            lower_rect = pygame.Rect(pipe['x'], pipe['height'] + self.pipe_gap, self.pipe_width, self.window_height - pipe['height'] - self.pipe_gap)

            upper_image = pygame.transform.scale(self.texture, (self.pipe_width, pipe['height']))
            self.window.blit(upper_image, upper_rect)
            lower_image = pygame.transform.scale(self.texture, (self.pipe_width, self.window_height - pipe['height'] - self.pipe_gap))
            self.window.blit(lower_image, lower_rect)

            # Проверка на столкновение
            if self.bird_x + self.bird_width > pipe['x'] and self.bird_x < pipe['x'] + self.pipe_width:
                if self.bird_y < pipe['height'] or self.bird_y + self.bird_height > pipe['height'] + self.pipe_gap:
                    self.game_over = True

        # Обновление скорости и положения птицы
        self.bird_y += self.bird_speed
        self.bird_speed += self.gravity

        # Проверка на выход за границы экрана
        if self.bird_y >= self.window_height or self.bird_y <= 0:
            self.game_over = True

        # Счет
        score_text = self.font.render(f'Score: {self.score}', True, pygame.Color(0, 255, 255, 255))
        self.window.blit(score_text, (self.window_width - 100, 10))

        return False

    def update(self):
        if not self.game_over:
            for pipe in self.pipes:
                pipe['x'] -= self.pipe_speed
                if pipe['x'] + self.pipe_width < 0:
                    self.pipes.remove(pipe)
                    self.score += 1

            self.pipe_counter -= self.pipe_speed
            if self.pipe_counter <= 0:
                self.create_pipe()
                self.pipe_counter = self.pipe_frequency

    def run_game(self):
        pygame.init()
        window = pygame.display.set_mode((self.window_width, self.window_height))
        clock = pygame.time.Clock()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.start_displayed:
                            self.start_displayed = False
                        if not self.game_over:
                            self.bird_speed = -6

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game_over:
                        if self.play_again_button.collidepoint(mouse_pos):
                            self.game_over = False
                            self.score = 0
                            self.pipes.clear()
                            self.pipe_counter = 0
                            self.bird_y = 300
                            self.bird_speed = 0
                        elif self.main_menu_button.collidepoint(mouse_pos):
                            running = False

            if not self.game_over:
                self.update()

            game_over = self.draw_game()

            if game_over:
                pygame.display.flip()
                clock.tick(60)
                continue

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode((1000, 600))  # Размер окна 1000x600 пикселей
    pygame.display.set_caption("Flappy Bird Game")  # Устанавливаем заголовок окна

    # Передаем созданное окно в игру
    FlappyBirdGame(window)
