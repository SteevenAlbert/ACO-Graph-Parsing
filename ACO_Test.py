from tracemalloc import start
import numpy as np

from AntColony import AntColony

distances = np.array([[0, 2, 1, 5, 7],
                      [2, 0, 4, 8, 2],
                      [2, 4, 0, 1, 3],
                      [5, 8, 1, 0, 2],
                      [7, 2, 3, 2, 0]])
                      
phermones =  np.ones(distances.shape)

def find_start_ants(distances):
    row_sum = distances.sum(axis=1)
    sum_mean = np.mean(row_sum)
    start_ants = np.where(row_sum >= sum_mean)
    
    return start_ants
  
def ant_tour(distances):
    path = []
    row_mean = distances.mean(axis=1)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            if(distances[i][j]>=row_mean[i]):
                path.append([i,j])



start_ants = find_start_ants(distances)
ant_tour(distances, start_ants)


