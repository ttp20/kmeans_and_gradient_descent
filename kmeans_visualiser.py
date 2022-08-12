import pygame
from random import randint
from statistics import mean

# points and cluster points(centroids)
class Point():
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color
    
    def get_xy(self):
        return [self.x, self.y]
    
    def set_x(self, x):
        self.x = x
    
    def set_y(self, y):
        self.y = y
    
    def set_color(self, color):
        self.color = color

    def get_color(self):
        return self.color

 # some useful functions
def distance(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**.5

def assign_label(point, clusters):
    distances_list = [] 
    for cluster in clusters:
        new_distance = distance(point, cluster)
        distances_list.append(new_distance)
    min_distance = min(distances_list)
    i = distances_list.index(min_distance)
    return COLORS[i]

def new_centroid(points):
    x_coordinates = [points[i].x for i in range(len(points))]
    y_coordinates = [points[i].y for i in range(len(points))]
    return [mean(x_coordinates), mean(y_coordinates)]


# pygame interface
pygame.init()

screen = pygame.display.set_mode((1200,650))

pygame.display.set_caption("kmeans visualiser")

running = True

clock = pygame.time.Clock()

# colors
BACKGROUND = (214, 214, 214)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (147, 153, 35)
PURPLE = (255, 0, 255)
SKY = (0, 255, 255)
ORANGE = (255, 125, 25)
GRAPE = (100, 25, 125)
GRASS = (55, 155, 65)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, SKY, ORANGE, GRAPE, GRASS]
BACKGROUND_PANEL = (249, 255, 230)

# texts
font_type = 'microsoftjhengheimicrosoftjhengheiuilight'
font = pygame.font.SysFont(font_type, 30)
font_small = pygame.font.SysFont(font_type, 15)

# a bunch of text
text_plus = font.render('+', True, WHITE)
text_plus_rect = text_plus.get_rect(center=(875, 75))

text_minus = font.render('-', True, WHITE)
text_minus_rect = text_plus.get_rect(center=(975, 75))

text_run = font.render('Run', True, WHITE)
text_run_rect = text_run.get_rect(center=(850+75, 150+25))

text_random = font.render('Random', True, WHITE)
text_random_rect = text_random.get_rect(center=(850+75, 250+25))

text_algorithm = font.render('Algorithm', True, WHITE)
text_algorithm_rect = text_algorithm.get_rect(center=(850+75, 450+25))

text_reset = font.render('Reset', True, WHITE)
text_reset_rect = text_reset.get_rect(center=(850+75, 550+25))

# initial configuration
K = 0
error = 0
points = []
clusters = []
labels = []


while running:
    clock.tick(60)
    screen.fill(BACKGROUND)

    # draw interface

    ## draw panel
    pygame.draw.rect(screen, BLACK, (50, 50, 700, 500))
    pygame.draw.rect(screen, BACKGROUND_PANEL, (55, 55, 690, 490))

    #  button +
    pygame.draw.rect(screen, BLACK, (850, 50, 50, 50))
    screen.blit(text_plus, text_plus_rect)

    # button -
    pygame.draw.rect(screen, BLACK, ((950, 50, 50, 50)))
    screen.blit(text_minus, text_minus_rect)

    # text "K = 0"
    text_k = font.render(f"K = {K}", True, BLACK)
    screen.blit(text_k, (1050, 50))

    # button Run,
    pygame.draw.rect(screen, BLACK, (850, 150, 150, 50))
    screen.blit(text_run, text_run_rect)

    # button Random
    pygame.draw.rect(screen, BLACK, (850, 250, 150, 50))
    screen.blit(text_random, text_random_rect)

    # text "Error = 0"
    text_error = font.render(f"Error : {error}", True, BLACK)
    text_error_rect = text_error.get_rect()
    screen.blit(text_error, (850,350))

    # button Algorithm
    pygame.draw.rect(screen, BLACK, (850, 450, 150, 50))
    screen.blit(text_algorithm, text_algorithm_rect)

    # button Reset
    pygame.draw.rect(screen, BLACK, (850, 550, 150, 50))
    screen.blit(text_reset, text_reset_rect)

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # mouse position when hovering over panel
    if 50 < mouse_x < 750 and 50 < mouse_y < 550:
        text_mouse = font_small.render(f"({mouse_x - 50}, {mouse_y - 50})", True, BLACK)
        screen.blit(text_mouse, (mouse_x + 10, mouse_y))

    # end draw interface

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        

        if event.type == pygame.MOUSEBUTTONDOWN:
            # add points
            if 50 < mouse_x < 750 and 50 < mouse_y < 550:
                labels = []
                point = Point(mouse_x, mouse_y)
                points.append(point)

            # add K
            if 850 < mouse_x < 900 and 50 < mouse_y < 100:
                K += 1
                if K > 9:
                    K = 9
                print("press +")

            # minus K
            if 950 < mouse_x < 1000 and 50 < mouse_y < 100:
                K -= 1
                print("press -")

            # run the algorithm
            if 850 < mouse_x < 1000 and 150 < mouse_y < 200:
                labels = []
                if clusters == []:
                    continue

                for point in points:
                    labels.append(assign_label(point, clusters))
                    point.set_color(assign_label(point, clusters))
                # update new centroids
                new_clusters = []

                for cluster in clusters:
                    cluster_points = [point for point in points if point.color == cluster.color]
                    if cluster_points != []:
                        new_cluster = Point(new_centroid(cluster_points)[0], new_centroid(cluster_points)[1], cluster.color)
                        new_clusters.append(new_cluster)
                clusters = new_clusters

                print("press Run")
            
            # randomly place centroids
            if 850 < mouse_x < 1000 and 250 < mouse_y < 300:
                clusters = []
                for point in points:
                    point.set_color(WHITE)
                for i in range(K):
                    random_point = Point(randint(50,750), randint(50, 550), COLORS[i])
                    clusters.append(random_point)
                print("press Random")

            # K-means using Scikit-learn
            if 850 < mouse_x < 1000 and 450 < mouse_y < 500:
                print("press Algorithm")

            # reset everything
            if 850 < mouse_x < 1000 and 550 < mouse_y < 600:
                K = 0
                error = 0
                points = []
                clusters = []
                labels = []
                print("press Reset")

    # Draw clusters
    for i in range(len(clusters)):
        pygame.draw.circle(screen, clusters[i].color, clusters[i].get_xy(), 8)

    # Draw points
    for i in range(len(points)):
        pygame.draw.circle(screen, BLACK, points[i].get_xy(), 4)
        
        if labels == []:
            pygame.draw.circle(screen, WHITE, points[i].get_xy(), 3)
        else:
            pygame.draw.circle(screen, points[i].color, points[i].get_xy(), 3)
    
    # update error text
    error = 0
    for cluster in clusters:
        for point in points:
            if point.color == cluster.color:
                error += distance(point, cluster)
    error = int(error)
    text_error = font.render(f"Error : {error}", True, BLACK)
    text_error_rect = text_error.get_rect()
    screen.blit(text_error, (850,350))


    pygame.display.flip()

pygame.quit()