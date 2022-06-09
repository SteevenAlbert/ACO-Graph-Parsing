from tracemalloc import start
import numpy as np
import pandas as pd

from AntColony import AntColony

distances = np.array([[0, 2, 1, 5, 7],
                      [2, 0, 4, 8, 2],
                      [2, 4, 0, 1, 3],
                      [5, 8, 1, 0, 2],
                      [7, 2, 3, 2, 0]])

# distances = np.array([[0, 0.8, 0.2, 0.1, 0.5],
#                       [0.2, 0, 0.3, 0.7, 0.2],
#                       [0.5, 0.3, 0, 0.5, 0.4],
#                       [0.6, 0.2, 0.6, 0, 0.3],
#                       [0.5, 0.1, 0.4, 0.3, 0]])

# distances = pd.read_csv("graphs\CryptoWall.csv_2_Win32_Filecoder.CryptoWall.G trojan.csv")


phermones = np.ones(distances.shape)
# row = [1, 2, 3, 4]
# sorted = np.sort(row)[::-1]
# print(np.where(row == sorted[0])[0][0])


def find_start_ants(distances):
    start_ants = []
    row_mean = distances.mean(axis=1)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            if distances[i][j] >= row_mean[i]:
                start_ants.append([i, j])
    # for row in distances:
    #     row_mean = row.mean()
    #     for ele in row:
    #         start_ants = np.where(ele >= row_mean)
    return start_ants


row_mean = distances.mean(axis=1)
# print(row_mean[1])


def spread_phermone(path):
    for i in range(len(path)):
        if distances[path[i][0]][path[i][1]] != 0:
            phermones[path[i][0]][path[i][1]] *= 1 / \
                distances[path[i][0]][path[i][1]]


def promising(start, end, path):
    sum = 0
    for i in range(len(path)):
        sum += distances[path[i][0]][path[i][1]]
    lr = sum/len(path)

    new_sum = sum + distances[start][end]
    new_lr = new_sum/(len(path)+1)

    if not any(end in sublist for sublist in path) and new_lr >= lr:
        return True
    return False


def all_paths(distances, start_ants):
    paths = []
    for i in range(len(start_ants)):
        path = [[-1, -1]]
        ant_path(distances, start_ants[i], path)
        paths.append(path)
    for j in range(len(paths)):
        spread_phermone(paths[j])
    return paths


def ant_path(distances, start_ant, path):
    val = False
    if len(path) == distances.shape[0]:
        return

    # mean = row_mean[start_ant[1]]
    row = distances[start_ant[1]]
    sorted = np.sort(row)[::-1]

    # for i in range(len(sorted)):
    #     if sorted[i] >= mean and not any(np.where(row == sorted[i])[0][0] in sublist for sublist in path):
    #         path.append([start_ant, np.where(row == sorted[i])[0][0]])
    #         ant_path(distances, np.where(row == sorted[i])[0][0], path)
    #         break
    path.append(start_ant)
    for i in range(len(sorted)):
        if promising(start_ant[1], np.where(row == sorted[i])[0][0], path):
            # path.append([start_ant[1], np.where(row == sorted[i])[0][0]])
            ant_path(distances, [start_ant[1], np.where(
                row == sorted[i])[0][0]], path)
            break
            # if sorted[i] >= mean:  # no error
            #     for path1 in path:
            #         if sorted[i] == path1[1]:
            #             val = True
            #     if val:
            #         path.append([start_ant, sorted[i]])
            #         ant_path(distances, sorted[i], path)
            #         break
# ants = find_start_ants(distances)
# ant_path(distances, ants, path)


def run(iterations, phermones):
    for i in range(iterations):
        ants = find_start_ants(distances)
        print(all_paths(distances, ants))  # [-1,-1]??
        phermones *= 0.95


run(3, phermones)
# print(phermones)


# PROMISING/LEARNING RATE
# promising(start_ant, np.where(row == sorted[i])[0][0], path)


# start_ants = find_start_ants(distances)
# path = [[-1, -1]]
# ant_path(distances, 0, path)
# print(path)
