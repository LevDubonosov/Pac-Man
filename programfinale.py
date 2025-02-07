import pygame
import sys
import math
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_RADIUS = 15
ENEMY_RADIUS = 15
PLAYER_MOVE_DISTANCE = 1
ENEMY_MOVE_SPEED = 1.2 # Speed for enemy movement
BARRIER_COLOR = (0, 255, 0)
PLAYER_COLOR = (255, 255, 0)
ENEMY_COLOR = (255, 0, 0)
BACKGROUND_COLOR = (0, 0, 0)
GAME_OVER_COLOR = (255, 0, 0)
U_IS_MOVING_FLAG = 0
D_IS_MOVING_FLAG = 0
L_IS_MOVING_FLAG = 0
R_IS_MOVING_FLAG = 0
REM_DIRECTION = 0
CURR_TIME = 0
direction = [0, 0]
COIN_RADIUS = 10
COST = 0
MOVINGFLAG1 = False
MOVINGFLAG2 = False

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

    pygame.Rect(51, 399, 324, 10),
    pygame.Rect(424, 399, 325, 10),
    pygame.Rect(51, 399, 10, 149),
    pygame.Rect(424, 399, 10, 139),
    pygame.Rect(424, 538, 325, 10),
    pygame.Rect(53, 538, 324, 10),
    pygame.Rect(370, 399, 10, 149),
    pygame.Rect(424, 399, 10, 139),
    pygame.Rect(739, 399, 10, 149),

    pygame.Rect(51, 251, 324, 10),
    pygame.Rect(51, 348, 324, 10),
    pygame.Rect(424, 251, 325, 10),
    pygame.Rect(424, 348, 325, 10),
    pygame.Rect(424, 251, 10, 97),
    pygame.Rect(51, 251, 10, 97),
    pygame.Rect(739, 251, 10, 97),
    pygame.Rect(370, 251, 10, 107),
]

enemy_barriers = [pygame.Rect(0, 270, 10, 60), pygame.Rect(790, 270, 10, 60)]

coins_positions = [[40, 30, 1], [130, 30, 1], [220, 30, 1], [310, 30, 1], [400, 30, 1], [490, 30, 1], [580, 30, 1], [670, 30, 1], [760, 30, 1],
                   [40, 230, 1], [130, 230, 1], [220, 230, 1], [310, 230, 1], [400, 230, 1], [490, 230, 1], [580, 230, 1], [670, 230, 1], [760, 230, 1],
                   [40, 380, 1], [130, 380, 1], [220, 380, 1], [310, 380, 1], [400, 380, 1], [490, 380, 1], [580, 380, 1], [670, 380, 1], [760, 380, 1],
                   [40, 570, 1], [130, 570, 1], [220, 570, 1], [310, 570, 1], [400, 570, 1], [490, 570, 1], [580, 570, 1], [670, 570, 1], [760, 570, 1],
                  ]

checked_coins = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

def checks(rect):
    for barrier in barriers:
        if rect.colliderect(barrier):
            return True
    for barrier in enemy_barriers:
        if rect.colliderect(barrier):
            return True
    return False

def check_collision(player_pos):
    player_rect = pygame.Rect(player_pos[0] - (PLAYER_RADIUS * 1.3), player_pos[1] - (PLAYER_RADIUS * 1.3),
                               PLAYER_RADIUS * 2 * 1.3, PLAYER_RADIUS * 2 * 1.3)
    for barrier in barriers:
        if player_rect.colliderect(barrier):
            return True
    return False

def checking(player_pos, direction, PLAYER_MOVE_DISTANCE):
    player_pos2 = []
    player_pos2.append(player_pos[0] + direction[0] * PLAYER_MOVE_DISTANCE)
    player_pos2.append(player_pos[1] + direction[1] * PLAYER_MOVE_DISTANCE)
    return player_pos2

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

        if not checks(potential_rect):
            enemy_pos[0] = potential_new_pos_x
            enemy_pos[1] = potential_new_pos_y


