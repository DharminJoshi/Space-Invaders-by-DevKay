"""
Space Invaders Game by DevKay
-----------------------------
Copyright (c) 2025 DevKay. All rights reserved.

This code is part of the Space Invaders game created by DevKay. You may not use,
modify, or distribute this code without permission from the original author, except
for personal use and non-commercial purposes. For inquiries, please contact DevKay
via GitHub or Email at info.dharmin@gmail.com .

Description:
This is a simple space-themed shooter game where the player controls a fighter plane that moves left and right to shoot down incoming alien enemies. The player earns points for each alien destroyed and can use power-ups like extra lives, bombs, and a double score boost. The player progresses through different levels, each with faster and more numerous enemies. The game ends when the player runs out of lives.

Features:
- Multiple levels with increasing difficulty.
- Power-ups: Extra Life, Bombs, and Double Score.
- High-score tracking.
- Pause and resume functionality.
- Customizable player and enemy sprites.

Developed by: Dharmin Joshi / DevKay
GitHub: https://github.com/DharminJoshi
Date: 2025
"""


import random
import time
from turtle import Screen, Turtle

# Set up the screen
screen = Screen()
screen.bgcolor("black")
screen.title("Space Invaders by DevKay")
screen.setup(width=800, height=600)

# Register custom shapes
screen.register_shape("fighter_plane.gif")  # Replace with the path to your fighter plane image
screen.register_shape("alien_resized.gif")  # Replace with the path to your alien image
screen.register_shape("explosion.gif")

# Game state variables
game_over = False
game_paused = False
lives = 3  # Initial number of lives
aliens_destroyed = 0  # Variable to count aliens destroyed

# Create the player turtle (fighter plane)
player = Turtle()
player.shape("fighter_plane.gif")
player.penup()
player.speed("fastest")
player.setposition(0, -250)
player.setheading(90)

# Set the player's movement speed
player_speed = 15

# Create a list to manage bullets
bullets = []
bullet_cooldown = 0.5
last_bullet_time = 0

# Create multiple enemies (aliens)
num_enemies = 5
enemies = []

def create_enemies(num):
    for _ in range(num):
        enemy = Turtle()
        enemy.shape("alien_resized.gif")
        enemy.penup()
        enemy.speed("fastest")
        x = random.randint(-200, 200)
        y = random.randint(100, 250)
        enemy.setposition(x, y)
        enemies.append(enemy)

create_enemies(num_enemies)

# Set the initial enemy speed
enemy_speed = 2

# Set the initial score
score = 0

# Set the initial level
level = 1

# Define levels and corresponding parameters
level_params = {
    1: {"enemy_speed": 2, "bullet_speed": 20, "num_enemies": 5},
    2: {"enemy_speed": 3, "bullet_speed": 25, "num_enemies": 7},
    3: {"enemy_speed": 4, "bullet_speed": 30, "num_enemies": 10},
    4: {"enemy_speed": 5, "bullet_speed": 35, "num_enemies": 12},
    5: {"enemy_speed": 6, "bullet_speed": 40, "num_enemies": 15},
}

# Power-ups
power_ups = {
    "extra_life": {"uses": 3, "max_uses": 3},
    "bomb": {"uses": 3, "max_uses": 3},
    "double_score": {"uses": 3, "max_uses": 3, "active": False, "duration": 5}
}

# Create the score, level, lives, and aliens destroyed display
score_display = Turtle()
score_display.color("white")
score_display.penup()
score_display.speed("fastest")
score_display.setposition(-380, 250)  # Adjusted position to prevent overlap
score_display.hideturtle()

# Create the power-up display
power_up_display = Turtle()
power_up_display.color("white")
power_up_display.penup()
power_up_display.speed("fastest")
power_up_display.setposition(200, 250)  # Adjusted position
power_up_display.hideturtle()

# Functions for player movement
def move_left():
    if not game_paused:
        x = player.xcor()
        x -= player_speed
        player.setx(max(x, -380))

def move_right():
    if not game_paused:
        x = player.xcor()
        x += player_speed
        player.setx(min(x, 380))

def fire_bullet():
    global last_bullet_time
    if not game_paused:
        current_time = time.time()
        if current_time - last_bullet_time >= bullet_cooldown:
            new_bullet = Turtle()
            new_bullet.color("yellow")
            new_bullet.shape("triangle")
            new_bullet.penup()
            new_bullet.speed("fastest")
            new_bullet.setheading(90)
            new_bullet.shapesize(0.5, 0.5)
            new_bullet.goto(player.xcor(), player.ycor() + 10)
            bullets.append(new_bullet)
            last_bullet_time = current_time

