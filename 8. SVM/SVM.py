import pygame as pygame
import numpy as np
from sklearn import svm

pygame.font.init()

# Окно игры: размер, позиция

screen = pygame.display.set_mode((1000, 700))
screen.fill((255, 255, 255))

data = np.empty((0, 5), dtype='f')


def create_data(pos, color):
    (x, y) = pos
    coord = [color[0], color[1], color[2], x, y]
    global data
    data = np.append(data, [coord], axis=0)
    points.append(pos)


def draw_circle():
    for point in data:
        pygame.draw.circle(screen, (point[0], point[1], point[2]), (int(point[3]), int(point[4])), radius, thickness)


radius = 7
selected_color = 0, 0, 255
selected_color_1 = 255, 0, 0

thickness = 0
points = []
clusters = []

pygame.display.update()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                create_data(pygame.mouse.get_pos(), selected_color)
                clusters.append(0)
            elif event.button == 3:
                create_data(pygame.mouse.get_pos(), selected_color_1)
                clusters.append(1)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                model = svm.SVC(kernel='linear', C=1.0)
                model.fit(points, clusters)

                W = model.coef_[0]
                I = model.intercept_

                xy = np.zeros((3, 2))
                xy[0][0] = -(I[0] / W[1])
                xy[0][1] = (I[0] / W[1]) / (-W[0] / W[1])

                xy[1][0] = 1 / W[1] - (I[0] / W[1])
                xy[1][1] = 1 / W[0] + (I[0] / W[1]) / (-W[0] / W[1])

                xy[2][0] = -1 / W[1] - (I[0] / W[1])
                xy[2][1] = -1 / W[0] + (I[0] / W[1]) / (-W[0] / W[1])
    
                pygame.draw.aaline(screen, (0, 0, 0), [0, xy[2][0]], [xy[2][1], 0])
                pygame.draw.aaline(screen, (0, 0, 0), [0, xy[1][0]], [xy[1][1], 0])

                pygame.draw.line(screen, (231, 109, 170), [0, xy[0][0]], [xy[0][1], 0], 2)

                pygame.display.update()

        draw_circle()
        pygame.display.flip()


pygame.quit()
