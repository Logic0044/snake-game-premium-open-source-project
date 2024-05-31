import pygame
import time
import random

# Initialize Pygame
pygame.init()

# Screen settings
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
grey = (169, 169, 169)
orange = (255, 165, 0)
purple = (160, 32, 240)

dis_width = 800
dis_height = 600

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game')

clock = pygame.time.Clock()
snake_block = 10
initial_speed = 15
speed_increment = 5
level_up_score = 10
initial_lives = 3

font_style = pygame.font.SysFont(None, 50)
score_font = pygame.font.SysFont(None, 35)

def Your_score(score):
    value = score_font.render("Score: " + str(score), True, black)
    dis.blit(value, [0, 0])

def Your_lives(lives):
    value = score_font.render("Lives: " + str(lives), True, black)
    dis.blit(value, [0, 35])

def our_snake(snake_block, snake_List):
    for x in snake_List:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])

def draw_obstacles(obstacles):
    for obs in obstacles:
        pygame.draw.rect(dis, grey, [obs[0], obs[1], snake_block, snake_block])

def draw_moving_obstacles(moving_obstacles):
    for obs in moving_obstacles:
        pygame.draw.rect(dis, red, [obs[0], obs[1], snake_block, snake_block])

def move_obstacles(moving_obstacles):
    for obs in moving_obstacles:
        obs[1] += snake_block
        if obs[1] >= dis_height:
            obs[1] = 0

def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])

def generate_obstacles(num_obstacles):
    obstacles = []
    for _ in range(num_obstacles):
        obs_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        obs_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        obstacles.append([obs_x, obs_y])
    return obstacles

def generate_moving_obstacles(num_moving_obstacles):
    moving_obstacles = []
    for _ in range(num_moving_obstacles):
        obs_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
        obs_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
        moving_obstacles.append([obs_x, obs_y])
    return moving_obstacles

def gameLoop():
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    snake_List = []
    Length_of_snake = 1
    snake_speed = initial_speed
    lives = initial_lives

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    special_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    special_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    special_food_active = True
    special_food_timer = 0

    speed_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    speed_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    speed_food_active = True
    speed_food_timer = 0

    freeze_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    freeze_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    freeze_food_active = True
    freeze_food_timer = 0
    freeze_duration = 0

    obstacles = generate_obstacles(10)  # Generate 10 obstacles
    moving_obstacles = generate_moving_obstacles(5)  # Generate 5 moving obstacles

    while not game_over:

        while game_close:
            dis.fill(blue)
            message("You Lost! Press Q-Quit or C-Play Again", red)
            Your_score(Length_of_snake - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        if special_food_active:
            pygame.draw.rect(dis, orange, [special_foodx, special_foody, snake_block, snake_block])
        if speed_food_active:
            pygame.draw.rect(dis, yellow, [speed_foodx, speed_foody, snake_block, snake_block])
        if freeze_food_active:
            pygame.draw.rect(dis, purple, [freeze_foodx, freeze_foody, snake_block, snake_block])

        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head:
                lives -= 1
                if lives == 0:
                    game_close = True

        for obs in obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                lives -= 1
                if lives == 0:
                    game_close = True

        for obs in moving_obstacles:
            if x1 == obs[0] and y1 == obs[1]:
                lives -= 1
                if lives == 0:
                    game_close = True

        if freeze_duration == 0:
            move_obstacles(moving_obstacles)

        our_snake(snake_block, snake_List)
        draw_obstacles(obstacles)
        draw_moving_obstacles(moving_obstacles)
        Your_score(Length_of_snake - 1)
        Your_lives(lives)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1
            if Length_of_snake % level_up_score == 0:
                snake_speed += speed_increment
                obstacles = generate_obstacles(10 + Length_of_snake // level_up_score * 5)
                moving_obstacles = generate_moving_obstacles(5 + Length_of_snake // level_up_score * 2)

        if x1 == special_foodx and y1 == special_foody:
            Length_of_snake += 5
            special_food_active = False

        if x1 == speed_foodx and y1 == speed_foody:
            snake_speed += 10
            speed_food_active = False

        if x1 == freeze_foodx and y1 == freeze_foody:
            freeze_duration = 50
            freeze_food_active = False

        if freeze_duration > 0:
            freeze_duration -= 1

        if not special_food_active:
            special_food_timer += 1
            if special_food_timer > 100:
                special_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                special_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                special_food_active = True
                special_food_timer = 0

        if not speed_food_active:
            speed_food_timer += 1
            if speed_food_timer > 150:
                speed_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                speed_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                speed_food_active = True
                speed_food_timer = 0

        if not freeze_food_active:
            freeze_food_timer += 1
            if freeze_food_timer > 200:
                freeze_foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
                freeze_foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
                freeze_food_active = True
                freeze_food_timer = 0

        clock.tick(snake_speed)

    pygame.quit()
    quit()

gameLoop()