def is_collision(t1, t2):
    return t1.distance(t2) < 20

def create_explosion(x, y):
    explosion = Turtle()
    explosion.shape("explosion.gif")
    explosion.penup()
    explosion.speed("fastest")
    explosion.setposition(x, y)
    screen.update()
    time.sleep(0.5)
    explosion.hideturtle()

def update_score_display():
    score_display.clear()
    score_display.write("Score: {}".format(score), align="left", font=("Courier", 16, "normal"))
    score_display.goto(-380, 230)  # Position for level display
    score_display.write("Level: {}".format(level), align="left", font=("Courier", 16, "normal"))
    score_display.goto(-380, 210)  # Position for lives display
    score_display.write("Lives: {}".format(lives), align="left", font=("Courier", 16, "normal"))
    score_display.goto(-380, 190)  # Position for aliens destroyed display
    score_display.write("Aliens Destroyed: {}".format(aliens_destroyed), align="left", font=("Courier", 16, "normal"))
    score_display.goto(-380, 250)  # Reset position for next update

def update_power_up_display():
    power_up_display.clear()
    power_up_display.write(
        "Extra Life: {}  Bomb: {}  Double Score: {}".format(
            power_ups["extra_life"]["uses"],
            power_ups["bomb"]["uses"],
            power_ups["double_score"]["uses"]
        ),
        align="left",
        font=("Courier", 16, "normal"),
    )

def display_message(message):
    message_display = Turtle()
    message_display.color("white")
    message_display.penup()
    message_display.speed("fastest")
    message_display.hideturtle()
    message_display.goto(0, 0)
    message_display.write(message, align="center", font=("Courier", 24, "normal"))
    screen.update()  # Ensure the message is shown immediately
    time.sleep(2)
    message_display.clear()

def reset_game():
    global score, level, enemy_speed, enemies, game_over, game_paused, lives, aliens_destroyed
    score = 0
    level = 1
    lives = 3  # Reset lives
    aliens_destroyed = 0  # Reset aliens destroyed
    enemy_speed = level_params[level]["enemy_speed"]
    for enemy in enemies:
        enemy.hideturtle()
    enemies.clear()
    bullets.clear()
    create_enemies(level_params[level]["num_enemies"])
    player.showturtle()
    update_score_display()
    update_power_up_display()
    game_over = False
    game_paused = False

def reset_level():
    global enemies, bullets, enemy_speed
    for enemy in enemies:
        enemy.hideturtle()
    enemies.clear()
    for bullet in bullets:
        bullet.hideturtle()
    bullets.clear()
    create_enemies(level_params[level]["num_enemies"])
    enemy_speed = level_params[level]["enemy_speed"]

def use_extra_life():
    global lives
    if power_ups["extra_life"]["uses"] > 0 and lives < 5:  # Limit to a maximum of 5 lives
        power_ups["extra_life"]["uses"] -= 1
        lives += 1
        update_score_display()
        update_power_up_display()

def use_bomb():
    global score, aliens_destroyed
    if power_ups["bomb"]["uses"] > 0:
        power_ups["bomb"]["uses"] -= 1
        update_power_up_display()
        for enemy in enemies:
            if enemy.isvisible():
                create_explosion(enemy.xcor(), enemy.ycor())
                enemy.hideturtle()
                aliens_destroyed += 1  # Increment aliens destroyed count
        enemies.clear()
        score += 100 * len(enemies)
        update_score_display()

def use_double_score():
    if power_ups["double_score"]["uses"] > 0:
        power_ups["double_score"]["uses"] -= 1
        power_ups["double_score"]["active"] = True
        screen.ontimer(deactivate_double_score, power_ups["double_score"]["duration"] * 1000)
        update_power_up_display()

def deactivate_double_score():
    power_ups["double_score"]["active"] = False

def show_intro():
    intro_display = Turtle()
    intro_display.color("white")
    intro_display.penup()
    intro_display.speed("fastest")
    intro_display.hideturtle()
    intro_display.goto(0, 0)
    intro_display.write("Welcome to the Shooting Game!\nDestroy the aliens and survive!\nGame starting in 5 seconds...", align="center", font=("Courier", 24, "normal"))
    screen.update()
    time.sleep(5)
    intro_display.clear()