def move_enemy_towards_player(enemy_pos):
    global MOVINGFLAG1
    global MOVINGFLAG2
    detection_range = 200 # Increased detection range for enemies

    if math.hypot(player_pos[0] - enemy_pos[0], player_pos[1] - enemy_pos[1]) < detection_range:
        # Calculate potential new position towards the player
        if enemy_pos == enemy1_pos :
            MOVINGFLAG1 = True
        else:
            MOVINGFLAG2 = True
        potential_new_pos_x = enemy_pos[0] + (PLAYER_MOVE_DISTANCE-1 if player_pos[0] > enemy_pos[0] else -PLAYER_MOVE_DISTANCE+1)
        potential_new_pos_y = enemy_pos[1] + (PLAYER_MOVE_DISTANCE-1 if player_pos[1] > enemy_pos[1] else -PLAYER_MOVE_DISTANCE+1)

        # Check for wall collisions before moving towards the player
        if not checks(pygame.Rect(potential_new_pos_x - ENEMY_RADIUS,
                                            enemy_pos[1] - ENEMY_RADIUS,
                                            ENEMY_RADIUS *2,
                                            ENEMY_RADIUS *2)):
            enemy_pos[0] = potential_new_pos_x

        if not checks(pygame.Rect(enemy_pos[0] - ENEMY_RADIUS,
                                            potential_new_pos_y - ENEMY_RADIUS,
                                            ENEMY_RADIUS *2,
                                            ENEMY_RADIUS *2)):
            enemy_pos[1] = potential_new_pos_y
    else:
        if enemy_pos == enemy1_pos:
            MOVINGFLAG1 = False
        else:
            MOVINGFLAG2 = False



