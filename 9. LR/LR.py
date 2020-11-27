import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import KMeans
from sklearn.svm import SVC


def predict(features, weights):
    zz = np.dot(features, weights)
    return 1 / (1 + np.exp(-zz))


def update_weights(features, labels, weights, lr):
    N = len(features)
    predictions = predict(features, weights)
    gradient = np.dot(np.transpose(features), predictions - labels)
    return weights - gradient * lr / N


def train(features, labels, weights, lr, iters):
    for i in range(iters):
        weights = update_weights(features, labels, weights, lr)
    return weights


def decision(proc):
    return 'yellow' if proc >= 0.5 else 'green'


# colors = ("#FF0000", "#0000FF")
# рандомно задаем точки
n = 100  # количество точек
# координаты точек для 3d
x = np.random.randint(0, 100, n)
y = np.random.randint(0, 100, n)
z = np.random.randint(0, 100, n)
# должны каким-то образом разделить точки на классы
# в частности применить k-means
points = []
for i in range(n):
    points.append([x[i], y[i], z[i]])
kmeans = KMeans(n_clusters=2, random_state=0).fit(points)
clusters = kmeans.labels_
# print(clusters)
colors = ['green'] * n
for i in range(n):
    if clusters[i] == 1:
        colors[i] = 'yellow'
    # рисуем их при помощи plotly

fig = go.Figure(data=[go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(color=colors))])

fig.show()

# предиктить новые точки (тоже на вход рандомно)
x_new = np.random.randint(0, 100)
y_new = np.random.randint(0, 100)
z_new = np.random.randint(0, 100)
fig = go.Figure(data=[go.Scatter3d(x=[x_new], y=[y_new], z=[z_new],
                                   mode='markers', marker=dict(color=['black']))])

points.append([x_new, y_new, z_new])

weights = train(points[:(len(points) - 1)], clusters, [0, 0, 0], 0.001, 5000)

print("Weights: [", weights[0], " , ", weights[1], " , ", weights[2], "]")
print("Test point:", points[(len(points) - 1)])
prediction = predict(points, weights)[len(points) - 1]

print("Prediction: point is ", decision(prediction), predict(points, weights)[len(points) - 1] * 100, "% ")

fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='markers', marker=dict(color=colors)))

svc = SVC(kernel='linear')
svc.fit(points[:n], clusters)

zz = lambda x, y: (-svc.intercept_[0] - svc.coef_[0][0] * x - svc.coef_[0][1] * y) / svc.coef_[0][2]

tmp = np.linspace(0, 100, 50)
xx, yx = np.meshgrid(tmp, tmp)

fig.add_trace(go.Surface(x=xx, y=yx, z=zz(xx, yx)))
fig.show()
