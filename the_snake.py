from random import randint
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Класс игрового объекта"""

    def __init__(self, body_color=None, position=(320, 240)):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Общая функция для рисования"""
        pass


class Apple(GameObject):
    """Класс яблока"""

    def randomize_position(self):
        """генерируем произвольную позицию"""
        self.position = (randint(0, 31) * 20, randint(0, 23) * 20)

    def __init__(self, body_color=(255, 0, 0)):
        self.randomize_position()
        self.body_color = body_color

    # Метод draw класса Apple
    def draw(self):
        """переопределяем функцию для рисования"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змеи"""

    positions: list = []

    def __init__(
            self, length=1, position=(320, 240), direction=RIGHT,
            next_direction=None, body_color=(0, 255, 0)):
        self.length = length
        self.direction = direction
        self.positions.append(position)
        self.next_direction = next_direction
        self.body_color = body_color
        self.position = self.positions[0]
        self.last = None

# Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Метод обновления направления после нажатия на кнопку"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для перемещения змеи"""
        if self.direction == RIGHT:
            self.positions.insert(
                0, (self.get_head_position()[0] + 20, self.get_head_position()[1])
            )
        if self.direction == LEFT:
            self.positions.insert(
                0, (self.get_head_position()[0] - 20, self.get_head_position()[1])
            )
        if self.direction == UP:
            self.positions.insert(
                0, (self.get_head_position()[0], self.get_head_position()[1] - 20)
            )
        if self.direction == DOWN:
            self.positions.insert(
                0, (self.get_head_position()[0], self.get_head_position()[1] + 20)
            )
        self.last = self.positions[-1]
        self.positions.pop()

    def get_head_position(self):
        """Возвращаем голову"""
        return self.positions[0]

    def reset(self):
        """Давай с начала"""
        self.length = 1
        self.direction = RIGHT
        self.position = (320, 240)
        self.positions = [self.position]
        self.next_direction = None
        self.body_color = (0, 255, 0)

# Метод draw класса Snake
    def draw(self):
        """РИСУЕМ"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


# Функция обработки действий пользователя
def handle_keys(game_object):
    """проверяем..."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """ну все, стартуем"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    main_snake = Snake()
    main_apple = Apple()
    while True:
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        handle_keys(main_snake)
        main_snake.update_direction()
        main_snake.move()
        if main_snake.get_head_position() == main_apple.position:
            main_snake.length += 1
            main_snake.positions.append(main_snake.last)
            main_apple.randomize_position()
        if main_snake.get_head_position() in main_snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            main_apple.randomize_position()
            main_snake.reset()
        main_snake.draw()
        main_apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