def main():
    clock = pygame.time.Clock()
    game_over = False
    global MOVINGFLAG
    global direction
    global PLAYER_MOVE_DISTANCE
    global player_pos
    global U_IS_MOVING_FLAG
    global D_IS_MOVING_FLAG
    global L_IS_MOVING_FLAG
    global R_IS_MOVING_FLAG
    global REM_DIRECTION
    global CURR_TIME
    global COST
    global ENEMY_MOVE_SPEED
    i = 1
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_w and U_IS_MOVING_FLAG == 0:
                    if direction != [0, -1]:
                        PLAYER_MOVE_DISTANCE = 3
                    if not check_collision(checking(player_pos, [0, -1], 5)):
                        direction = [0, -1]
                        D_IS_MOVING_FLAG = 0
                        L_IS_MOVING_FLAG = 0
                        U_IS_MOVING_FLAG = 0
                        R_IS_MOVING_FLAG = 0
                    else:
                        REM_DIRECTION = [0, -1]
                        CURR_TIME = time.time()
                elif event.key == pygame.K_s and D_IS_MOVING_FLAG == 0:
                    if direction != [0, 1]:
                        PLAYER_MOVE_DISTANCE = 3
                    if not check_collision(checking(player_pos, [0, 1], 5)):
                        direction = [0, 1]
                        D_IS_MOVING_FLAG = 0
                        L_IS_MOVING_FLAG = 0
                        U_IS_MOVING_FLAG = 0
                        R_IS_MOVING_FLAG = 0
                    else:
                        REM_DIRECTION = [0, 1]
                        CURR_TIME = time.time()
                elif event.key == pygame.K_a and L_IS_MOVING_FLAG == 0:
                    if direction != [-1, 0]:
                        PLAYER_MOVE_DISTANCE = 3
                    if not check_collision(checking(player_pos, [-1, 0], 5)):
                        direction = [-1, 0]
                        D_IS_MOVING_FLAG = 0
                        L_IS_MOVING_FLAG = 0
                        U_IS_MOVING_FLAG = 0
                        R_IS_MOVING_FLAG = 0
                    else:
                        REM_DIRECTION = [-1, 0]
                        CURR_TIME = time.time()
                elif event.key == pygame.K_d and R_IS_MOVING_FLAG == 0:
                    if direction != [1, 0]:
                        PLAYER_MOVE_DISTANCE = 3
                    if not check_collision(checking(player_pos, [1, 0], 5)):
                        direction = [1, 0]
                        D_IS_MOVING_FLAG = 0
                        L_IS_MOVING_FLAG = 0
                        U_IS_MOVING_FLAG = 0
                        R_IS_MOVING_FLAG = 0
                    else:
                        REM_DIRECTION = [1, 0]
                        CURR_TIME = time.time()
        if not game_over:
            player_new_position = [
                player_pos[0] + direction[0] * PLAYER_MOVE_DISTANCE,
                player_pos[1] + direction[1] * PLAYER_MOVE_DISTANCE,
            ]
            player_rect = pygame.Rect(player_new_position[0] - PLAYER_RADIUS,
                                       player_new_position[1] - PLAYER_RADIUS,
                                       PLAYER_RADIUS *2,
                                       PLAYER_RADIUS *2)
            player_pos2 = []
            player_pos2.append(player_pos[0] + direction[0] * PLAYER_MOVE_DISTANCE)
            player_pos2.append(player_pos[1] + direction[1] * PLAYER_MOVE_DISTANCE)
            if time.time() <= CURR_TIME + 1.0 and CURR_TIME != 0 and REM_DIRECTION != 0 and not check_collision(checking(player_pos, REM_DIRECTION, 5)):
                direction = REM_DIRECTION
                D_IS_MOVING_FLAG = 0
                L_IS_MOVING_FLAG = 0
                U_IS_MOVING_FLAG = 0
                R_IS_MOVING_FLAG = 0
                CURR_TIME = 0
                REM_DIRECTION = 0
            elif check_collision(player_pos2):
                PLAYER_MOVE_DISTANCE = 0
                if direction == [0, -1]:
                    U_IS_MOVING_FLAG = 1
                elif direction == [0, 1]:
                    D_IS_MOVING_FLAG = 1
                elif direction == [-1, 0]:
                    L_IS_MOVING_FLAG = 1
                elif direction == [1, 0]:
                    R_IS_MOVING_FLAG = 1
            elif time.time() > CURR_TIME + 1.0 and CURR_TIME != 0:
                CURR_TIME = 0
                REM_DIRECTION = 0
            else:
                player_pos = player_pos2
            if player_pos[0] < PLAYER_RADIUS:
                player_pos[0] = WIDTH - PLAYER_RADIUS
            elif player_pos[0] > WIDTH - PLAYER_RADIUS:
                player_pos[0] = PLAYER_RADIUS

            # Move enemies randomly until they see the player
            if i % 61 == 0:
                if not MOVINGFLAG1:
                    move_enemy_randomly(enemy1_pos)
                if not MOVINGFLAG2:
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

            for position in coins_positions:
                if (position[0] > player_pos[0] - PLAYER_RADIUS and position[0] < player_pos[0] + PLAYER_RADIUS) and (position[1] > player_pos[1] - PLAYER_RADIUS and position[1] < player_pos[1] + PLAYER_RADIUS):
                    position[2] = 0

        screen.fill(BACKGROUND_COLOR)

        for barrier in barriers:
            pygame.draw.rect(screen,BARRIER_COLOR ,barrier)

        pygame.draw.circle(screen ,PLAYER_COLOR ,
                           (int(player_pos[0]), int(player_pos[1])), PLAYER_RADIUS)
        pygame.draw.circle(screen ,ENEMY_COLOR ,
                           (int(enemy1_pos[0]), int(enemy1_pos[1])), ENEMY_RADIUS)
        pygame.draw.circle(screen ,ENEMY_COLOR ,
                           (int(enemy2_pos[0]), int(enemy2_pos[1])), ENEMY_RADIUS)
        c = 0
        for position in coins_positions:
            if int(position[2]) == 1:
                c += 1
                pygame.draw.circle(screen, PLAYER_COLOR, (int(position[0]), int(position[1])), COIN_RADIUS)
            else:
                if checked_coins[coins_positions.index(position)] == 0:
                    checked_coins[coins_positions.index(position)] = 1
                    COST += 1
        if c == 0:
            for position in coins_positions:
                position[2] = 1
            for i in range(len(checked_coins)):
                checked_coins[i] = 0
            PLAYER_MOVE_DISTANCE += 0.05
            ENEMY_MOVE_SPEED += 0.05
        font = pygame.font.SysFont(None, 30)
        text_surface = font.render(str(COST), True, GAME_OVER_COLOR)
        text_rect = text_surface.get_rect(center=(750, 20))
        screen.blit(text_surface, text_rect)

        if game_over:
            font = pygame.font.SysFont(None,55)
            text_surface = font.render('Game Over', True,GAME_OVER_COLOR)
            text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text_surface,text_rect)

        i += 1
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