def show_main_menu():
    menu_display = Turtle()
    menu_display.color("white")
    menu_display.penup()
    menu_display.speed("fastest")
    menu_display.hideturtle()
    menu_display.goto(0, 0)
    menu_display.write("Main Menu\nPress 's' to start or 'q' to quit.", align="center", font=("Courier", 24, "normal"))
    return menu_display

def show_in_game_menu():
    global game_paused
    game_paused = True
    in_game_menu_display = Turtle()
    in_game_menu_display.color("white")
    in_game_menu_display.penup()
    in_game_menu_display.speed("fastest")
    in_game_menu_display.hideturtle()
    in_game_menu_display.goto(0, 0)
    in_game_menu_display.write("Paused\nPress 'r' to resume or 'q' to quit.", align="center", font=("Courier", 24, "normal"))
    return in_game_menu_display

def start_game():
    global game_over, game_paused
    game_over = False
    game_paused = False
    show_intro()
    reset_game()

def quit_game():
    global game_over
    game_over = True
    screen.bye()

def pause_game():
    if not game_paused:
        in_game_menu_display = show_in_game_menu()
        screen.onkeypress(lambda: resume_game(in_game_menu_display), "r")
        screen.onkeypress(quit_game, "q")

def resume_game(menu_display):
    global game_paused
    game_paused = False
    menu_display.clear()
    screen.onkeypress(pause_game, "p")
    screen.onkeypress(quit_game, "q")

def toggle_fullscreen():
    root = screen.getcanvas().winfo_toplevel()
    fullscreen = not root.attributes('-fullscreen')
    root.attributes('-fullscreen', fullscreen)
    if fullscreen:
        screen.setup(width=root.winfo_screenwidth(), height=root.winfo_screenheight())
    else:
        screen.setup(width=800, height=600)

# Keyboard bindings
screen.listen()
screen.onkeypress(move_left, "Left")
screen.onkeypress(move_right, "Right")
screen.onkeypress(fire_bullet, "space")
screen.onkeypress(use_extra_life, "e")
screen.onkeypress(use_bomb, "b")
screen.onkeypress(use_double_score, "d")
screen.onkeypress(pause_game, "p")
screen.onkeypress(toggle_fullscreen, "F11")
screen.onkeypress(toggle_fullscreen, "Alt_L")

# Main game loop
menu_display = show_main_menu()
screen.onkeypress(lambda: (menu_display.clear(), start_game()), "s")
screen.onkeypress(quit_game, "q")

while True:
    if not game_over:
        if not game_paused:
            for enemy in enemies:
                enemy.setx(enemy.xcor() + enemy_speed)

                # Reverse enemy direction and move down if it hits the boundary
                if enemy.xcor() > 380 or enemy.xcor() < -380:
                    enemy_speed *= -1
                    for e in enemies:
                        e.sety(e.ycor() - 40)

                # Check for collision between bullet and enemy
                for bullet in bullets[:]:
                    if is_collision(bullet, enemy):
                        bullet.hideturtle()
                        bullets.remove(bullet)
                        x = random.randint(-200, 200)
                        y = random.randint(100, 250)
                        enemy.setposition(x, y)
                        score_increment = 20 if power_ups["double_score"]["active"] else 10
                        score += score_increment
                        aliens_destroyed += 1  # Increment aliens destroyed count
                        update_score_display()

                # Check for collision between player and enemy
                if is_collision(player, enemy):
                    lives -= 1
                    if lives == 0:
                        player.hideturtle()
                        for e in enemies:
                            e.hideturtle()
                        score_display.clear()
                        score_display.write("Game Over! Final Score: {}".format(score), align="center", font=("Courier", 24, "normal"))
                        game_over = True
                        break
                    else:
                        x = random.randint(-200, 200)
                        y = random.randint(100, 250)
                        enemy.setposition(x, y)
                        player.setposition(0, -250)
                        update_score_display()

            # Move the bullets
            for bullet in bullets[:]:
                bullet.sety(bullet.ycor() + level_params[level]["bullet_speed"])
                # Check if the bullet has gone out of bounds
                if bullet.ycor() > 275:
                    bullet.hideturtle()
                    bullets.remove(bullet)

            # Check if all enemies are destroyed and increase level
            if score // 100 >= level and level < len(level_params):
                display_message(f"Congratulations! Level {level} completed.\nGet ready for Level {level + 1}!")
                level += 1
                reset_level()
                update_score_display()

        screen.update()

# Keep the window open after the game ends
screen.mainloop()
