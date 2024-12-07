import unittest
import pygame
from test_flappy import Bird, SCREEN_WIDTH, SCREEN_HEIGHT, SPEED
from unittest.mock import MagicMock
from database import Database


class TestBird(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Инициализируем pygame для тестов
        pygame.init()
        pygame.display.set_mode((1, 1))

    @classmethod
    def tearDownClass(cls):
        pygame.quit()

    def setUp(self):
        self.bird = Bird()

    def test_initial_position(self):
        # Проверяем, что птица начинает в правильной позиции
        self.assertAlmostEqual(self.bird.rect[0], SCREEN_WIDTH / 6)
        self.assertAlmostEqual(self.bird.rect[1], SCREEN_HEIGHT / 2)

    def test_bump(self):
        # Проверка, что при bump скорость меняется на отрицательную
        self.bird.bump()
        self.assertEqual(self.bird.speed, -SPEED)

    def test_update_position(self):
        # Проверяем, что птица после update смещается вниз (учет гравитации)
        initial_y = self.bird.rect[1]
        self.bird.update()
        self.assertGreater(self.bird.rect[1], initial_y)  # птица должна опуститься

    def test_cycle_images(self):
        # Проверяем, что индекс изображения меняется корректно
        initial_image = self.bird.image
        self.bird.update()
        self.assertNotEqual(self.bird.image, initial_image)



class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Предполагается, что Database имеет методы add_score и get_top_scores
        # Здесь можно использовать mock или тестовую бд
        self.db = Database()
        # Чистим таблицу или создаем тестовую базу
        # Для простоты предполагаем, что в классе Database есть метод clear для очистки
        # Если нет — используйте mock или настройте тестовую среду отдельно.
        if hasattr(self.db, 'clear'):
            self.db.clear()

    def tearDown(self):
        self.db.close()

    def test_add_and_get_scores(self):
        self.db.add_score(10)
        self.db.add_score(50)
        self.db.add_score(30)

        top_scores = self.db.get_top_scores(3)
        # Проверяем, что результаты отсортированы по убыванию
        self.assertEqual(top_scores, [50, 30, 10])


if __name__ == '__main__':
    unittest.main()
