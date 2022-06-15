# ---------------------------------------------------
#   Created by:
#   Laila Elhattab
#   Steven Albert
#   Rana Raafat
#   Judy Wagdy
#
#   Supervised by:
#   Dr. Eslam Amer
# ---------------------------------------------------

import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)


# ----------------------------------------------INITIALIZATION------------------------------------------
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

graph_name = "CryptoWall.csv_2_Win32_Filecoder.CryptoWall.D trojan.csv"
distances = pd.read_csv("graphs/"+graph_name, header=None)
distances = np.array(distances.to_numpy())
phermones = np.zeros(distances.shape)
participation = np.zeros(distances.shape)


# ------------------------------------------------FUNCTIONS-----------------------------------------------
# Finding the start ants
def find_start_ants(distances):
    start_ants = []
    # Get the mean of each row
    row_mean = distances.mean(axis=1)
    for i in range(distances.shape[0]):
        for j in range(distances.shape[1]):
            # Append the edges where the weight is at least equal to the row mean
            if distances[i][j] >= row_mean[i]:
                start_ants.append([i, j])
                participation[i][j] = distances[i][j]
    return start_ants


row_mean = distances.mean(axis=1)

# Spread the phermones depending on the weight of the edge
def spread_phermone(path):
    lr = calculateLR(path)
    for i in range(len(path)):       
        phermones[path[i][0]][path[i][1]] += participation[path[i][0]][path[i][1]] / lr
        file.write(str(round(phermones[path[i][0]][path[i][1]],4))+ " ")
    file.write("\n \n")


def calculateLR(path):
    sum = 0
    for i in range(len(path)):
        sum += distances[path[i][0]][path[i][1]]
    lr = sum/len(path)
    return lr 


# Check whether this edge should be visited
def promising(start, end, path):
    lr = calculateLR(path)

    new_path = path.copy()
    new_path.append([start, end])
    new_lr = calculateLR(new_path)

    # Check whether the end node has already been visited
    if not any(end in sublist for sublist in path) and new_lr >= lr:  
        if new_lr == lr:
            participation[start][end] = participation[path[-1][0]][path[-1][1]]
        else:
            participation[start][end] = new_lr - lr
        return True
    return False


# Generate all paths in a single iteration
def all_paths(distances, start_ants):
    paths = []
    for i in range(len(start_ants)):
        path = []
        ant_path(distances, start_ants[i], path)
        paths.append(path)
        file.write("Path "+str(path)+"\n")
        file.write("Phermones ")
        spread_phermone(path)
    return paths


# Generate the path of a single ant
def ant_path(distances, start_ant, path):
    if len(path) == distances.shape[0]:
        return


    row = distances[start_ant[1]] * phermones[start_ant[1]]

    sorted_row = sorted(enumerate(row), key=lambda x: x[1], reverse=True)

    path.append(start_ant)

    for i in [sub[0] for sub in sorted_row ]:
        if promising(start_ant[1], i, path):  
            ant_path(distances, [start_ant[1], i], path)
            break


# The main function
def run(phermones):
    ants = find_start_ants(distances)

    for i in range(len(ants)):
        file.write("\n-----------------------------Iteration "+ str(i)+ ":-----------------------------\n")
        paths = all_paths(distances, ants)
        phermones *= 0.95  # the decay factor
        file.write("After applying the decay factor: \n"+repr(phermones)+"\n")
    return ants, paths

# --------------------------------------------------------------------------------------------------------
file = open("steps.txt","w")
ants, paths = run(phermones)

df = pd.DataFrame(phermones)
df.to_csv("phermones/Phermones___"+graph_name+".csv", index=False, header=None)

# print(phermones)