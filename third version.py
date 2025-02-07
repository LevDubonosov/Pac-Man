import pygame
import sys
import math
from math import sqrt
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_RADIUS = 15
ENEMY_RADIUS = 15
PLAYER_MOVE_DISTANCE = 3
ENEMY_MOVE_SPEED = 1  # Speed for enemy movement
BARRIER_COLOR = (0, 255, 0)
PLAYER_COLOR = (255, 255, 0)
ENEMY_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man Style Game")

player_pos = [WIDTH // 1.98, HEIGHT // 1.5]
enemy1_pos = [37, 37]   # Adjusted top-left enemy starting position
enemy2_pos = [762, 562]  # Adjusted bottom-right enemy starting position

# Barriers (rectangles)
barriers = [
    pygame.Rect(0, 0, 800, 10),
    pygame.Rect(0, 0, 10, 270),
    pygame.Rect(0, 330, 10, 290),
    pygame.Rect(0, 590, 800, 10),
    pygame.Rect(790, 0, 10, 270),
    pygame.Rect(790, 330, 10, 290),
    pygame.Rect(51, 50, 324, 10),
    pygame.Rect(424, 50, 325, 10),
    pygame.Rect(51, 50, 10, 150),
    pygame.Rect(424, 50, 10, 150),
    pygame.Rect(51, 200, 324, 10),
    pygame.Rect(424, 200, 325, 10),
    pygame.Rect(370, 50, 10, 160),
    pygame.Rect(739, 50, 10, 150),
    pygame.Rect(51 ,399 ,324 ,10),
    pygame.Rect(424 ,399 ,325 ,10),
    pygame.Rect(51 ,399 ,10 ,149),
    pygame.Rect(424 ,399 ,10 ,139),
    pygame.Rect(424 ,538 ,325 ,10),
    pygame.Rect(53 ,538 ,324 ,10),
    pygame.Rect(370 ,399 ,10 ,149),
    pygame.Rect(424 ,399 ,10 ,139),
    pygame.Rect(739 ,399 ,10 ,149)
]

def check_collision(rect):
    for barrier in barriers:
        if rect.colliderect(barrier):
            return True
    return False

def is_player_visible_to_enemy(enemy_pos):
    # Create a line from the enemy to the player
    line_rect = pygame.Rect(player_pos[0] - PLAYER_RADIUS,
                             player_pos[1] - PLAYER_RADIUS,
                             PLAYER_RADIUS *2,
                             PLAYER_RADIUS *2)

    # Check for barriers along the line of sight
    for barrier in barriers:
        if barrier.colliderect(line_rect):
            return False
    return True

def move_enemy_randomly(enemy_pos):
    # Randomly choose a direction to move in
    for i in range(2000):
        direction_x = random.choice([-ENEMY_MOVE_SPEED, ENEMY_MOVE_SPEED])
        direction_y = random.choice([-ENEMY_MOVE_SPEED, ENEMY_MOVE_SPEED])

        potential_new_pos_x = enemy_pos[0] + direction_x
        potential_new_pos_y = enemy_pos[1] + direction_y

    # Create a rectangle for the potential new position of the enemy
        potential_rect = pygame.Rect(potential_new_pos_x - ENEMY_RADIUS,
                                      potential_new_pos_y - ENEMY_RADIUS,
                                      ENEMY_RADIUS *2,
                                      ENEMY_RADIUS *2)

        if not check_collision(potential_rect):
            enemy_pos[0] = potential_new_pos_x
            enemy_pos[1] = potential_new_pos_y


def move_enemy_towards_player(enemy_pos):
    detection_range = 200 # Increased detection range for enemies

    if is_player_visible_to_enemy(enemy_pos) and math.hypot(player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]) < detection_range:
        # Calculate potential new position towards the player
        potential_new_pos_x = enemy_pos[0] + (PLAYER_MOVE_DISTANCE-1 if player_pos[0] > enemy_pos[0] else -PLAYER_MOVE_DISTANCE+1)
        potential_new_pos_y = enemy_pos[1] + (PLAYER_MOVE_DISTANCE-1 if player_pos[1] > enemy_pos[1] else -PLAYER_MOVE_DISTANCE+1)

        # Check for wall collisions before moving towards the player
        if not check_collision(pygame.Rect(potential_new_pos_x - ENEMY_RADIUS,
                                            enemy_pos[1] - ENEMY_RADIUS,
                                            ENEMY_RADIUS *2,
                                            ENEMY_RADIUS *2)):
            enemy_pos[0] = potential_new_pos_x

        if not check_collision(pygame.Rect(enemy_pos[0] - ENEMY_RADIUS,
                                            potential_new_pos_y - ENEMY_RADIUS,
                                            ENEMY_RADIUS *2,
                                            ENEMY_RADIUS *2)):
            enemy_pos[1] = potential_new_pos_y



def main():
    clock = pygame.time.Clock()
    game_over = False
    i = 1

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        direction = [0,0]

        if not game_over:
            if keys[pygame.K_w]:
                direction = [0,-1]
            elif keys[pygame.K_s]:
                direction = [0,+1]
            elif keys[pygame.K_a]:
                direction = [-1,+0]
            elif keys[pygame.K_d]:
                direction = [+1,+0]

            player_new_position = [
                player_pos[0] + direction[0] * PLAYER_MOVE_DISTANCE,
                player_pos[1] + direction[1] * PLAYER_MOVE_DISTANCE,
            ]

            player_rect = pygame.Rect(player_new_position[0] - PLAYER_RADIUS,
                                       player_new_position[1] - PLAYER_RADIUS,
                                       PLAYER_RADIUS *2,
                                       PLAYER_RADIUS *2)

            if not check_collision(player_rect):
                player_pos[:] = player_new_position

            # Move enemies randomly until they see the player
            if i % 61 == 0:
                move_enemy_randomly(enemy1_pos)
                move_enemy_randomly(enemy2_pos)
                i = 1

            # Move enemies towards the player only if visible
            move_enemy_towards_player(enemy1_pos)
            move_enemy_towards_player(enemy2_pos)

            # Check for collision with enemies
            enemy_rect_1 = pygame.Rect(enemy1_pos[0] - ENEMY_RADIUS,
                                        enemy1_pos[1] - ENEMY_RADIUS,
                                        ENEMY_RADIUS *2,
                                        ENEMY_RADIUS *2)

            enemy_rect_2 = pygame.Rect(enemy2_pos[0] - ENEMY_RADIUS,
                                        enemy2_pos[1] - ENEMY_RADIUS,
                                        ENEMY_RADIUS *2,
                                        ENEMY_RADIUS *2)

            if player_rect.colliderect(enemy_rect_1) or player_rect.colliderect(enemy_rect_2):
                game_over = True

        screen.fill(BACKGROUND_COLOR)

        for barrier in barriers:
            pygame.draw.rect(screen,BARRIER_COLOR ,barrier)

        pygame.draw.circle(screen ,PLAYER_COLOR ,
                           (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
        pygame.draw.circle(screen ,ENEMY_COLOR ,
                           (int(enemy1_pos[0]), int(enemy1_pos[1])), ENEMY_RADIUS)
        pygame.draw.circle(screen ,ENEMY_COLOR ,
                           (int(enemy2_pos[0]), int(enemy2_pos[1])), ENEMY_RADIUS)

        if game_over:
            font = pygame.font.SysFont(None ,55)
            text_surface = font.render('Game Over', True,GAME_OVER_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH //2 ,HEIGHT //2))
            screen.blit(text_surface,text_rect)

        i += 1
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
