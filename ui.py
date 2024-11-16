# ui.py

import pygame
import sys
from database import Database

# Инициализация Pygame
pygame.init()

# Размеры экрана
SCREEN_WIDTH = 643
SCREEN_HEIGHT = 900

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

# Шрифты
FONT_LARGE = pygame.font.SysFont('Arial', 48)
FONT_MEDIUM = pygame.font.SysFont('Arial', 36)
FONT_SMALL = pygame.font.SysFont('Arial', 24)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Parrot')

# Загрузка ресурсов
background_image = pygame.image.load('assets/images/flappy-bird-background.png')
parrot_image = pygame.image.load('assets/images/pixel_parrot.png')

class UIManager:
    def __init__(self):
        self.player_name = ""
        self.database = Database('highscores.db')

    def draw_exit_button(self):
        # Рисует кнопку "выход" в верхнем левом углу
        exit_text = FONT_SMALL.render('Выход', True, WHITE)
        exit_button_rect = pygame.Rect(10, 10, exit_text.get_width() + 20, exit_text.get_height() + 10)
        pygame.draw.rect(screen, GRAY, exit_button_rect)
        screen.blit(exit_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))
        return exit_button_rect

    def main_menu(self):
        while True:
            screen.blit(background_image, (0, 0))
            title_text = FONT_LARGE.render('Flappy Parrot', True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            # Опции меню
            start_text = FONT_MEDIUM.render('1. Начать игру', True, WHITE)
            highscores_text = FONT_MEDIUM.render('2. Таблица рекордов', True, WHITE)
            exit_text = FONT_MEDIUM.render('3. Выход', True, WHITE)

            screen.blit(start_text, (SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200))
            screen.blit(highscores_text, (SCREEN_WIDTH // 2 - highscores_text.get_width() // 2, 250))
            screen.blit(exit_text, (SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 300))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.get_player_name()
                        return
                    elif event.key == pygame.K_2:
                        self.show_high_scores()
                    elif event.key == pygame.K_3:
                        self.quit_game()

    def get_player_name(self):
        input_active = True
        self.player_name = ""

        while input_active:
            screen.fill(BLACK)
            prompt_text = FONT_MEDIUM.render('Введите ваше имя:', True, WHITE)
            screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 200))

            name_text = FONT_MEDIUM.render(self.player_name, True, WHITE)
            screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 250))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if self.player_name.strip() == "":
                            self.player_name = "Игрок"
                        input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.player_name = self.player_name[:-1]
                    else:
                        self.player_name += event.unicode

    def show_high_scores(self):
        high_scores = self.database.get_high_scores()
        showing = True

        while showing:
            screen.fill(BLACK)
            title_text = FONT_LARGE.render('Таблица рекордов', True, WHITE)
            screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

            for index, (name, score) in enumerate(high_scores):
                score_text = FONT_SMALL.render(f"{index + 1}. {name} - {score}", True, WHITE)
                screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 150 + index * 30))

            # Отображение кнопки выхода
            exit_button_rect = self.draw_exit_button()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        showing = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        showing = False

    def game_over_screen(self, score, is_new_high_score):
        self.database.save_score(self.player_name, score)
        showing = True

        while showing:
            screen.fill(BLACK)
            game_over_text = FONT_LARGE.render('Игра окончена', True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))

            score_text = FONT_MEDIUM.render(f'Ваш счёт: {score}', True, WHITE)
            screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 200))

            if is_new_high_score:
                congrats_text = FONT_MEDIUM.render('Новый рекорд!', True, WHITE)
                screen.blit(congrats_text, (SCREEN_WIDTH // 2 - congrats_text.get_width() // 2, 250))

            retry_text = FONT_MEDIUM.render('1. Играть снова', True, WHITE)
            menu_text = FONT_MEDIUM.render('2. Главное меню', True, WHITE)
            screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 350))
            screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 400))

            # Отображение кнопки выхода
            exit_button_rect = self.draw_exit_button()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        showing = False
                    elif event.key == pygame.K_2:
                        showing = False
                        self.main_menu()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        showing = False
                        self.main_menu()

    def quit_game(self):
        self.database.close()
        pygame.quit()
        sys.exit()

# Для тестирования
if __name__ == "__main__":
    ui_manager = UIManager()
    ui_manager.main_menu()
