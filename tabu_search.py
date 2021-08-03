# -*- coding: utf-8 -*-
"""
Created on Sat Jul 24 15:56:22 2021

@author: Jerry
"""
import numpy as np
import pandas as pd
from itertools import combinations
from collections import namedtuple
import sys
#%%
class TSPProblem:
    def __init__(self,coordinate,cities_name):
        self.coordinate = coordinate
        self.cities_name = cities_name
        self.city_count = len(self.cities_name)
        
    def get_distance(self,arr1,arr2):
        #Euclidean distance
        return np.sqrt(np.power(arr1-arr2,2).sum())
    
    def compute_objective_value(self,cities_id):
        total_distance = 0
        for i in range(len(cities_id)):
            city1 = cities_id[i]
            city2 = cities_id[i+1] if i<len(cities_id)-1 else cities_id[0]
            total_distance += self.get_distance(self.coordinate[city1],self.coordinate[city2])
        return total_distance
    
    def to_cities_name(self,cities_id):
        return [self.cities_name[i] for i in cities_id]
#%%
 #%%
Move = namedtuple('Tabu', ['i1', 'v1','i2','v2'])

class TabuSearch:
    def  __init__(self,
                  var_num,
                  fitness_func,
                  tabu_size,
                  iteration_num = 50,
                  after_generation = None,
                  save_best_sols=False):
        
        self.var_num = var_num
        self.iteration_num = iteration_num
        self.tabu_list = [] #[(i1,v1,i2)]
        self.tabu_size = tabu_size
        self.fitness_func  =  fitness_func
        self.after_generation = after_generation
        self.reset()
        
        
    def reset(self):
        self.candidate_swapped_index = list(combinations(list(range(self.var_num)), 2))
        self.candiate_count = len(self.candidate_swapped_index)
        
        self.iteration = 0
        self.current_sol = [i for i in range(self.var_num)]
        self.the_best_sol = self.current_sol[:]
        self.the_best_val = self.fitness_func(self.current_sol)
 
    def swap_move(self,sol,move):
        sol[move.i1],sol[move.i2] = sol[move.i2],sol[move.i1]
        return
    
    def run(self):
        for iteration in range(self.iteration_num):
            self.run_one_iteration()
            if(self.after_generation):
                self.after_generation(self)

    def run_one_iteration(self):
        self.iteration += 1

        neighbor_best_val = sys.maxsize
        neighbor_best_sol = None
        neighbor_best_move = None
        
        non_tabu_neighbor_best_val = sys.maxsize
        non_tabu_neighbor_best_move = None
        
        for swapped_index in self.candidate_swapped_index:
            c1,c2 = swapped_index
            move = Move(c1,self.current_sol[c1],c2,self.current_sol[c2])
            
            neighbor_sol =  self.current_sol[:]
            self.swap_move(neighbor_sol, move)
            neighbor_value = self.fitness_func(neighbor_sol)
            
            #check if it is in tabu
            violated = False
            for tabu_move in self.tabu_list:
                if (tabu_move.i1 == c1 and tabu_move.v1 == neighbor_sol[c1] and \
                    tabu_move.i2 == c2 and tabu_move.v2 == neighbor_sol[c2]):
                    violated = True
                    break   
            
            if neighbor_value<neighbor_best_val:
                neighbor_best_val = neighbor_value
                neighbor_best_sol = neighbor_sol[:]
                neighbor_best_move = move
                
            if not violated and neighbor_value<non_tabu_neighbor_best_val:
                non_tabu_neighbor_best_val = neighbor_value
                non_tabu_neighbor_best_move = move
        
        #udpate
        #better than aspiration level
        if(neighbor_best_val<self.the_best_val):
            self.the_best_val = neighbor_best_val
            self.the_best_sol = neighbor_best_sol
            
            #udpate move
            self.swap_move(self.current_sol, neighbor_best_move)
            
            if move not in self.tabu_list:
                self.tabu_list.insert(0,neighbor_best_move)
            elif(move in self.tabu_list[1:]):
                self.tabu_list.remove(move)
                self.tabu_list.insert(0,neighbor_best_move)
                
        else :
             #udpate move
             self.swap_move(self.current_sol, non_tabu_neighbor_best_move)
             self.tabu_list.append(non_tabu_neighbor_best_move)
        
        if len(self.tabu_list) > self.tabu_size:
            self.tabu_list = self.tabu_list[:-1]  
#%%
data = pd.read_csv("data/Latitude and Longitude of Taiwan County.csv")
coordinate = data.iloc[:,1:].values   
problem = TSPProblem(coordinate,data["縣市"].values)  

def output_message(tabu_search):
    print(f"=====Itieration {tabu_search.iteration}=====")
    print(f"Best Solution = {tabu_search.the_best_sol}")
    print(f"Best Fitness = {tabu_search.the_best_val}")


tabu = TabuSearch(var_num=problem.city_count,
                  fitness_func=problem.compute_objective_value,
                  tabu_size=5,
                  iteration_num = 5,
                  after_generation=output_message)
tabu.run()


tabu.tabu_list
#%%  
#https://blog.csdn.net/zuochao_2013/article/details/72292466
#https://blog.csdn.net/qq_38048756/article/details/109394815
#file:///E:/Download/A%20Tabu-search%20Based%20Bayesian%20Network%20Structure%20Learning%20Algorithm.pdf