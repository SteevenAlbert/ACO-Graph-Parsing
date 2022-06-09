#---------------------------------------------------
#   Created by:                            
#   Laila Elhattab  
#   Steven Albert  
#   Rana Raafat          
#   Judy Wagdy             
#                       
#   Supervised by:          
#   Dr. Eslam Amer          
#---------------------------------------------------

import numpy as np
import pandas as pd
np.set_printoptions(suppress=True)


#----------------------------------------------INITIALIZATION------------------------------------------
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


#------------------------------------------------FUNCTIONS-----------------------------------------------
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
    return start_ants


row_mean = distances.mean(axis=1)

# Spread the phermones depending on the weight of the edge
def spread_phermone(path):
    for i in range(len(path)):
        phermones[path[i][0]][path[i][1]] *= distances[path[i][0]][path[i][1]]


# Check whether this edge should be visited
def promising(start, end, path):
    sum = 0

    # Check whether the learning rate will increase with the addition of this edge
    for i in range(len(path)):
        sum += distances[path[i][0]][path[i][1]]
    lr = sum/len(path)

    new_sum = sum + distances[start][end]
    new_lr = new_sum/(len(path)+1)

    # Check whether the end node has already been visited
    if not any(end in sublist for sublist in path) and new_lr >= lr:
        return True
    return False


# Generate all paths in a single iteration
def all_paths(distances, start_ants):
    paths = []
    for i in range(len(start_ants)):
        path = []
        ant_path(distances, start_ants[i], path)
        paths.append(path)
    for j in range(len(paths)):
        spread_phermone(paths[j])
    return paths


# Generate the path of a single ant
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

# The main function 
def run(iterations, phermones):
    for i in range(iterations):
        ants = find_start_ants(distances)
        all_paths(distances, ants)
        phermones *= 0.95 # the decay factor 

def NormalizeData(data):
    return (data - np.min(data)) / (np.max(data) - np.min(data))

#--------------------------------------------------------------------------------------------------------
run(2, phermones)
# print ("----------------------------PHERMONES--------------------------")
# print(phermones)

scaledPhermones = NormalizeData(phermones)
df = pd.DataFrame(phermones)
df.to_csv("Phermones.csv")

df = pd.DataFrame(scaledPhermones)
df.to_csv("ScaledPhermones.csv")
# print ("--------------------------SCALED PHERMONES-----------------------")
# print(scaledPhermones)
