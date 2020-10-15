import matplotlib.pyplot as plt
import numpy as np


def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


n = 300
eps, minPts = 5, 3
x = np.random.randint(1, 100, n)
y = np.random.randint(1, 100, n)
# хранение цветов
flags = []
for i in range(0, n):
    # количество соседей, -1 потому что считает себя
    neighb = -1
    for j in range(0, n):
        if dist(x[i], y[i], x[j], y[j]) < eps:
            neighb += 1
    if neighb >= minPts:
        flags.append('g')
    else:
        flags.append('r')


def recursive_point_mark(point, visited_points, clusters, cluster_numb):
    clusters[point] = cluster_numb
    visited_points[point] = True
    for i in range(0, n):
        if dist(x[point], y[point], x[i], y[i]) < eps:
            if not visited_points[i]:
                recursive_point_mark(i, visited_points, clusters, cluster_numb)


visited_points = [False for i in range(n)]
clusters = [0 for i in range(n)]
cluster_numb = 1

for i in range(0, n):
    if flags[i] != 'g':
        for j in range(0, n):
            if flags[j] == 'g':
                if dist(x[i], y[i], x[j], y[j]) < eps:
                    flags[i] = 'y'
                    break
    if flags[i] == 'g' and not visited_points[i]:
        recursive_point_mark(i, visited_points, clusters, cluster_numb)
        cluster_numb += 1
    plt.scatter(x[i], y[i], color=flags[i])
print(cluster_numb)

for i in range(0, n):
    if clusters[i] != 0:
        for j in range(0, n):
            if clusters[j] == clusters[i]:
                x_values = [x[i], x[j]]
                y_values = [y[i], y[j]]
                plt.plot(x_values, y_values)

plt.show()
# clusters = []
# for i in range (0, n):
#     for j in range (i, n):

# присваиваем номер и увелич на 1, проверяем зеленая или нет
# все ближ зеленые
