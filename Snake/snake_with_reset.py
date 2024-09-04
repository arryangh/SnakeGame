import random
import sys
import time
import pygame
pygame.mixer.init()
music = pygame.mixer.music.load("snake_music.mp3")
pygame.mixer.music.play(-1)


eat_sound = pygame.mixer.Sound("duDO.mp3")
lose_sound = pygame.mixer.Sound("lose.mp3")



class Game: #on crée une class Game
    def __init__(self):
        self.snake = Snake() #constitué d'un snake
        self.food = Food() # et d'un food (qui est regéneré si on le mange)
        self.point = 0

    def update(self): #la fonction update de la class Game appelle juste la fonction move snake de la class Snake
        self.snake.move_snake()
        self.check_head_on_food()
        self.game_over()

    def draw_game_element(self):
        self.food.draw_food()
        self.snake.draw_snake()
    def check_head_on_food(self):
        snake_length = len(self.snake.body)
        snake_head_block = self.snake.body[snake_length - 1]
        food_block = self.food.block


        if snake_head_block.x == food_block.x and snake_head_block.y == food_block.y:
            self.generate_food()
            self.point += 1
            eat_sound.play()
        else:
            if self.snake.direction != "STOP":
                self.snake.body.pop(0)

    def generate_food(self):
        self.food = Food()
        should_generate_food = True

        while should_generate_food:
            count = 0
            for block in self.snake.body:
                if block.x == self.food.block.x and block.y == self.food.block.y:
                    count += 1

                if count == 0:
                    should_generate_food = False
                else:
                    self.food = Food()

    def game_over(self):
        snake_length = len(self.snake.body)
        snake_head = self.snake.body[snake_length - 1]

        if snake_head.x not in range(0, NB_COL) or snake_head.y not in range(0, NB_ROW):
            print("Vous avez touché le mur! ")
            self.snake.reset_snake()
            lose_sound.play()

        for block in self.snake.body[0:snake_length - 1]:
            if block.x == snake_head.x and block.y == snake_head.y:
                self.snake.reset_snake()
                print("Vous vous êtes touché! ")
                lose_sound.play()




class Snake:
    def __init__(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"

    def draw_snake(self):
        for block in self.body:
            x_coord = block.x * CELL_SIZE
            y_coord = block.y * CELL_SIZE
            block_rect = pygame.Rect(x_coord, y_coord, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("blue"), block_rect)

    def move_snake(self):
        snake_block_count = len(self.body)
        old_head = self.body[snake_block_count - 1]

        if self.direction == "RIGHT":
            new_head = Block(old_head.x + 1, old_head.y)
            self.body.append(new_head)


        elif self.direction == "LEFT":
            new_head = Block(old_head.x - 1, old_head.y)
            self.body.append(new_head)  # on ajoute la nouvelle tête à la liste des block composants le snake


        elif self.direction == "TOP":
            new_head = Block(old_head.x, old_head.y - 1)
            self.body.append(new_head)  # on ajoute la nouvelle tête à la liste des block composants le snake


        elif self.direction == "DOWN":
            new_head = Block(old_head.x, old_head.y + 1)
            self.body.append(new_head)  # on ajoute la nouvelle tête à la liste des block composants le snake


        else:  # si self.direction == "STOP"
            new_head = Block(old_head.x, old_head.y)

    def reset_snake(self):
        self.body = [Block(2, 6), Block(3, 6), Block(4, 6)]
        self.direction = "RIGHT"
        game.point = 0




class Block:
    def __init__(self, x_pos, y_pos):
        self.x = x_pos
        self.y = y_pos


class Food:
    def __init__(self):
        x = random.randint(0, NB_COL - 1)
        y = random.randint(0, NB_ROW - 1)
        self.block = Block(x, y)

    def draw_food(self):
        rect = pygame.Rect(self.block.x * CELL_SIZE, self.block.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, pygame.Color("red"), rect)


pygame.init()

NB_COL = 10
NB_ROW = 15
CELL_SIZE = 40

screen = pygame.display.set_mode((NB_COL * CELL_SIZE, NB_ROW * CELL_SIZE))
game_on = True
timer = pygame.time.Clock()


game = Game()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 200)


def show_grid():
    for i in range(0, NB_COL):
        for j in range(0, NB_ROW):
            rect = pygame.Rect(i * CELL_SIZE, j * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, pygame.Color("white"), rect, width=1)


while game_on:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == SCREEN_UPDATE:
            game.update()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if game.snake.direction != "DOWN":
                    game.snake.direction = "TOP"

            if event.key == pygame.K_DOWN:
                if game.snake.direction != "TOP":
                    game.snake.direction = "DOWN"
            if event.key == pygame.K_RIGHT:
                if game.snake.direction != "LEFT":
                    game.snake.direction = "RIGHT"
            if event.key == pygame.K_LEFT:
                if game.snake.direction != "RIGHT":
                    game.snake.direction = "LEFT"

            if event.key == pygame.K_SPACE:
                game.snake.direction = "STOP"

    screen.fill(pygame.Color("white"))
    pygame.display.set_caption(f"{game.point}")
    game.draw_game_element()
    show_grid()
    pygame.display.update()
    timer.tick(60)