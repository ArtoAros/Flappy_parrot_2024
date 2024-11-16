import pygame
import sys
from database import Database

# Инициализация Pygame
pygame.init()
pygame.mixer.init()  # Инициализация микшера для музыки

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

pygame.mixer.music.load('assets/music/background_music.mp3')  # Укажите путь к файлу с музыкой
pygame.mixer.music.play(-1, 0.0)  # Бесконечный цикл


class UIManager:
    def __init__(self):
        self.player_name = ""
        self.database = Database('highscores.db')
        self.volume = 5  # Изначальный уровень громкости (от 0 до 10)
        pygame.mixer.music.set_volume(self.volume / 10.0)  # Устанавливаем громкость

    def draw_exit_button(self):
        exit_text = FONT_SMALL.render('Назад', True, WHITE)
        exit_button_rect = pygame.Rect(10, 10, exit_text.get_width() + 15, exit_text.get_height() + 15)
        screen.blit(exit_text, (exit_button_rect.x + 10, exit_button_rect.y + 5))
        return exit_button_rect

    def draw_music_button(self):
        music_text = FONT_SMALL.render('Музыка', True, WHITE)
        music_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - music_text.get_width() // 2, 350, music_text.get_width(), music_text.get_height())
        screen.blit(music_text, music_button_rect.topleft)
        return music_button_rect

    def adjust_volume(self):
        while True:
            screen.blit(background_image, (0, 0))

            # Текст для громкости
            volume_text = FONT_MEDIUM.render(f'Громкость: {self.volume}', True, WHITE)
            volume_text_rect = volume_text.get_rect(center=(SCREEN_WIDTH // 2, 200))

            screen.blit(volume_text, volume_text_rect.topleft)

            # Увеличиваем размер шрифта для кнопок "+" и "-"
            button_font = pygame.font.SysFont('Arial', 48)  # Увеличиваем размер шрифта

            # Кнопки для увеличения и уменьшения громкости
            decrease_text = button_font.render('-', True, WHITE)
            increase_text = button_font.render('+', True, WHITE)

            # Располагаем кнопки на одной линии с текстом громкости
            decrease_rect = pygame.Rect(volume_text_rect.left - 50, 200, decrease_text.get_width(),
                                        decrease_text.get_height())
            increase_rect = pygame.Rect(volume_text_rect.right + 30, 200, increase_text.get_width(),
                                        increase_text.get_height())

            screen.blit(decrease_text, decrease_rect.topleft)
            screen.blit(increase_text, increase_rect.topleft)

            # Отображаем кнопку "Назад"
            exit_button_rect = self.draw_exit_button()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit_game()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if exit_button_rect.collidepoint(event.pos):
                        return  # Возвращаемся на главный экран
                    elif decrease_rect.collidepoint(event.pos) and self.volume > 0:
                        self.volume -= 1
                        pygame.mixer.music.set_volume(self.volume / 10.0)  # Обновляем громкость
                    elif increase_rect.collidepoint(event.pos) and self.volume < 10:
                        self.volume += 1
                        pygame.mixer.music.set_volume(self.volume / 10.0)  # Обновляем громкость

    def main_menu(self):
        while True:
            screen.blit(background_image, (0, 0))

            # Опции меню
            start_text = FONT_MEDIUM.render('Начать игру', True, WHITE)
            highscores_text = FONT_MEDIUM.render('Таблица рекордов', True, WHITE)
            music_text = FONT_MEDIUM.render('Музыка', True, WHITE)
            exit_text = FONT_MEDIUM.render('Выход', True, WHITE)

            start_rect = pygame.Rect(SCREEN_WIDTH // 2 - start_text.get_width() // 2, 200, start_text.get_width(), start_text.get_height())
            highscores_rect = pygame.Rect(SCREEN_WIDTH // 2 - highscores_text.get_width() // 2, 250, highscores_text.get_width(), highscores_text.get_height())
            music_rect = pygame.Rect(SCREEN_WIDTH // 2 - music_text.get_width() // 2, 300, music_text.get_width(), music_text.get_height())
            exit_rect = pygame.Rect(SCREEN_WIDTH // 2 - exit_text.get_width() // 2, 350, exit_text.get_width(), exit_text.get_height())

            screen.blit(start_text, start_rect.topleft)
            screen.blit(highscores_text, highscores_rect.topleft)
            screen.blit(music_text, music_rect.topleft)
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
                    elif music_rect.collidepoint(event.pos):
                        self.adjust_volume()  # Переход к регулировке громкости
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

    def quit_game(self):
        pygame.mixer.music.stop()
        self.database.close()
        pygame.quit()
        sys.exit()

# Для тестирования
if __name__ == "__main__":
    ui_manager = UIManager()
    ui_manager.main_menu()
