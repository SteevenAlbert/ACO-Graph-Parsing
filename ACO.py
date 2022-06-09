from AntColony import AntColony
from tracemalloc import start
import numpy as np
import pandas as pd
import decimal
np.set_printoptions(suppress=True)

# distances = np.array([[0, 2, 1, 5, 7],
#                        [2, 0, 4, 8, 2],
#                        [2, 4, 0, 1, 3],
#                        [5, 8, 1, 0, 2],
#                        [7, 2, 3, 2, 0]])

# distances = np.array([[0, 0.8, 0.2, 0.1, 0.5],
#                       [0.2, 0, 0.3, 0.7, 0.2],
#                       [0.5, 0.3, 0, 0.5, 0.4],
#                       [0.6, 0.2, 0.6, 0, 0.3],
#                       [0.5, 0.1, 0.4, 0.3, 0]])

distances = pd.read_csv(
    "graphs/CryptoWall.csv_2_Win32_Filecoder.CryptoWall.D trojan.csv")
distances.drop(distances.columns[0], axis=1, inplace=True)
distances = np.array(distances.to_numpy())
phermones = np.ones(distances.shape)


def find_start_ants(distances):
    start_ants = []
    row_mean = distances.mean(axis=1)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            if distances[i][j] >= row_mean[i]:
                start_ants.append([i, j])
    return start_ants


row_mean = distances.mean(axis=1)


def spread_phermone(path):
    for i in range(len(path)):
        phermones[path[i][0]][path[i][1]] *= distances[path[i][0]][path[i][1]]


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
        path = []
        ant_path(distances, start_ants[i], path)
        paths.append(path)
    for j in range(len(paths)):
        spread_phermone(paths[j])
    return paths


def ant_path(distances, start_ant, path):
    if len(path) == distances.shape[0]:
        return

    row = distances[start_ant[1]]*phermones[start_ant[1]]
    sorted = np.sort(row)[::-1]

    path.append(start_ant)
    for i in range(len(sorted)):
        if promising(start_ant[1], np.where(row == sorted[i])[0][0], path):

            ant_path(distances, [start_ant[1], np.where(
                row == sorted[i])[0][0]], path)
            break


def run(iterations, phermones):
    for i in range(iterations):
        ants = find_start_ants(distances)
        all_paths(distances, ants)
        phermones *= 0.95


run(2, phermones)
# print(phermones)


def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))


scaledPhermones = NormalizeData(phermones)
df = pd.DataFrame(phermones)
df.to_csv("Phermones.csv")

df = pd.DataFrame(scaledPhermones)
df.to_csv("ScaledPhermones.csv")
# print(scaledPhermones)
