import pygame
import random

# Инициализация Pygame
pygame.init()

# Определение параметров окна игры
window_width = 1000
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Flappy Bird')

# Цвета
black = (0, 0, 0)
white = (255, 255, 255)

# Основные параметры игры
bird_x = 50
bird_y = 300
bird_width = 20
bird_height = 20
bird_speed = 0
gravity = 0.35

pipe_width = 40
pipe_speed = 3
pipe_gap = 150 

game_over = False

pipes = []
pipe_frequency = 200
pipe_counter = 0

score = 0

def create_pipe():
    pipe_height = random.randint(50, window_height-300)
    pipes.append({'x': window_width, 'height': pipe_height})

clock = pygame.time.Clock()
start_button = pygame.Rect(window_width // 2 - 100, window_height // 2 - 25, 200, 50)
start_displayed = True  # Флаг для отображения начала игры

# Загрузка изображения неба
sky_image = pygame.image.load('sky.jpeg').convert()

# Масштабирование изображения под размер окна
sky_image = pygame.transform.scale(sky_image, (window_width, window_height))
sky_rect = sky_image.get_rect()

texture = pygame.image.load("texture.jpeg").convert()

font = pygame.font.Font(None, 36)
play_again_button = pygame.Rect(window_width // 2 - 100, window_height // 2, 200, 50)
main_menu_button = pygame.Rect(window_width // 2 - 100, window_height // 2 + 60, 200, 50)

running = True

while running:
    window.blit(sky_image, sky_rect)

    if game_over:
        play_again_text = font.render('Играть снова', True, white)
        play_again_rect = play_again_text.get_rect(center=play_again_button.center)
        window.blit(play_again_text, play_again_rect)
        
        main_menu_text = font.render('В главное меню', True, white)
        main_menu_rect = main_menu_text.get_rect(center=main_menu_button.center)
        window.blit(main_menu_text, main_menu_rect)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if play_again_button.collidepoint(mouse_pos):
                    game_over = False
                    break
                elif main_menu_button.collidepoint(mouse_pos):
                    running = False
                    break
        if running == False:
            break
        if game_over == False:
            window.fill(white)  # Очистить экран перед отрисовкой игры
            bird_x = 50
            bird_y = 300
            bird_speed = 0
            gravity = 0.35
            game_over = False
            pipes.clear()
            pipe_counter = 0
            score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start_displayed:
                start_displayed = False

    if start_displayed:
        pygame.draw.rect(window, white, start_button)
        font = pygame.font.Font(None, 24)
        text = font.render('Press Space to Start', True, black)
        text_rect = text.get_rect(center=start_button.center)
        window.blit(text, text_rect)
    else:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            bird_speed = -6

        if not game_over:
            bird_y += bird_speed
            bird_speed += gravity

            for pipe in pipes:
                pipe['x'] -= pipe_speed
                if pipe['x'] + pipe_width < 0:
                    pipes.remove(pipe)
                    score += 1
            
            pipe_counter -= pipe_speed
            if pipe_counter <= 0:
                create_pipe()
                pipe_counter = pipe_frequency

            for pipe in pipes:
                upper_rect = pygame.Rect(pipe['x'], 0, pipe_width, pipe['height'])
                lower_rect = pygame.Rect(pipe['x'], pipe['height'] + pipe_gap, pipe_width, window_height - pipe['height'] - pipe_gap)

                upper_image = pygame.transform.scale(texture, (pipe_width, pipe['height']))
                window.blit(upper_image, upper_rect)
                lower_image = pygame.transform.scale(texture, (pipe_width, window_height - pipe['height'] - pipe_gap))
                window.blit(lower_image, lower_rect)


                if bird_x + bird_width > pipe['x'] and bird_x < pipe['x'] + pipe_width:
                    if bird_y < pipe['height'] or bird_y + bird_height > pipe['height'] + pipe_gap:
                        game_over = True

            pygame.draw.rect(window, black, (bird_x, bird_y, bird_width, bird_height))

            if bird_y >= window_height or bird_y <= 0:
                game_over = True

        score_text = font.render('Score: ' + str(score), True, pygame.Color(0, 255, 255, 255))
        window.blit(score_text, (window_width - 100, 10))

    pygame.display.flip()
    clock.tick(60 + score * 5)
pygame.quit()