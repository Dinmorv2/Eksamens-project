import pygame
from random import randrange as rnd, randint

pygame.init()

run = True
game_active = False
game_over = False
game_won = False

skærm_bredde = 1200
skærm_højde = 800

screen = pygame.display.set_mode((skærm_bredde, skærm_højde))

pygame.display.set_caption("Breakout")

ur = pygame.time.Clock()

x = skærm_bredde / 2 - 100

#Opret spillerens rektangel én gang uden for løkken.
player = pygame.Rect(x, skærm_højde - 50, 200, 20)

# Kugle (ball)
Kugle_radius = 10
kugle_hastighed = 6
kugle_flade = int(Kugle_radius * 2 ** 0.5)
kugle = pygame.Rect(rnd(kugle_flade, skærm_bredde - kugle_flade), skærm_højde // 2, kugle_flade, kugle_flade)
x_2 = kugle_hastighed
y_2 = kugle_hastighed

# Kugle tæller
ball_count = 1

# Blocks
block_cols = 10
block_rows = 5
block_width = skærm_bredde // block_cols - 10  # Juster bredden, så den passer inden for skærmen med lidt plads.
block_height = skærm_højde // (block_rows * 6)  # Juster højden baseret på skærmens højde.
blocks = []

# Opret blokke med tilfældige farver.
for row in range(block_rows):
    for col in range(block_cols):
        block_x = col * (block_width + 10) + 20
        block_y = row * (block_height + 10) + 20
        block = pygame.Rect(block_x, block_y, block_width, block_height)
        block_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        blocks.append((block, block_color))

# antal blokke tilbage
blocks_left = len(blocks)

# skrifttype for skift og knapper
font = pygame.font.Font(None, 74)
button_font = pygame.font.Font(None, 50)

# Startmenu knapper
start_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2 - 50, 200, 50)
quit_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2 + 50, 200, 50)

def show_start_menu():
    screen.fill((0, 0, 0))

    # Title
    titel_text = font.render("Breakout", True, (0, 0, 255))
    screen.blit(titel_text, (skærm_bredde / 2 - 100, skærm_højde / 2 - 200))

    # Start knaps
    pygame.draw.rect(screen, (0, 255, 0), start_button,border_radius=25)
    start_text = button_font.render('Spil', True, (255, 255, 255))
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)
    
    # Afslut knap
    pygame.draw.rect(screen, (255, 0, 0), quit_button,border_radius=25)
    quit_text = button_font.render('Afslut', True, (255, 255, 255))
    quit_text_rect = quit_text.get_rect(center=quit_button.center)
    screen.blit(quit_text, quit_text_rect)

