import pygame
import sys
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_RADIUS = 15
PLAYER_MOVE_DISTANCE = 5  # Дистанция перемещения за кадр
BARRIER_COLOR = (0, 255, 0)
PLAYER_COLOR = (255, 255, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Style Game")

# Игрок
player_pos = [WIDTH // 2, HEIGHT // 2]
direction = [0, 0]  # Направление движения (x, y)

# Барьеры (прямоугольники)
barriers = [
    pygame.Rect(100, 100, 600, 20),
    pygame.Rect(100, 200, 20, 400),
    pygame.Rect(100, 580, 600, 20),
    pygame.Rect(680, 200, 20, 400),
]

# Функция для проверки столкновения с барьерами
def check_collision(player_pos):
    player_rect = pygame.Rect(player_pos[0] - PLAYER_RADIUS, player_pos[1] - PLAYER_RADIUS,
                               PLAYER_RADIUS * 2, PLAYER_RADIUS * 2)
    for barrier in barriers:
        if player_rect.colliderect(barrier):
            return True
    return False

# Основной игровой цикл
def main():
    global direction
    clock = pygame.time.Clock()
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_w:
                    direction = [0, -1]  # Вверх
                elif event.key == pygame.K_s:
                    direction = [0, 1]   # Вниз
                elif event.key == pygame.K_a:
                    direction = [-1, 0]  # Влево
                elif event.key == pygame.K_d:
                    direction = [1, 0]   # Вправо

        if not game_over:
            # Обновление позиции игрока в зависимости от направления
            player_pos[0] += direction[0] * PLAYER_MOVE_DISTANCE
            player_pos[1] += direction[1] * PLAYER_MOVE_DISTANCE

            # Проверка на столкновение с барьерами
            if check_collision(player_pos):
                game_over = True

            # Проверка на столкновение с невидимыми барьерами по краям
            if player_pos[0] < PLAYER_RADIUS or player_pos[0] > WIDTH - PLAYER_RADIUS or \
               player_pos[1] < PLAYER_RADIUS or player_pos[1] > HEIGHT - PLAYER_RADIUS:
                player_pos[0], player_pos[1] = WIDTH // 2, HEIGHT // 2

        # Отрисовка элементов на экране
        screen.fill(BACKGROUND_COLOR)

        # Отрисовка барьеров
        for barrier in barriers:
            pygame.draw.rect(screen, BARRIER_COLOR, barrier)

        # Отрисовка игрока
        pygame.draw.circle(screen, PLAYER_COLOR, (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)

        # Если игра окончена - отображаем сообщение Game Over
        if game_over:
            font = pygame.font.SysFont(None, 55)
            text_surface = font.render('Game Over', True, GAME_OVER_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface, text_rect)

        # Обновление экрана
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
