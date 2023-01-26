import pygame
import random
from pygame.constants import QUIT
import webbrowser
from copy import deepcopy
import time
import os
from collections import deque

#initializer
pygame.init()
pygame.font.init()

class Food:
    def __init__(self, name, ingredients, similarity = 0):
        self.name = name
        self.ingredients = ingredients

    def __str__(self):
        return str(self.name)

    def append_ingredients(self, list):
        pass

    def calculate_cooking_order(self):
        pass

class Dot:
    active = True
    def __init__(self, display):
        self.x = random.randint(0, display_size[0]//10-1) * 10
        self.y = random.randint(0, display_size[1]//10-1) * 10
        self.display = display

    def draw(self):
        pygame.draw.circle(self.display, WHITE, [self.x, self.y], 5)

class Ingredients:
    def __init__(self, category, name, cooking_time=0, existence=0):
        self.category = category
        self.name = name
        self.cooking_time = cooking_time
        self.existence = existence

class Ingredient_Button:
    def __init__(self, name, center, existence=0, button_size=(120,30)):
        self.button_size = button_size
        self.name = name
        self.center = center
        self.existence = existence
        self.text = ingredient_font.render(self.name, True, WHITE)
        self.Rect = self.text.get_rect()
        self.Rect.center = self.center
    def draw(self):
        if self.existence == 0:
            pygame.draw.rect(game_display, RED, [self.center[0]-self.button_size[0]//2, self.center[1]-self.button_size[1]//2, self.button_size[0], self.button_size[1]]) 
        else:
            pygame.draw.rect(game_display, GREEN, [self.center[0]-self.button_size[0]//2, self.center[1]-self.button_size[1]//2, self.button_size[0], self.button_size[1]])
        game_display.blit(self.text, self.Rect)        

    def click(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x,y = event.pos
            if self.center[0]-self.button_size[0]//2<x<self.center[0]+self.button_size[0]//2 and self.center[1]-self.button_size[1]//2<y<self.center[1]+self.button_size[1]//2:
                self.existence +=1
                self.existence = self.existence % 2    
                #file overwrite
                for i in range(len(ingredient_category_list)):
                    for p in range(len(ingredient_list[i])):
                        if ingredient_list[i][p].name == self.name:
                            try:
                                existence_memory_list[i][p] = self.existence 
                            except:
                                existence_memory_list[i].append(self.existence)     
                ingredient_existence.write(str(existence_memory_list)+'\n')

class VS_Button:
    def __init__(self, name, center, t, button_size=(300,60)):
        self.button_size = button_size
        self.name = name
        self.center = center
        self.t = t
        self.text = ingredient_font.render(self.name, True, WHITE)
        self.Rect = self.text.get_rect()
        self.Rect.center = self.center
    def draw(self):
        pygame.draw.rect(game_display, GREEN, [self.center[0]-self.button_size[0]//2, self.center[1]-self.button_size[1]//2, self.button_size[0], self.button_size[1]])
        game_display.blit(self.text, self.Rect)

    def click(self):
        if event.type == pygame.MOUSEBUTTONDOWN:
            y,z = event.pos           
            if self.center[0]-self.button_size[0]//2<y<self.center[0]+self.button_size[0]//2 and self.center[1]-self.button_size[1]//2<z<self.center[1]+self.button_size[1]//2:
                    x = self.t
                    page_log.append(deepcopy(self.t))

#constants
BLACK=(0, 0, 0)
RED = (255, 0, 0)
WHITE=(255, 255, 255)
GREEN=(126, 200, 80)
PINK=(238, 195, 218)
PURPLE=(172, 110, 217)
SKY_BLUE=(174, 209, 247)
BLUE = (98, 107, 215)
YELLOW = (250, 218, 94)

#size and positions
display_size = (900, 700)
button_size = (300, 50)
category_button_size = (120, 30)
ingredient_button_size = (120, 30)
my_ingredients_button = (display_size[0]*0.32, display_size[1]*0.5)
recommendation_button = (display_size[0]*0.32, display_size[1]*0.6)
cooking_time_button = (display_size[0]*0.32, display_size[1]*0.7)
append_button = (display_size[0]*0.32, display_size[1]*0.8)

#display setting
game_display = pygame.display.set_mode(display_size)
dots = [Dot(game_display) for _ in range(50)]
pygame.display.set_caption('냉장고를 부탁해')

##file reading and writing
#read recipe
with open('recipe.txt', 'r+') as recipe:
    recipe_list = []
    for line in recipe:
        if '\n' in line:
            memory_line = line[:-1].split(',')
        else:
            memory_line = line.split(',')
        recipe_list.append(Food(memory_line[0],memory_line[1:]))

#read ingredients
ingredient_list = []
ingredient_category_list = []
ingredient_count_list = []
ingredient_button_list = []
category_x_list = [1.01,1.02,1.03,1.04,1.05,1.06,1.07,1.08,1.09,1.1,1.11,1.12]
with open('ingredient.txt', 'r+') as ingredients:
    for line in ingredients:
        if '\n' in line:
            memory_line = line[:-1].split(',')
        else:
            memory_line = line.split(',')
        ingredient_list.append([])
        a=0
        for i in range(len(memory_line)-1):
            ingredient_list[-1].append(Ingredients(memory_line[0],memory_line[i+1]))
            a += 1
            if memory_line[0] not in ingredient_category_list:
                ingredient_category_list.append(memory_line[0])
            ingredient_count_list.append(a)
#font
font = pygame.font.Font('훈새마을운동R.ttf', 100)
button_font = pygame.font.Font('훈새마을운동R.ttf', 20)
ingredient_font = pygame.font.Font('훈새마을운동R.ttf', 20)
recipe_title_font = pygame.font.Font('훈새마을운동R.ttf', 50)
recipe_font = pygame.font.Font('훈새마을운동R.ttf',30)
recipe_ingredient_font = pygame.font.Font('훈새마을운동R.ttf',20)

#ingredient text
ingredient_text_list= []
ingredient_Rect_list = []
for p in range(len(ingredient_list)):
    ingredient_text_list.append([])
    ingredient_Rect_list.append([])
    ingredient_button_list.append([])
    position = deque(i+1 for i in range(5))
    for i in range(len(ingredient_list[p])):
        ingredient_text_list[p].append(ingredient_font.render(ingredient_list[p][i].name, True, WHITE))
        ingredient_Rect_list[p].append(ingredient_text_list[p][i].get_rect())
        if len(ingredient_list[p]) == 1:
            ingredient_Rect_list[p][i].center = (display_size[0]//2,display_size[1]//2)
            ingredient_button_list[p].append(Ingredient_Button(ingredient_list[p][i].name,ingredient_Rect_list[p][i].center))
        else:
            number_of_lines = len(ingredient_list[p]) // 5 + 1
            ingredient_Rect_list[p][i].center = (display_size[0]//6*position[0],display_size[1]//(number_of_lines+1)*(i//5+1))
            position.rotate(-1)
            ingredient_button_list[p].append(Ingredient_Button(ingredient_list[p][i].name,ingredient_Rect_list[p][i].center))
            
#write if ingredient exists
ingredient_existence = open('ingredient existence.txt', 'r+')
if os.stat('ingredient existence.txt').st_size == 0:
    existence_memory_list = []
    for i in range(len(ingredient_category_list)):
        existence_memory_list.append([])
    for i in range(len(ingredient_category_list)):
        for p in range(len(ingredient_list[i])):
            existence_memory_list[i].append(ingredient_list[i][p].existence)        
    ingredient_existence.write(str(existence_memory_list)+'\n')
else:
    ingredient_existence_list = ingredient_existence.readlines()
    existence_memory_list = eval(ingredient_existence_list[-1])
    for i in range(len(ingredient_list)):
        for p in range(len(ingredient_list[i])):
            try:
                ingredient_list[i][p].existence = existence_memory_list[i][p]
                ingredient_button_list[i][p].existence = existence_memory_list[i][p]
            except:
                ingredient_list[i][p].existence = 0
                ingredient_button_list[i][p].existence = 0               
##text setting

#title text
title_text = font.render('냉장고를 부탁해!', True, WHITE)
titleRect = title_text.get_rect()
titleRect.center = (display_size[0] * 0.5 , display_size[1] * 0.3)
#choose what I have button text
my_ingredients_text = button_font.render('What do I have?', True, WHITE)
my_ingredients_Rect = my_ingredients_text.get_rect()
my_ingredients_Rect.center = (my_ingredients_button[0]+button_size[0]/2, my_ingredients_button[1]+button_size[1]/2)
#recommendation button text
recommendation_text = button_font.render('What can I make?', True, WHITE)
recommendationRect = recommendation_text.get_rect()
recommendationRect.center = (recommendation_button[0]+button_size[0]/2,recommendation_button[1]+button_size[1]/2)
#cooking time button text
cooking_time_text = button_font.render('Credits', True, WHITE)
cooking_time_Rect = cooking_time_text.get_rect()
cooking_time_Rect.center = (cooking_time_button[0]+button_size[0]/2, cooking_time_button[1]+button_size[1]/2)
#append button text
append_text = button_font.render('Customize!', True, WHITE)
appendRect = append_text.get_rect()
appendRect.center = (append_button[0]+button_size[0]/2,append_button[1]+button_size[1]/2)
#ingredient category text
ingredient_category_text_list= []
ingredient_category_Rect_list = []
for i in range(len(ingredient_category_list)):
    ingredient_category_text_list.append(ingredient_font.render(ingredient_category_list[i], True, WHITE))
    ingredient_category_Rect_list.append(ingredient_category_text_list[i].get_rect())
    if i >5:
        ingredient_category_Rect_list[i].center = ((display_size[0]/7)*(i-5), display_size[1]*0.75)
    else:
        ingredient_category_Rect_list[i].center = ((display_size[0])/7*(i+1), display_size[1]*0.25)

#menu function
x = 0
page_log = [0]

#initial values
game_over = False
category_name = 'input'
ingredient_name = 'input'
recipe_name = 'input'
recipe_ingredient_name = 'input'

#actual running code
while not game_over:

#cursor setting
    pygame.mouse.set_visible(False)
    cursor_image = pygame.image.load('cursor dot.png')
    cursor_image = pygame.transform.scale(cursor_image, (60, 40))
    cursorRect = cursor_image.get_rect()
    cursorRect.center = pygame.mouse.get_pos()

#quit button
    for event in pygame.event.get():
        if event.type == QUIT:
            game_over = True

    #fill display
        game_display.fill(YELLOW)

    #when x==0
        if x==0:
        #print dots
            for dot in dots:
                if dot.active:
                    dot.draw()
                if ((pygame.mouse.get_pos()[0]-dot.x)**2 + (pygame.mouse.get_pos()[1]-dot.y)**2)**0.5 < 30 and dot.active:
                    dot.active = False
                    newdot = Dot(game_display)
                    dots.append(newdot)
            
        #button drawing
            pygame.draw.rect(game_display, GREEN, [my_ingredients_button[0], my_ingredients_button[1], button_size[0], button_size[1]])
            pygame.draw.rect(game_display, GREEN, [recommendation_button[0], recommendation_button[1], button_size[0], button_size[1]])
            pygame.draw.rect(game_display, GREEN, [cooking_time_button[0], cooking_time_button[1], button_size[0], button_size[1]])
            pygame.draw.rect(game_display, GREEN, [append_button[0], append_button[1], button_size[0], button_size[1]])   

        #print words and images
            game_display.blit(title_text, titleRect)
            game_display.blit(recommendation_text, recommendationRect)
            game_display.blit(my_ingredients_text, my_ingredients_Rect)
            game_display.blit(cooking_time_text, cooking_time_Rect)
            game_display.blit(append_text, appendRect)
            game_display.blit(cursor_image, cursorRect)

        
        #detect menu movement
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if my_ingredients_button[0]<x<my_ingredients_button[0] + 300 and my_ingredients_button[1]<y<my_ingredients_button[1]+50:
                    x = 1
                    page_log.append(deepcopy(x))
                    continue           
                elif recommendation_button[0]<x<recommendation_button[0] + 300 and recommendation_button[1]<y<recommendation_button[1]+50:
                    x = 2
                    page_log.append(deepcopy(x))
                    continue
                elif cooking_time_button[0]<x<cooking_time_button[0] + 300 and cooking_time_button[1]<y<cooking_time_button[1]+50:
                    x = 3
                    page_log.append(deepcopy(x))
                    
                elif append_button[0]<x<append_button[0] + 300 and append_button[1]<y<append_button[1]+50:
                    x = 4
                    page_log.append(deepcopy(x))
                else:
                    x = 0

    #when x == 1(choose ingredients that I have)              
        elif x == 1:

            for i in range(len(ingredient_category_list)):
                pygame.draw.rect(game_display, GREEN, [ingredient_category_Rect_list[i].center[0]-category_button_size[0]/2, ingredient_category_Rect_list[i].center[1]-category_button_size[1]/2, category_button_size[0], category_button_size[1]])
                game_display.blit(ingredient_category_text_list[i], ingredient_category_Rect_list[i])
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                x,y = event.pos
                if ingredient_category_Rect_list[0].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[0].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[0].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[0].center[1]+category_button_size[1]/2:
                        x = category_x_list[0]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[1].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[1].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[1].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[1].center[1]+category_button_size[1]/2:
                        x = category_x_list[1]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[2].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[2].center[0]+category_button_size[1]/2 and ingredient_category_Rect_list[2].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[2].center[1]+category_button_size[1]/2:
                        x = category_x_list[2]
                        page_log.append(deepcopy(x))       
                elif ingredient_category_Rect_list[3].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[3].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[3].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[3].center[1]+category_button_size[1]/2:
                        x = category_x_list[3]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[4].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[4].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[4].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[4].center[1]+category_button_size[1]/2:
                        x = category_x_list[4]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[5].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[5].center[0]+category_button_size[1]/2 and ingredient_category_Rect_list[5].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[5].center[1]+category_button_size[1]/2:
                        x = category_x_list[5]
                        page_log.append(deepcopy(x))       
                elif ingredient_category_Rect_list[6].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[6].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[6].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[6].center[1]+category_button_size[1]/2:
                        x = category_x_list[6]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[7].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[7].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[7].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[7].center[1]+category_button_size[1]/2:
                        x = category_x_list[7]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[8].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[8].center[0]+category_button_size[1]/2 and ingredient_category_Rect_list[8].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[8].center[1]+category_button_size[1]/2:
                        x = category_x_list[8]
                        page_log.append(deepcopy(x))       
                elif ingredient_category_Rect_list[9].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[9].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[9].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[9].center[1]+category_button_size[1]/2:
                        x = category_x_list[9]
                        page_log.append(deepcopy(x))
                elif ingredient_category_Rect_list[10].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[10].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[10].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[10].center[1]+category_button_size[1]/2:
                        x = category_x_list[10]
                        page_log.append(deepcopy(x)) 
                elif ingredient_category_Rect_list[11].center[0]-category_button_size[0]/2<x<ingredient_category_Rect_list[11].center[0]+category_button_size[0]/2 and ingredient_category_Rect_list[11].center[1]-category_button_size[1]/2<y<ingredient_category_Rect_list[11].center[1]+category_button_size[1]/2:
                        x = category_x_list[11]
                        page_log.append(deepcopy(x))                                                                       
                else:
                    x=1
            else:
                pass
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_BACKSPACE:
                    x = 0
                    page_log.append(deepcopy(x))               
            game_display.blit(cursor_image, cursorRect)
                
    #when 1.01 <= x <= 1.11(specific ingredients)    
        elif 1 < x <= 1.12:
            for p in range(len(category_x_list)):
                if category_x_list[p] == x:
                    for i in range(len(ingredient_list[p])):
                        ingredient_button_list[p][i].draw()
                        ingredient_button_list[p][i].click()
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_BACKSPACE:
                    x = 1
                    page_log.append(deepcopy(x))
        #image print         
            game_display.blit(cursor_image, cursorRect)

    #when x == 2(menu recommendation)
        elif x == 2:
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_BACKSPACE:
                    x = 1
                    page_log.append(deepcopy(x))
            what_I_have = []
            for i in range(len(ingredient_list)):
                for p in range(len(ingredient_list[i])):
                    if ingredient_button_list[i][p].existence == 1:
                        what_I_have.append(ingredient_list[i][p])
            similarity_list = []
            for item in recipe_list:
                similarity = 0
                for itemm in item.ingredients:
                    for i in range(len(what_I_have)):
                        if itemm == what_I_have[i].name:
                            similarity += 1
                    similarity = similarity / len(item.ingredients)
                item.similarity = similarity
                similarity_list.append(similarity)
            similarity_list_deepcopy = deepcopy(similarity_list)
            similarity_list.sort(reverse= True)
            similarity_index = similarity_list[4]
            similarity_text_list = []
            similarity_ingredient_text_list = []
            similarity_rect_list = []
            similarity_ingredient_rect_list = []
            for item in recipe_list:
                if item.similarity >= similarity_index and item.similarity != 0:
                    c = item.name
                    d = str(item.ingredients)
                    similarity_text_list.append(recipe_ingredient_font.render(d, True, WHITE))
                    similarity_ingredient_text_list.append(recipe_font.render(c,True, BLACK))
                    similarity_rect_list.append(similarity_text_list[-1].get_rect())
                    similarity_ingredient_rect_list.append(similarity_ingredient_text_list[-1].get_rect())
            if len(similarity_text_list) > 5:
                similarity_text_list = similarity_text_list[:5]
                similarity_rect_list = similarity_rect_list[:5]
                for i in range(5):
                    similarity_rect_list[i].center = (display_size[0]//2,display_size[1]//(len(similarity_rect_list)+2)*(i+2))
                    similarity_ingredient_rect_list[i].center = (display_size[0]//2,display_size[1]//(2*(len(similarity_rect_list)+2))*(2*i+3))
            else:
                for i in range(len(similarity_rect_list)):
                    similarity_rect_list[i].center = (display_size[0]//2,display_size[1]//(len(similarity_rect_list)+2)*(i+2))
                    similarity_ingredient_rect_list[i].center = (display_size[0]//2,display_size[1]//(2*(len(similarity_rect_list)+2))*(2*i+3))

            if len(similarity_text_list) == 0:
                recipe_title_text = recipe_title_font.render('I have nothing to recommend :(', True, GREEN)
                recipe_title_Rect = recipe_title_text.get_rect()            
                recipe_title_Rect.center = (display_size[0]//2,display_size[1]//2)
            else:
                recipe_title_text = recipe_title_font.render('You can make these!', True, GREEN)
                recipe_title_Rect = recipe_title_text.get_rect()            
                recipe_title_Rect.center = (display_size[0]//2,display_size[1]//(len(similarity_rect_list)+2)*1)
            for i in range(len(similarity_text_list)):
                game_display.blit(similarity_text_list[i],similarity_rect_list[i])
                game_display.blit(similarity_ingredient_text_list[i],similarity_ingredient_rect_list[i])
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_BACKSPACE:
                    x = 0
                    page_log.append(deepcopy(x))
            game_display.blit(recipe_title_text, recipe_title_Rect)
            game_display.blit(cursor_image, cursorRect)

    #when x == 3(cooking order recommendation)
        elif x == 3:
            credit_text = recipe_title_font.render('made by Diane, thanks!', True, WHITE)
            credit_Rect = credit_text.get_rect()
            credit_Rect.center = (display_size[0]//2, display_size[1]//2)
            game_display.blit(credit_text, credit_Rect)
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_BACKSPACE:
                    x = 0
                    page_log.append(deepcopy(x))        

    #when x == 4(append new menu, ingredient)
        elif x == 4:
            append_recipe_button = VS_Button('Append recipe', (display_size[0]//2,display_size[1]//4), 4.2)
            append_ingredient_button = VS_Button('Append ingredient', (display_size[0]//2, (display_size[1]//4)*3), 4.3)
            append_recipe_button.draw()
            append_ingredient_button.draw()
            append_recipe_button.click()
            append_ingredient_button.click()
            x=page_log[-1]
            if event.type == pygame.constants.KEYDOWN:
                if event.key == pygame.constants.K_BACKSPACE:
                    x = 0
                    page_log.append(deepcopy(x))          
            game_display.blit(cursor_image, cursorRect)        

    #when x == 4.2, 4.3(large input)
        elif x == 4.2:
            append_ingredient_title_text = recipe_title_font.render('Type the recipe name', True, GREEN)
            append_ingredient_title_rect = append_ingredient_title_text.get_rect()
            append_ingredient_title_rect.center = (display_size[0]//2, display_size[1]//4)
            game_display.blit(append_ingredient_title_text,append_ingredient_title_rect)
            pygame.draw.rect(game_display, WHITE, [display_size[0]//2-200,display_size[1]//4 * 2-25,400,50])

            input_text = recipe_ingredient_font.render(recipe_name, True, BLACK)
            input_rect = input_text.get_rect()
            input_rect.center = (display_size[0]//2,display_size[1]//4 * 2)
            game_display.blit(input_text, input_rect)
            state = pygame.key.get_pressed()
            game_display.blit(cursor_image, cursorRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    recipe_name = recipe_name[:-1]
                elif event.key == pygame.K_BACKSPACE:
                    x = 4.
                    page_log.append(deepcopy(x))       
                elif event.key == pygame.K_RETURN:
                    x = 4.21
                    page_log.append(deepcopy(x))                                 
                else:
                    recipe_name += event.unicode  

        elif x == 4.3:
            append_ingredient_title_text = recipe_title_font.render('Type the ingredient category(one of twelve)', True, GREEN)
            append_ingredient_title_rect = append_ingredient_title_text.get_rect()
            append_ingredient_title_rect.center = (display_size[0]//2, display_size[1]//4)
            game_display.blit(append_ingredient_title_text,append_ingredient_title_rect)
            pygame.draw.rect(game_display, WHITE, [display_size[0]//2-200,display_size[1]//4 * 2-25,400,50])

            input_text = recipe_ingredient_font.render(category_name, True, BLACK)
            input_rect = input_text.get_rect()
            input_rect.center = (display_size[0]//2,display_size[1]//4 * 2)
            game_display.blit(input_text, input_rect)
            state = pygame.key.get_pressed()
            game_display.blit(cursor_image, cursorRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    category_name = category_name[:-1]
                elif event.key == pygame.K_BACKSPACE:
                    x = 4
                    page_log.append(deepcopy(x))
                elif event.key == pygame.K_RETURN:
                    x = 4.31
                    page_log.append(deepcopy(x))                    
                else:
                    category_name += event.unicode   
    
    #when x == 4.21, 4.31(small input)
        elif x == 4.21:
            append_ingredient_title_text = recipe_title_font.render('Type ingredient list', True, GREEN)
            append_ingredient_title_rect = append_ingredient_title_text.get_rect()
            append_ingredient_title_rect.center = (display_size[0]//2, display_size[1]//4)
            game_display.blit(append_ingredient_title_text,append_ingredient_title_rect)
            pygame.draw.rect(game_display, WHITE, [display_size[0]//2-200,display_size[1]//4 * 2-25,400,50])

            input_text = recipe_ingredient_font.render(recipe_ingredient_name, True, BLACK)
            input_rect = input_text.get_rect()
            input_rect.center = (display_size[0]//2,display_size[1]//4 * 2)
            game_display.blit(input_text, input_rect)
            state = pygame.key.get_pressed()
            game_display.blit(cursor_image, cursorRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    recipe_ingredient_name = recipe_ingredient_name[:-1]

                elif event.key == pygame.K_BACKSPACE:
                    x = 4.3
                    page_log.append(deepcopy(x))

                elif event.key == pygame.K_RETURN:
                    middle_line = ''
                    with open('recipe.txt', 'a+') as renewal:
                        middle_line += recipe_name
                        middle_line += ','
                        middle_line += recipe_ingredient_name
                        middle_line += '\n'
                        renewal.write(middle_line)
                    with open('recipe.txt', 'r+') as recipe:
                        recipe_list = []
                        for line in recipe:
                            if '\n' in line:
                                memory_line = line[:-1].split(',')
                            else:
                                memory_line = line.split(',')
                            recipe_list.append(Food(memory_line[0],memory_line[1:]))   
                    x = 4
                    page_log.append(deepcopy(x))                    
                else:
                    recipe_ingredient_name += event.unicode

        elif x == 4.31:
            append_ingredient_title_text = recipe_title_font.render('Type ingredient name', True, GREEN)
            append_ingredient_title_rect = append_ingredient_title_text.get_rect()
            append_ingredient_title_rect.center = (display_size[0]//2, display_size[1]//4)
            game_display.blit(append_ingredient_title_text,append_ingredient_title_rect)
            pygame.draw.rect(game_display, WHITE, [display_size[0]//2-200,display_size[1]//4 * 2-25,400,50])

            input_text = recipe_ingredient_font.render(ingredient_name, True, BLACK)
            input_rect = input_text.get_rect()
            input_rect.center = (display_size[0]//2,display_size[1]//4 * 2)
            game_display.blit(input_text, input_rect)
            state = pygame.key.get_pressed()
            game_display.blit(cursor_image, cursorRect)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DELETE:
                    ingredient_name = ingredient_name[:-1]

                elif event.key == pygame.K_BACKSPACE:
                    x = 4.3
                    page_log.append(deepcopy(x))

                elif event.key == pygame.K_RETURN:
                    with open('ingredient.txt', 'r+') as renewal:
                        lines = renewal.readlines()
                        for i in range(len(lines)):
                            if category_name in lines[i]:
                                lines[i] = lines[i][:-1]
                                lines[i] += ','
                                lines[i] += ingredient_name
                                lines[i] += '\n'
                        renewal.seek(0)
                        renewal.truncate(0)
                        for i in range(len(lines)):
                            renewal.write(str(lines[i]))
                    x = 4
                    page_log.append(deepcopy(x))                    
                else:
                    ingredient_name += event.unicode             
                                

#frame rate
    pygame.event.pump()
    pygame.display.update()
    time.sleep(0.02)
    pygame.time.Clock().tick(20)
