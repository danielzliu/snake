import pygame
import random
import sys

class User:

        def  __init__(self):
                self.board_height = 15
                self.board_width = 15
                self.body_width = 25 


class Body:
        #class för varje ruta (koordinater) i spelet

        def __init__ (self, xpos, ypos, user, head_or_body, red_body_pic, green_body_pic):
                self.xpos = range(xpos , xpos + user.body_width)                                         
                self.ypos = range(ypos , ypos + user.body_width)

                if head_or_body == True:
                        self.image = pygame.transform.scale(red_body_pic, (user.body_width, user.body_width))

                elif head_or_body == False:
                        self.image = pygame.transform.scale(green_body_pic, (user.body_width, user.body_width))


class Food:
        #class för vaje mat

        def __init__ (self, xpos, ypos, user, food_pic):
                self.xpos = range(xpos , xpos + user.body_width)                                         
                self.ypos = range(ypos , ypos + user.body_width)
                self.image = pygame.transform.scale(food_pic, (user.body_width, user.body_width))

class Border:
        
        def __init__(self, xpos, ypos, user, border_pic):
                
                self.xpos = range(xpos , xpos + user.body_width)                                         
                self.ypos = range(ypos , ypos + user.body_width)
                self.image = pygame.transform.scale(border_pic, (user.body_width, user.body_width))
                

def open_window(gameDisplay):
    #Öppnar fönster för spelet
    pygame.init()
    pygame.display.set_caption('Snake')                                        #Namn på spel.
    gameDisplay.fill((255,255,255))
    pygame.display.update()

def create_borders(gameDisplay, user, border_pic):

        borders = []
        for xpos in range(user.board_width):
                for ypos in range(user.board_width):

                        if xpos == 0 or xpos == user.board_width -1 or ypos == 0 or ypos == user.board_width -1:

                                border = Border(xpos*user.body_width, ypos*user.body_width, user, border_pic)
                                borders.append(border)
                                gameDisplay.blit(border.image, (border.xpos[0], border.ypos[0]))

        return borders