def reset_game():
    global kugle, x_2, y_2, game_over, game_won, player, blocks, blocks_left, ball_count, balls
    x = skærm_bredde / 2 - 100
    player = pygame.Rect(x, skærm_højde - 50, 200, 20)
    kugle = pygame.Rect(rnd(kugle_flade, skærm_bredde - kugle_flade), skærm_højde // 2, kugle_flade, kugle_flade)
    x_2 = kugle_hastighed
    y_2 = kugle_hastighed
    game_over = False
    game_won = False
    ball_count = 1
    balls = []
    blocks = []
    for row in range(block_rows):
        for col in range(block_cols):
            block_x = col * (block_width + 10) + 20
            block_y = row * (block_height + 10) + 20
            block = pygame.Rect(block_x, block_y, block_width, block_height)
            block_color = (randint(0, 255), randint(0, 255), randint(0, 255))
            blocks.append((block, block_color))
    # Reset blocks_left
    blocks_left = len(blocks)

def spawn_ball(x, y):
    return pygame.Rect(x, y, kugle_flade, kugle_flade)

balls = []

# Program loop
while run:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            
            # Hvis spillet ikke er aktivt, tjek for startmenu knap klik
            if not game_active:
                if start_button.collidepoint(mouse_pos):
                    game_active = True
                    reset_game()
                elif quit_button.collidepoint(mouse_pos):
                    run = False
                    
            # Hvis spillet er aktivt, tjek for genstart, startmenu eller afslut knap klik
            elif game_over or game_won:
                try_again_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2, 200, 50)
                start_menu_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2 - 70, 200, 50)
                if try_again_button.collidepoint(mouse_pos):
                    reset_game()
                    game_active = True
                elif start_menu_button.collidepoint(mouse_pos):
                    game_active = False
                elif quit_button.collidepoint(mouse_pos):
                    run = False

    if game_active:
        if not game_over and not game_won:
            # Get the state of all keyboard buttons
            keys = pygame.key.get_pressed()

            # Update player position based on key
            if keys[pygame.K_RIGHT] and player.right < skærm_bredde:
                player.move_ip(10, 0)
            if keys[pygame.K_LEFT] and player.left > 0:
                player.move_ip(-10, 0)

            # Move the main ball
            kugle.x += x_2
            kugle.y += y_2

            # Ball collision with walls
            if kugle.left <= 0 or kugle.right >= skærm_bredde:
                x_2 = -x_2
            if kugle.top <= 0:
                y_2 = -y_2
            if kugle.bottom >= skærm_højde:
                if ball_count > 1:
                    ball_count -= 1
                    kugle = balls.pop(0)
                else:
                    game_over = True  # Trigger game over when the ball hits the bottom edge

            # Ball collision with player paddle
            if kugle.colliderect(player):
                y_2 = -y_2  # Reverse the vertical direction

            # Ball collision with blocks
            for block, block_color in blocks[:]:
                if kugle.colliderect(block):
                    blocks.remove((block, block_color))
                    blocks_left -= 1  # Decrease blocks_left when a block is removed
                    y_2 = -y_2
                    if randint(1, 5) == 1:  # Randomly spawn new balls sometimes
                        balls.append(spawn_ball(block.x + block.width // 2, block.y))
                    break

            # Check if all blocks are removed
            if blocks_left == 0:
                game_won = True

            # Move extra balls
            for ball in balls:
                ball.y += 3  # Adjust the falling speed

                # Check for collision with player paddle for extra balls
                if ball.colliderect(player):
                    balls.remove(ball)
                    ball_count += 1
                    new_ball = spawn_ball(player.centerx, player.top - kugle_flade)
                    balls.append(new_ball)

                # Remove the ball if it goes out of the screen
                if ball.bottom >= skærm_højde:
                    balls.remove(ball)
                    ball_count -= 1

        # Clear the screen
        screen.fill((0, 0, 0))

        if not game_over and not game_won:
            # Draw the player rectangle
            pygame.draw.rect(screen, (255, 255, 0), player)

            # Draw the main ball
            pygame.draw.circle(screen, (255, 255, 255), kugle.center, Kugle_radius)

            # Draw the blocks
            for block, block_color in blocks:
                pygame.draw.rect(screen, block_color, block)

            # Draw extra balls
            for ball in balls:
                pygame.draw.circle(screen, (255, 255, 255), ball.center, Kugle_radius)

        elif game_over or game_won:
            # Display Game Over or You Won message
            if game_over:
                end_text = font.render('Game Over', True, (255, 0, 0))
            else:
                end_text = font.render('Du har vundet!', True, (0, 255, 0))
            text_rect = end_text.get_rect(center=(skærm_bredde / 2, skærm_højde / 2 - 100))
            screen.blit(end_text, text_rect)

            # Display Try Again button
            try_again_text = button_font.render('Spil igen', True, (255, 255, 255))
            try_again_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2, 200, 50)
            pygame.draw.rect(screen, (0, 255, 0), try_again_button, border_radius=25)
            try_again_text_rect = try_again_text.get_rect(center=try_again_button.center)
            screen.blit(try_again_text, try_again_text_rect)

            # Display Quit button
            quit_text = button_font.render('Afslut', True, (255, 255, 255))
            quit_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2 + 70, 200, 50)
            pygame.draw.rect(screen, (255, 0, 0), quit_button, border_radius=25)
            quit_text_rect = quit_text.get_rect(center=quit_button.center)
            screen.blit(quit_text, quit_text_rect)

            # Display start menu button
            start_menu_text = button_font.render('Start menu', True, (255, 255, 255))
            start_menu_button = pygame.Rect(skærm_bredde / 2 - 100, skærm_højde / 2 - 70, 200, 50)
            pygame.draw.rect(screen, (0, 255, 0), start_menu_button, border_radius=25)
            start_menu_text_rect = start_menu_text.get_rect(center=start_menu_button.center)
            screen.blit(start_menu_text, start_menu_text_rect)

    else:
        # Show start menu
        show_start_menu()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate at 60 FPS
    ur.tick(60)

# Quit Pygame
pygame.quit()
