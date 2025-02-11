import pygame as pg
import sys, random
from pygame.locals import *
from constants import *
from snake import *

# TODO: Clean up code / Optimize

pg.init()

# Game Setup
fps_clock = pg.time.Clock()
text_font = pg.font.SysFont('Arial Rounded MT Bold', 60)
text_font2 = pg.font.SysFont('Arial Rounded MT Bold', 30)

WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Snake")

def get_food_pos(snake):
    while True:
        x_pos = random.randrange(40)
        y_pos = random.randrange(30)
        food_pos = (x_pos, y_pos)

        if food_pos not in snake.occupied_positions:
            return food_pos

def draw_food(screen, food_pos):
    pg.draw.rect(
                screen,
                (255, 0, 0),
                (food_pos[0] * 20, food_pos[1] * 20, 20, 20)
    )

def load_game_over(screen, snake):
    screen.fill(BACKGROUND)
    game_over_surf = text_font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_surf.get_rect(center=(800 / 2, 600 / 3))

    score_surf = text_font2.render(f'Score: {len(snake.body)}', True, (255, 255, 255))
    score_rect = score_surf.get_rect(center=(800 / 2, 600 / 2))

    message_surf = text_font2.render('---Press Space to Play Again---', True, (255, 255, 255))
    message_rect = message_surf.get_rect(center=(800 / 2, 600 / 2 + 100))
    
    
    screen.blit(game_over_surf, game_over_rect)
    screen.blit(score_surf, score_rect)
    screen.blit(message_surf, message_rect)
    pg.display.flip()
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False
                    return 1
        fps_clock.tick(FPS)

def main():
    looping = True
    snake = Snake()
    food_pos = get_food_pos(snake)

    # The main game loop
    while looping:
        # Get inputs
        for event in pg.event.get():
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pg.K_UP:
                    new_direction = Direction.UP
                elif event.key == pg.K_DOWN:
                    new_direction = Direction.DOWN
                elif event.key == pg.K_LEFT:
                    new_direction = Direction.LEFT
                elif event.key == pg.K_RIGHT:
                    new_direction = Direction.RIGHT
                elif event.key == pg.K_SPACE:
                    pass # We will pause the game and load pause screen

                if snake.is_valid_direction_change(new_direction):
                    snake.direction = new_direction
        
        collision_check = snake.check_for_collision(food_pos)
        if collision_check == -1:
            continue_game = load_game_over(WINDOW, snake)
            if continue_game:
                snake = Snake()
                food_pos = get_food_pos(snake)
            else:
                pg.quit()
                sys.exit()

        elif collision_check == 1:
            food_pos = get_food_pos(snake)
        
        snake.update_position()

        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        draw_food(WINDOW, food_pos)
        snake.draw(WINDOW)
        pg.display.update()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()
