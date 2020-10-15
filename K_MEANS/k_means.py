import matplotlib.pyplot as plt
import numpy as np
import random

n = 100
x = [random.randint(1, n) for i in range(n)]
y = [random.randint(1, n) for i in range(n)]
K = range(0, 10)

# Ищем центральную точку (пункт 2)
x_c = np.mean(x)
y_c = np.mean(y)


def dist(x1, y1, x2, y2):
    return np.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def clust(x, y, x_cc, y_cc, k):
    cluster = []
    for i in range(0, n):
        d = dist(x[i], y[i], x_cc[0], y_cc[0])
        numb = 0
        for j in range(0, k):
            if dist(x[i], y[i], x_cc[j], y_cc[j]) < d:
                d = dist(x[i], y[i], x_cc[j], y_cc[j])
                numb = j
        cluster.append(numb)
    return cluster


def calculate_center_of_mass(cluster, x, y, k):
    center_of_mass_x = [0 for i in range(k)]
    center_of_mass_y = [0 for i in range(k)]
    count = [0 for i in range(k)]

    for i in cluster:
        count[i] += 1

    number = 0
    for i in cluster:
        center_of_mass_x[i] += x[number] / count[i]
        center_of_mass_y[i] += y[number] / count[i]
        number += 1

    return [center_of_mass_x, center_of_mass_y]


R = 0
for i in range(0, n):
    r = dist(x_c, y_c, x[i], y[i])
    if r > R:
        R = r


def J_c(k, x_cc, y_cc, cluster):
    for i in range(0, k):
        clusterSum = 0
        for j in range(0, len(cluster)):
            if (cluster[j] == i):
                clusterSum += dist(x[j], y[j], x_cc[i], y_cc[i]) ** 2
    return clusterSum


val_k = []
for k in K:
    x_cc = [R * np.cos(2 * np.pi * i / k) + x_c for i in range(k)]
    y_cc = [R * np.sin(2 * np.pi * i / k) + x_c for i in range(k)]

cluster = clust(x, y, x_cc, y_cc, k)

center_of_mass = calculate_center_of_mass(cluster, x, y, k)
# сравнение текущего расположения точек
# с новым прощитанными
changed = False
while not changed:
    new_cluster = clust(x, y, center_of_mass[0], center_of_mass[1], k)

    val_k.append(J_c(k, x_cc, y_cc, cluster))
    if np.array_equal(new_cluster, cluster):
        changed = True
        break

    cluster = new_cluster
    center_of_mass = calculate_center_of_mass(cluster, x, y, k)

print(val_k)

plt.plot(K[0:len(val_k)], val_k)
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

k = len(val_k) - 1
changed = False
while not changed:
    new_cluster = clust(x, y, center_of_mass[0], center_of_mass[1], k)
    if np.array_equal(new_cluster, cluster):
        changed = True
        break

    cluster = new_cluster

    center_of_mass = calculate_center_of_mass(cluster, x, y, k)

    colors = ['r', 'b', 'y', 'o', 'p']

print(k)
for i in range(0, n):
    plt.scatter(x[i], y[i], color=colors[cluster[i]])
    plt.scatter(center_of_mass[0], center_of_mass[1], marker='o', c='b', s=250)
plt.show()