def spawn_snake(gameDisplay, user, red_body_pic, green_body_pic):
        snake = []

        xpos = (user.board_width // 2) * user.body_width
        ypos = (user.board_height // 2)* user.body_width
        snake.append(Body(xpos, ypos, user,  True, red_body_pic, green_body_pic))
        snake.append(Body(xpos, ypos + user.body_width, user, False, red_body_pic, green_body_pic))

        return snake

def spawn_food(gameDisplay, user, food_pic, snake, borders): #DEN KAN FORTFARANDE SPAWNA PÅ ORMEN!

        xpos = [1]
        ypos = [1]
        first_try = True

        while check_if_collusion(xpos, ypos, snake, borders) == True or first_try == True:
                xpos = random.randint(1, user.board_width - 2) * user.body_width
                ypos = random.randint(1, user.board_width - 2) * user.body_width

                xpos = range(xpos , xpos + user.body_width)
                ypos = range(ypos , ypos + user.body_width)
                first_try = False
        
        food = Food(xpos[0], ypos[0], user, food_pic)
        gameDisplay.blit(food.image, (food.xpos[0], food.ypos[0]))
        return food

def check_if_collusion(xpos, ypos, snake, borders):
        
        obstacles_list = [snake, borders]
        for obstacles in obstacles_list:
                for obstacle in obstacles:
                        
                        if xpos[0] == obstacle.xpos[0] and ypos[0] == obstacle.ypos[0]:
                                
                                return True

        return False

        
def move(gameDisplay, user, snake,borders, direction, white_pic):
        if direction != '':
                old_xpos1 = snake[0].xpos
                old_ypos1 = snake[0].ypos

                for body in snake: #Tar bort de gamla bilderna
                        gameDisplay.blit(pygame.transform.scale(white_pic, (user.body_width, user.body_width)), (body.xpos[0], body.ypos[0])) 
                if direction == 'n' and snake[0].ypos[0] - user.body_width != snake[1].ypos[0]: 
                        snake[0].ypos = range(snake[0].ypos[0] - user.body_width, snake[0].ypos[0])
                
                elif direction == 's' and snake[0].ypos[0] + user.body_width != snake[1].ypos[0]:
                        snake[0].ypos = range(snake[0].ypos[0] + user.body_width, snake[0].ypos[0] + 2 * user.board_width)

                elif direction == 'w' and snake[0].xpos[0] - user.body_width != snake[1].xpos[0]:
                        snake[0].xpos = range(snake[0].xpos[0] - user.body_width, snake[0].xpos[0])

                elif direction == 'e' and snake[0].xpos[0] + user.body_width != snake[1].xpos[0]:
                        snake[0].xpos = range(snake[0].xpos[0] + user.body_width, snake[0].xpos[0] + 2 * user.board_width)

                for i in range(0, len(snake) - 1):
                        
                        if i % 2 == 0:
                                old_xpos2 = snake[i + 1].xpos
                                old_ypos2 = snake[i + 1].ypos
                                snake[i + 1].xpos = old_xpos1
                                snake[i + 1].ypos = old_ypos1

                        elif i % 2 == 1:
                                old_xpos1 = snake[i + 1].xpos
                                old_ypos1 = snake[i + 1].ypos
                                snake[i + 1].xpos = old_xpos2
                                snake[i + 1].ypos = old_ypos2

                collided = check_if_collusion(snake[0].xpos, snake[0].ypos, snake[1:len(snake)-1], borders)

                if collided == True:
                        lose_game()
                        
                        

def grow_snake(user, snake, tail_xpos, tail_ypos, red_body_pic, green_body_pic):
        snake.append(Body(tail_xpos, tail_ypos, user, False, red_body_pic, green_body_pic))
        just_eaten = False

        return just_eaten

def lose_game():

        raise Exception('Game Over!')
                                                           

def close_window():
    #Stänger fönstret.
    pygame.quit()
    sys.exit()

def main():
        user = User()
        display_height = user.board_height * user.body_width
        display_width = user.board_width * user.body_width
        clock = pygame.time.Clock()
        gameDisplay = pygame.display.set_mode((display_width , display_height))   

        open_window(gameDisplay)

        white_pic = pygame.image.load('GFX/white.jpg')
        border_pic = pygame.image.load('GFX/border.jpg')
        red_body_pic = pygame.image.load('GFX/red_body.jpg')
        green_body_pic = pygame.image.load('GFX/green_body.jpg')
        food_pic = pygame.image.load('GFX/food.jpg')

        borders = create_borders(gameDisplay, user, border_pic)
        snake = spawn_snake(gameDisplay, user, red_body_pic, green_body_pic)
        food = spawn_food(gameDisplay, user, food_pic, snake, borders)
        just_eaten = False



        direction = ''
        while True:

                for event in pygame.event.get():
                    key = pygame.key.get_pressed()
                    
                    if event.type == pygame.QUIT:
                        close_window()

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP and snake[0].ypos[0] - user.body_width != snake[1].ypos[0]:
                                direction = 'n'
                        elif event.key == pygame.K_DOWN and snake[0].ypos[0] + user.body_width != snake[1].ypos[0]:
                                direction = 's'
                        elif event.key == pygame.K_LEFT and snake[0].xpos[0] - user.body_width != snake[1].xpos[0]:
                                direction = 'w'
                        elif event.key == pygame.K_RIGHT and snake[0].xpos[0] + user.body_width != snake[1].xpos[0]:
                                direction = 'e'
                
                move(gameDisplay, user, snake, borders, direction, white_pic)
                

                if just_eaten == True:
                        just_eaten = grow_snake(user, snake, tail_xpos, tail_ypos, red_body_pic, green_body_pic)
                        
                        

                if snake[0].xpos[0] == food.xpos[0] and snake[0].ypos[0] == food.ypos[0]: #Om ormen äter maten
                        food = spawn_food(gameDisplay, user, food_pic, snake,borders)
                        tail_xpos = snake[-1].xpos[0]
                        tail_ypos = snake[-1].ypos[0]
                        just_eaten = True

                for body in snake: #Uppdaterar skärmen
                        gameDisplay.blit(body.image, (body.xpos[0], body.ypos[0]))

                pygame.display.update()

                clock.tick(10)

if __name__ == '__main__':

        main()
        
