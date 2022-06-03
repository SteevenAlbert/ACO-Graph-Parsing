from tracemalloc import start
import numpy as np

from AntColony import AntColony

distances = np.array([[0, 2, 1, 5, 7],
                      [2, 0, 4, 8, 2],
                      [2, 4, 0, 1, 3],
                      [5, 8, 1, 0, 2],
                      [7, 2, 3, 2, 0]])

# np.array([[0, 0.8, 0.2, 0.1, 0.5],
#                       [0.2, 0, 0.3, 0.7, 0.2],
#                       [0.5, 0.3, 0, 0.5, 0.4],
#                       [0.6, 0.2, 0.6, 0, 0.3],
#                       [0.5, 0.1, 0.4, 0.3, 0]])
phermones =  np.ones(distances.shape)

def find_start_ants(distances):
    row_sum = distances.sum(axis=1)
    sum_mean = np.mean(row_sum)
    start_ants = np.where(row_sum >= sum_mean)
    
    return start_ants

row_mean = distances.mean(axis=1)

def all_paths(distances, start_ants):
    for i in range(start_ants):
        arr = []
        path = ant_path(distances, start_ants[i], arr)


def ant_path(distances, start_ant, path):

    if len(path) == distances.shape[0]:
        return

    mean = row_mean[start_ant]
    row = distances[start_ant]
    sorted = np.sort(distances[start_ant])[::-1]

    for i in range(len(sorted)):
        if sorted[i] >= mean and not any(np.where(row == sorted[i])[0][0] in sublist for sublist in path):
            path.append([start_ant, np.where(row == sorted[i])[0][0]])
            ant_path(distances, np.where(row == sorted[i])[0][0], path)
            break

# PROMISING/LEARNING RATE
# promising(start_ant, np.where(row == sorted[i])[0][0], path)
# def promising(start, end, path):
#     sum = 0
#     for i in range(len(path)):
#         sum += distances[path[i][0]][path[i][1]]
#     lr = sum/len(path)

#     new_sum = sum + distances[start][end]
#     new_lr = new_sum/(len(path)+1)

#     if not any(end in sublist for sublist in path) and new_lr >= lr:
#         return True
#     return False
    

# start_ants = find_start_ants(distances)
path = [[-1,-1]]
ant_path(distances, 0, path)
print(path)


