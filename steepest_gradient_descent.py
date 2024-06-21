import numpy as np
import math
import matplotlib.pyplot as plt


def graph_data(x, y, x_2, y_2):
    plt.figure()
    plt.scatter(x, y, color='red')
    plt.plot(x_2, y_2, color='blue')
    plt.xlabel('Number of Days')
    plt.ylabel('Number of Cells')
    plt.title("Vector Cells - Regular Cancer Cells")
    plt.ylim([-0.05, 1.05])
    return plt.show()

def gamma(a, b, c, d, t, n):
    result = 0
    for i in range(len(t)):
        result += (a * np.exp(-b * np.exp(-c * t[i])) + d - n[i]) ** 2
    return result

def f(a, b, c, d, t):
    return a * np.exp(-b * np.exp(-c * t)) + d

def validate_interval(df, x0, x1):
    print(df(x0))
    print(df(x1))
    return df(x0) * df(x1) < 0

def bisection(df, x0, x1, max_iter=100, tol=1e-3):
    # if not validate_interval(df, x0, x1):
        # return
    for i in range(max_iter):
        approximation = x0 + (x1 - x0) / 2
        y = df(approximation)
        if -tol < y < tol:
            return approximation
        if validate_interval(df, x0, approximation):
            x1 = approximation
        else:
            x0 = approximation
    return approximation


def grad(x0, norm_t, norm_n):
    a = x0[0].item()
    b = x0[1].item()
    c = x0[2].item()
    d = x0[3].item()

    partial_a = 0
    partial_b = 0
    partial_c = 0
    partial_d = 0
    
    for i in range(len(norm_t)):
        partial_a += (a * np.exp(-2*b * np.exp(-c * norm_t[i])) - (norm_n[i] * np.exp(-b * np.exp(-c * norm_t[i]))) + (d * np.exp(-b * np.exp(-c * norm_t[i]))))
        partial_b += (-(a**2) * np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i])) + (norm_n[i] * a * np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))) - (a*d* np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))))
        partial_c += ((a**2) *b*norm_t[i]*np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i])) - (norm_n[i]*a*b*norm_t[i]*np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))) + (norm_t[i]*a*b*d* np.exp(-c*norm_t[i] - b * np.exp(-c*norm_t[i]))))
        partial_d += (a*np.exp(-b*np.exp(-c*norm_t[i])) + d - norm_n[i])
    
    g = np.zeros((4, 1))
    g[0] = partial_a
    g[1] = partial_b
    g[2] = partial_c
    g[3] = partial_d
    
    # g[0] = 4 * ((a - 4) ** 3)
    # g[1] = 2 * (b - 3)
    # g[2] = 16 * ((c + 5) ** 3)
    # g[3] = some other simplification?
    
    return g


def main():
    # below are the collected data points from the 2023 lab
    '''data_1 = [(0,150000),
            (1,53777),
            (2,65333),
            (3,134909),
            (4,222000),
            (5,248773),
            (6,376560),
            (7,555000),
            (8,975000),
            (9,1280000),
            (12,2302000),
            (13,2673000),
            (14,2870000)]'''

    # below is the sample data from the 2024 lab supplemented by LaGrange interpolation
    data_1 = [(0, 0.8),
              (60, 0.8033),
              (120, 0.8067),
              (180, 0.81),
              (240, 0.8133),
              (300, 0.8167),
              (360, 0.82),
              (420, 0.6589),
              (480, 0.5222),
              (540, 0.41),
              (600, 0.3222),
              (660, 0.2589),
              (720, 0.22)]

    # store x values (time) of the data into array t
    t = np.array([data[0] for data in data_1])
    # store y values (number of cells) of the data into array n
    n = np.array([data[1] for data in data_1])

    # normalization of the data
    min_n = float(min(n))
    max_n = float(max(n))
    norm_n = []  # this is the new list where the normalized data goes
    for i in range(len(n)):
        value = float((n[i] - min_n) / (max_n - min_n))
        norm_n.append(value)

    min_t = float(min(t))
    max_t = float(max(t))
    norm_t = []  # this is the new list where the normalized data goes
    for i in range(len(t)):
        value = float((t[i] - min_t) / (max_t - min_t))
        norm_t.append(value)

    # user makes the initial guesses for the parameters and step size
    # a = float(input("Initial value for a: "))
    # initial_a = a
    # b = float(input("Initial value for b: "))
    # initial_b = b
    # c = float(input("Initial value for c: "))
    # initial_c = c
    # d = float(input("Initial value for d: "))
    # initial_d = d
    # note: no need for initial step size

    # initialize variables
    iteration = 0
    x0 = np.array([1, 1, 1, 1])
    x0 = np.reshape(x0, (4, 1))

    # calculate and solve the parameters using the gradient descent method
    while True:
        iteration += 1
        g = grad(x0, norm_t, norm_n)

        def d_ls_fun(z):
            return np.dot(g.T, grad(x0 - z * g, norm_t, norm_n))

        print("iteration: ", iteration)
        step_size = bisection(d_ls_fun, -10, 10, 30, 1e-2)
        w = x0 - step_size * g
        # print(f"iteration: {iteration}")
        # print(f"partial a: {g[0]}, partial b:{g[1]}, partial c: {g[2]}, partial d: {g[3]}")

        # termination condition for the gradient descent algorithm
        if np.linalg.norm(w - x0) / np.linalg.norm(x0) < 1e-4:
            print(f"After {iteration}th interations: ")
            print(f"Parameter a is: {w[0]} and partial A is {g[0]}")
            print(f"Parameter b is: {w[1]} and partial B is {g[1]}")
            print(f"Parameter c is: {w[2]} and partial C is {g[2]}")
            print(f"Parameter d is: {w[3]} and partial D is {g[3]}")

            # Use the parameters found here for the function f(t). Get and store the output values for the graph
            x = np.linspace(0, 1, 100)
            f_t = []
            for i in range(len(x)):
                function_t = w[0] * np.exp(-w[1] * np.exp(-w[2] * x[i])) + w[3]
                f_t.append(function_t)
            graph_data(norm_t, norm_n, x, f_t)  # calls the graphing function and graphs
            break

        # elif iteration > 10000:
        #     print("Too many iterations")
        #     print(initial_a, initial_b, initial_c, step_size)
        #     print(a, b, c)
        #     print(f"partial a: {g[0]}, partial b:{g[1]}, partial c: {g[2]}")
        #     break
        x0 = w


main()

'''data_2 = [(0,150000),
            (1,53777),
            (2,65333),
            (3,134909),
            (4,222000),
            (5,248773),
            (6,376560),
            (7,555000),
            (8,975000),
            (9,1280000),
            (12,2302000),
            (13,2673000),
            (14,2870000)]'''