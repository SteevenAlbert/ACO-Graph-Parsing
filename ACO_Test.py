from tracemalloc import start
import numpy as np

from AntColony import AntColony

distances = np.array([[0, 2, 1, 5, 7],
                      [2, 0, 4, 8, 2],
                      [2, 4, 0, 1, 3],
                      [5, 8, 1, 0, 2],
                      [7, 2, 3, 2, 0]])

def find_start_ants(distances):
    row_mean = np.divide(distances.sum(axis=1), distances.shape[0])
    start_ants_coord = np.where(distances >= row_mean)
    # listOfCoordinates= list(zip(start_ants_coord[0], start_ants_coord[1]))
    # for cord in listOfCoordinates:
    #     print(cord)
    return start_ants_coord

# def parse_ants(distances, start_ants):

#     if (not start_ants):
#         return 0
#     else:
#         start_ants.remove[0][0]
#         start_ants.remove[1][0]
#         return parse_ants

def parse_ants(distances, start_ants):
    print(start_ants[0][5])


coords = find_start_ants(distances)
parse_ants(distances, coords)


