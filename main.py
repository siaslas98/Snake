import pygame as pg
import sys, random
from pygame.locals import *
from constants import *
from snake import *

# TODO: Clean up code / Optimize in snake.py
# TODO: Create You Win Screen
# TODO: Create Pause Game State Mechanism
pg.init()

# Game Setup
fps_clock = pg.time.Clock()
text_font = pg.font.SysFont('Arial Rounded MT Bold', 60)
text_font2 = pg.font.SysFont('Arial Rounded MT Bold', 30)

WINDOW = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pg.display.set_caption("Snake")

def get_food_pos(snake):
    available_positions = ALL_POSITIONS - snake.occupied_positions
    return random.choice(list(available_positions))

def draw_food(screen, food_pos):
    pg.draw.rect(
                screen,
                (255, 0, 0),
                (food_pos[0] * 20, food_pos[1] * 20, 20, 20)
    )

def pause_game(screen):
    game_pause_message = "Game Paused, hit space bar to resume"
    game_pause_surf = text_font2.render(game_pause_message, True, (255, 255, 255))
    game_pause_rect = game_pause_surf.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                return 0
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    running = False
                    return None
                
            screen.fill(BACKGROUND)
            screen.blit(game_pause_surf, game_pause_rect)

            pg.display.update()
            fps_clock.tick(FPS)

def load_game_over(screen, snake):
    messages = [
        ("Game Over", text_font, 600 / 3), # message, font, position along the vertical axis
        (f"Score: {len(snake.body)}", text_font2, 600 / 2),
        ("---Press Space to Play Again---", text_font2, 600 / 2 + 100)
    ]

    rendered_texts= [
        (font.render(text, True, (255, 255, 255)), (800 / 2, y)) # surf, (x, y) position
        for text, font, y in messages
    ]

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
                
        screen.fill(BACKGROUND)
        for surf, pos in rendered_texts:
            rect = surf.get_rect(center=pos)
            screen.blit(surf, rect)

        pg.display.update()
        fps_clock.tick(FPS)

def main():
    running = True
    snake = Snake()
    food_pos = get_food_pos(snake)

    # The main game loop
    while running:
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
                    resume = pause_game(WINDOW)
                    if resume == 0:
                        pg.quit()
                        sys.exit()
                    
                        
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

        # Render elements of the game
        WINDOW.fill(BACKGROUND)
        snake.update_position()
        draw_food(WINDOW, food_pos)
        snake.draw(WINDOW)
        pg.display.update()
        fps_clock.tick(FPS)

if __name__ == "__main__":
    main()
