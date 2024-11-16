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
        # Создаем текст "Выход" и получаем размеры прямоугольника кнопки
        exit_text = FONT_SMALL.render('Назад', True, WHITE)
        exit_button_rect = pygame.Rect(10, 10, exit_text.get_width() + 15, exit_text.get_height() + 15)

        # Пропускаем вызов pygame.draw.rect, чтобы не рисовать фон кнопки, делая ее "невидимой"

        # Рисуем только текст
        screen.blit(exit_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))

        # Возвращаем прямоугольник для проверки нажатия мышкой
        return exit_button_rect

    def main_menu(self):
        while True:
            screen.blit(background_image, (0, 0))
            # title_text = FONT_LARGE.render('Flappy Parrot', True, WHITE)
            # screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))

            # Опции меню
            start_text = FONT_MEDIUM.render('Начать игру', True, WHITE)
            highscores_text = FONT_MEDIUM.render('Таблица рекордов', True, WHITE)
            exit_text = FONT_MEDIUM.render('Выход', True, WHITE)

            start_rect = pygame.Rect(SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200, start_text.get_width(), start_text.get_height())
            highscores_rect = pygame.Rect(SCREEN_WIDTH // 2 - highscores_text.get_width() // 2, 250, highscores_text.get_width(), highscores_text.get_height())
            exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 300, exit_text.get_width(), exit_text.get_height())

            screen.blit(start_text, start_rect.topleft)
            screen.blit(highscores_text, highscores_rect.topleft)
            screen.blit(exit_text, exit_rect.topleft)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        self.get_player_name()
                        return
                    elif highscores_rect.collidepoint(event.pos):
                        self.show_high_scores()
                    elif exit_rect.collidepoint(event.pos):
                        self.quit_game()

    def get_player_name(self):
        input_active = True
        self.player_name = ""

        while input_active:
            screen.blit(background_image, (0, 0))
            prompt_text = FONT_MEDIUM.render('Введите ваше имя:', True, WHITE)
            screen.blit(prompt_text, (SCREEN_WIDTH // 2 - prompt_text.get_width() // 2, 200))

            name_text = FONT_MEDIUM.render(self.player_name, True, WHITE)
            screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, 250))

            # Отображение кнопки выхода
            exit_button_rect = self.draw_exit_button()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        self.main_menu()
                        # Возвращаемся в главное меню, если нажата кнопка "Назад"
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
            screen.blit(background_image, (0, 0))
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

            retry_text = FONT_MEDIUM.render('Играть снова', True, WHITE)
            menu_text = FONT_MEDIUM.render('Главное меню', True, WHITE)

            retry_rect = pygame.Rect(SCREEN_WIDTH // 2 - retry_text.get_width() // 2, 350, retry_text.get_width(), retry_text.get_height())
            menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - menu_text.get_width() // 2, 400, menu_text.get_width(), menu_text.get_height())

            screen.blit(retry_text, retry_rect.topleft)
            screen.blit(menu_text, menu_rect.topleft)

            # Отображение кнопки выхода
            exit_button_rect = self.draw_exit_button()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if retry_rect.collidepoint(event.pos):
                        showing = False
                    elif menu_rect.collidepoint(event.pos):
                        showing = False
                        self.main_menu()
                    elif exit_button_rect.collidepoint(event.pos):
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