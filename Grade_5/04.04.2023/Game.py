import pygame
import random
import sys


def game_loop():
    pygame.init()
    white = (255, 255, 255)
    yellow = (255, 255, 102)
    black = (0, 0, 0)
    red = (213, 50, 80)
    green = (0, 255, 0)
    blue = (50, 153, 213)
    dis_width = 2000
    dis_height = 1000
    display = pygame.display.set_mode((dis_width, dis_height))
    pygame.display.set_caption('Змейка от жизни')
    clock = pygame.time.Clock()
    snake_block = 10
    snake_speed = 15
    font_style = pygame.font.SysFont("bahnschrift", 25)
    score_font = pygame.font.SysFont("comicsansms", 35)
    game_over = False
    game_close = False
    x1 = dis_width / 2
    y1 = dis_height / 2
    x1_change = 0
    y1_change = 0
    snake_list = []
    length_of_snake = 1
    food_x, food_y = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0,\
        round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
    while not game_over:
        display.fill(blue)

        while game_close:
            display.blit(
                font_style.render("Вы проиграли! Нажмите Q для выхода или C для повторной игры", True, red),
                [dis_width / 6, dis_height / 3])
            display.blit(score_font.render(f"Ваш счёт: {length_of_snake - 1}", True, yellow), [0, 0])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # Whenever a key is pressed down
            elif event.type == pygame.KEYDOWN:
                # W -> Up; S -> Down; A -> Left; D -> Right
                if event.key == pygame.K_UP or event.key == ord('w'):
                    y1_change = -snake_block
                    x1_change = 0
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    y1_change = snake_block
                    x1_change = 0
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    x1_change = -snake_block
                    y1_change = 0
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    x1_change = snake_block
                    y1_change = 0

                # Esc -> Create event to quit the game
                if event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        pygame.draw.rect(display, green, [food_x, food_y, snake_block, snake_block])
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        pygame.draw.rect(display, black, [snake_head[0], snake_head[1], snake_block, snake_block])

        if x1 == food_x and y1 == food_y:
            food_x = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
            food_y = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

            for point in snake_list:
                pygame.draw.rect(display, white, [point[0], point[1], snake_block, snake_block])

        display.blit(score_font.render(f"Ваш счёт: {length_of_snake - 1}", True, yellow), [0, 0])

        pygame.display.update()

        clock.tick(snake_speed)
    pygame.quit()
    quit()


if __name__ == "__main__":
    game_loop()
