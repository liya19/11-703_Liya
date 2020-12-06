import pygame
import pandas as pd
from PIL import Image
from resizeimage import resizeimage
from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

pygame.font.init()

data = pd.DataFrame(columns=['color', 'x', 'y'])


def convert_y_to_vector(y):
    y_vector = np.zeros((len(y), 10))
    for i in range(len(y)):
        y_vector[i, y[i]] = 1
    return y_vector


def sigmoid(x, deriv=False):
    if deriv:
        return x * (1 - x)
    return 1 / (1 + np.exp(-x))


def predict(x):
    L1 = x
    L2 = sigmoid(np.dot(L1, W1))
    L3 = sigmoid(np.dot(L2, W2))
    return np.argmax(L3, axis=1)


def get_data_from_jpeg():
    return np.array(Image.open('screen_resized.jpeg').convert('L').point(lambda x: int(x / 17)))


def image_converter():
    img = Image.open(r'screen.jpeg')
    # img.show()
    resized_img = resizeimage.resize_thumbnail(img, [8, 8])
    # resized_img = resizeimage.resize_contain(img, [8, 8]) #либо thumbnail либо contain
    resized_img = resized_img.convert('RGB')
    resized_img.save('screen_resized.jpeg')
    # resized_img.show()


def create_data(pos, color):
    (x, y) = pos
    hex_color = '#%02x%02x%02x' % tuple([color[0], color[1], color[2]])
    coord = {'color': hex_color, 'x': x, 'y': y}
    global data
    data = data.append(coord, ignore_index=True)
    data.drop_duplicates()


def draw_circle():
    for index, row in data.iterrows():
        pygame.draw.circle(screen, tuple(int(row[0].lstrip('#')[i:i + 2], 16) for i in (0, 2, 4)),
                           (int(row[1]), int(row[2])),
                           radius, thickness)


radius = 25
draw_color = 255, 255, 255
thickness = 0

bg_color = 0, 0, 0
(width, height) = (800, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('dataGenerator')

running = True
pushing = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pushing = True
        elif event.type == pygame.MOUSEBUTTONUP:
            pushing = False

    if pushing:
        create_data(pygame.mouse.get_pos(), draw_color)

    screen.fill(bg_color)
    draw_circle()
    pygame.display.flip()

pygame.image.save(screen, 'screen.jpeg')
pygame.quit()

image_converter()

digits = load_digits()

X = digits.data
Y = digits.target

X_scale = StandardScaler()

X = X_scale.fit_transform(X)
data = get_data_from_jpeg()
data_transformed = data.reshape(1, -1).astype(np.float32)
print(data)
data_transformed = X_scale.transform(data_transformed)
print(data_transformed[0])

eta = 0.7
epochs = 5000

W1 = 2 * np.random.random((64, 30)) - 1
W2 = 2 * np.random.random((30, 10)) - 1

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.4)
y_v_train = convert_y_to_vector(y_train)

for epoch in range(epochs):
    L1 = X_train
    L2 = sigmoid(np.dot(L1, W1))
    L3 = sigmoid(np.dot(L2, W2))

    L3_e = y_v_train - L3
    D3 = L3_e * sigmoid(L3, True)
    L2_e = np.dot(D3, W2.T)
    D2 = L2_e * sigmoid(L2, True)

    W2 += eta * np.dot(L2.T, D3) / len(X)
    W1 += eta * np.dot(L1.T, D2) / len(X)

y_predict = predict(X_test)
print(accuracy_score(y_test, y_predict)*100)
print(predict(data_transformed))
plt.gray()
plt.matshow(data)
plt.show()