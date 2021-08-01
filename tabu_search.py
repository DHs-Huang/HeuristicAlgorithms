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
data = pd.read_csv("data/Latitude and Longitude of Taiwan County.csv")
coordinate = data.iloc[:,1:].values   
problem = TSPProblem(coordinate,data["縣市"].values)  

tabu_size = 5
#tabu_state = np.zeros(shape=(problem.city_count,problem.city_count)) #剩餘秒數
Move = namedtuple('Tabu', ['i1', 'v1','i2','v2'])
tabu_list = [] #[(i1,v1,i2)]

#get_neighbourhood
candidate_swapped_index = list(combinations(list(range(problem.city_count)), 2))
candiate_count = len(candidate_swapped_index)

#init
current_sol = [i for i in range(problem.city_count)]
the_best_sol = current_sol[:]
the_best_val = problem.compute_objective_value(current_sol)

neighbor_best_val = sys.maxsize
neighbor_best_sol = None
neighbor_best_move = None

non_tabu_neighbor_best_val = sys.maxsize
non_tabu_neighbor_best_sol = None

for swapped_index in candidate_swapped_index:
    #compute candidate objective value
    c1,c2 = swapped_index 
    neighbor_sol =  current_sol[:]
    neighbor_sol[c1],neighbor_sol[c2] = neighbor_sol[c2],neighbor_sol[c1]
    neighbor_value = problem.compute_objective_value(neighbor_sol)
    
    #check if it is in tabu
    violated = False
    for tabu_move in tabu_list:
        if (tabu_move.i1 == c1 and tabu_move.v1 == neighbor_sol[c1] and \
            tabu_move.i2 == c2 and tabu_move.v2 == neighbor_sol[c2]):
            violated = True
            break   
    
    if neighbor_value<neighbor_best_val:
        neighbor_best_val = neighbor_value
        neighbor_best_sol = neighbor_sol
        neighbor_best_move = swapped_index
        
    if violated and neighbor_value<non_tabu_neighbor_best_val:
        non_tabu_neighbor_best_val = neighbor_value
        non_tabu_neighbor_best_sol = neighbor_sol
        non_tabu_neighbor_best_move = swapped_index
    
#better than aspiration level
if(neighbor_best_val<the_best_val):
    the_best_val = neighbor_best_val
    the_best_sol = neighbor_sol
    
    v1 = current_sol[neighbor_best_move[0]]
    v2 = current_sol[neighbor_best_move[1]]
    
    move = Move(i1=neighbor_best_move[0],v1=v1,
                i2=neighbor_best_move[1],v2=v2)
    
    if move not in tabu_list:
        tabu_list.inset(0,move)
    elif(move in tabu_list[1:]):
        tabu_list.remove(move)
        tabu_list.inset(0,move)
        
else :
     move = Move(i1=non_tabu_neighbor_best_move[0],v1=v1,
                i2=non_tabu_neighbor_best_move[1],v2=v2)
     tabu_list.append(0,move)   

#%%   
#https://blog.csdn.net/zuochao_2013/article/details/72292466
#https://blog.csdn.net/qq_38048756/article/details/109394815
#file:///E:/Download/A%20Tabu-search%20Based%20Bayesian%20Network%20Structure%20Learning%20Algorithm.pdf