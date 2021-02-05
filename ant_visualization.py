# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 15:45:02 2021

@author: Jerry
"""


import sys, pygame
import numpy as np
import random
#%%
class Color:
    BLUE = (0,0,255)
    RED = (255,0,0) 
    WHITE = (255,255,255)
    BLACK = (0,0,0) 
    YELLOW = (255,255,0) 
    SLATE_GREY = (112,128,144)

class Block:
    
    def __init__(self,position,size,color):
        #(left,top)
        self.position = position
        #(width,height)
        self.size = size
        self.color = color
              
class Food(Block): 
    
    all_food = []
    @staticmethod
    def add_food(food):
        Food.all_food.append(food)
    
    def remove_all_food():
        Food.all_food = []
        
    def __init__(self,position,size,color):
        super().__init__(position,size,color)
        Food.add_food(self)

class Button(Block):
    
    def __init__(self,position,size,color,image,callback):
        super().__init__(position,size,color)
        self.image = pygame.transform.scale(image,size)
        self.rect = image.get_rect(topleft=position)
        self.callback = callback
        
    def on_click(self, event):
        if event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.callback()

class Ant(Block):
    all_ant = []
    @staticmethod
    def add_ant(ant):
        Ant.all_ant.append(ant)
        
    def __init__(self,position,size,color,image,callback):
        super().__init__(position,size,color)
        Ant.add_ant(self)
#%%       
FOOD_WIDTH = 50
FOOD_HEIGHT = 50

NEST_WIDTH = 50
NEST_HEIGHT = 50

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

MAP_WIDTH = 800
MAP_HEIGHT = 600

screen = None

maps = []
for w in range(int(MAP_WIDTH/FOOD_WIDTH)):
    for h in range(int(MAP_HEIGHT/FOOD_HEIGHT)):
        maps.append((w*FOOD_WIDTH,h*FOOD_HEIGHT))
        
def random_generate_map():
    remove_all_food_on_map()
    
    posible_positions = random.sample(maps,6)
    
    #nest
    nest = Block(posible_positions.pop(),(NEST_WIDTH,NEST_HEIGHT),Color.SLATE_GREY)
    pygame.draw.rect(screen,nest.color,(nest.position[0],nest.position[1],nest.size[0],nest.size[1]))

    for pos in posible_positions:
        food = Food(pos,(FOOD_WIDTH,FOOD_HEIGHT),Color.BLUE)
        pygame.draw.rect(screen,food.color,(food.position[0],food.position[1],food.size[0],food.size[1]))
        
def remove_all_food_on_map():
    for food in Food.all_food:
        pygame.draw.rect(screen,Color.WHITE.value,(food.position[0],food.position[1],food.size[0],food.size[1]))
    Food.remove_all_food()  
 
def start():
    pass
                  
def main():  
    global screen
    
    #resoucrse
    random_map_img = pygame.image.load('image/random_map.png')
    start_img = pygame.image.load("image/start.png")
     
    posible_positions = random.sample(maps,6)

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    # Fill the background with white
    screen.fill(Color.WHITE)
    
    #nest
    nest = Block(posible_positions.pop(),(NEST_WIDTH,NEST_HEIGHT),Color.SLATE_GREY)
    pygame.draw.rect(screen,nest.color,(nest.position[0],nest.position[1],nest.size[0],nest.size[1]))
    
    #food
    for pos in posible_positions:
        food = Food(pos,(FOOD_WIDTH,FOOD_HEIGHT),Color.BLUE)
        pygame.draw.rect(screen,food.color,(food.position[0],food.position[1],food.size[0],food.size[1]))
    
    #draw line
    pygame.draw.line(screen, Color.SLATE_GREY, (0,MAP_HEIGHT), (SCREEN_WIDTH, MAP_HEIGHT))
    pygame.display.flip()
    
    #button
    random_map = Button((0,MAP_HEIGHT),(80,50),Color.YELLOW,random_map_img,random_generate_map)
    screen.blit(random_map.image, random_map.rect)  
    
    start_img = Button((0+random_map.size[0],MAP_HEIGHT),(80,50),Color.YELLOW,start_img,start)
    screen.blit(start_img.image, start_img.rect)  
    
    # Run until the user asks to quit
    running = True
    
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
              #checks if a mouse is clicked 
            if event.type == pygame.MOUSEBUTTONDOWN: 
                random_map.on_click(event)
           
        #screen.blit(random_map.image, random_map.rect)   
        # Flip the display
        pygame.display.update()
        
    # Done! Time to quit.
    pygame.quit()

if __name__ == "__main__":
    main()
    
       
    