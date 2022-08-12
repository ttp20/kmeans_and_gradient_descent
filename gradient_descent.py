import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from scipy.stats import linregress

# training data 
x_train = [2,9,7,9,11,16,15,23,22,29,29,35,37,40,46]
y_train = [2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]


def loss(beta):
	m = len(x_train)
	return 0.5/m * np.linalg.norm(X.dot(beta) - Y, 2)**2
    
def grad(beta):
	m = len(x_train)
	return 1/m * X.T.dot(X.dot(beta)-Y)

def gradient_descent(beta_init, learning_rate, iteration):
    beta_list = [beta_init]
    for i in range(iteration):
        beta_new = beta_list[-1] - learning_rate*grad(beta_list[-1])
        if np.linalg.norm(grad(beta_new))/len(beta_new) < 0.5:
            break
        beta_list.append(beta_new)
    return beta_list



# set figure
fig1 = plt.figure("GD for Linear Regression")
ax = plt.axes(xlim=(-10, 60), ylim=(-1,20))

# scatter plot for training data
plt.plot(x_train, y_train, 'ro')

# fit linear regression line
result = linregress(x_train, y_train)

# plot linear regression line
x_values = np.linspace(1, 46, 2)
plt.plot(x_values, result.intercept + result.slope*x_values, color='green')

# random initial line: y = 2x + 1
intercept = 1
slope = 2
res = [slope, intercept]
plt.plot(x_values, intercept + slope*x_values, color='black')

# rewrite the linear model in matrix form 
Y = np.array([y_train]).T
x = np.array([x_train])
ones = np.ones_like(x)
X = np.concatenate((x.T, ones.T), axis=1)
beta_init = np.array([[slope, intercept]]).T

# run gradient descent
iteration = 90
learning_rate = 0.0001

beta_list = gradient_descent(beta_init, learning_rate, iteration)
print(beta_list[0][0]) # slope
print(beta_list[0][1]) # intercept
for i in range(len(beta_list)):
    slope = beta_list[i][0][0]
    intercept = beta_list[i][1][0]
    plt.plot(x_values, slope*x_values + intercept, color='black')

# draw animation
x_data = []
y_data = []
line , = ax.plot([],[], color = "yellow")
def update(i):
    slope = beta_list[i][0][0]
    intercept = beta_list[i][1][0]

    y_values = intercept + slope*x_values
    line.set_data(x_values, y_values)
    return line,

iters = np.arange(1,len(beta_list), 1)
line_ani = animation.FuncAnimation(fig1, update, iters, interval=50, blit=True)
plt.show()