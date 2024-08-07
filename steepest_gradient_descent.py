import numpy as np
import time
import matplotlib.pyplot as plt


def graph_data(x, y, x_2, y_2):
    plt.figure()
    plt.scatter(x,y, color = 'purple')
    plt.plot(x_2,y_2, color = 'green')
    plt.xlabel('Time in minutes - normalized')
    plt.ylabel('p_NFKB')
    plt.title('Over expression of HER2. Reach equilibrium. Block HER2 (in vivo) 1a')
    plt.ylim([-0.05, 1.05])
    return plt.show()

# least squares
def gamma(a, b, c, d, t, n):
    result = 0
    for i in range(len(t)):
        result += (gompertz(a, b, c, d, t[i]) - n[i]) ** 2
    return result

# Gompertz function with d parameter
def gompertz(a, b, c, d, t):
    return a * np.exp(-b * np.exp(-c * t)) + d

def validate_interval(df, x0, x1):
    print(df(x0), df(x1))
    return df(x0) * df(x1) < 0

def bisection(df, x0, x1, max_iter=100, tol=1e-3):
    print("x0: ", x0, ", x1: ", x1)
    #if not validate_interval(df, x0, x1):
        #return
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

# gradient of gamma
def grad(x0, norm_t, n):
    a = x0[0].item()
    b = x0[1].item()
    c = x0[2].item()
    d = x0[3].item()

    partial_a = 0
    partial_b = 0
    partial_c = 0
    partial_d = 0
    
    # old loop, not cleaned up
    '''for i in range(len(norm_t)):
        partial_a += (a * np.exp(-2*b * np.exp(-c * norm_t[i])) - (n[i] * np.exp(-b * np.exp(-c * norm_t[i]))) + (d * np.exp(-b * np.exp(-c * norm_t[i]))))
        partial_b += (-(a**2) * np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i])) + (n[i] * a * np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))) - (a*d* np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))))
        partial_c += ((a**2) *b*norm_t[i]*np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i])) - (n[i]*a*b*norm_t[i]*np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))) + (norm_t[i]*a*b*d* np.exp(-c*norm_t[i] - b * np.exp(-c*norm_t[i]))))
        partial_d += (a*np.exp(-b*np.exp(-c*norm_t[i])) + d - n[i])'''
    
    #now, consolidated into one loop and clean it up:
    for i in range(len(norm_t)):
        #this is e^(-b*e^(-c*t))
        exp_term_no_coeff = np.exp(-b*np.exp(-c*norm_t[i]))
        #3 terms in side the sum
        inside_terms = (a*np.exp(-b*np.exp(-c*norm_t[i]))+d-n[i])
        #e^((-c*t)-(b*e^(-c*t)))
        exp_term_minus_ct = np.exp((-c*norm_t[i])-b*np.exp(-c*norm_t[i]))
        #summations
        partial_a += (inside_terms)*(exp_term_no_coeff)
        partial_b += (inside_terms)*(-a)*(exp_term_minus_ct)
        partial_c += (inside_terms)*(exp_term_minus_ct)*(a*b*norm_t[i])
        partial_d += (inside_terms)
    
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
    data_1a = [
                (0,0.8),
                (180,0.81),
                (360,0.82),
                (540,0.41),
                (720,0.22)]

    data_1a_int = [(0, 0.8),
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
    
    data_2a = [
                (15,0.8),
                (30,0.41),
                (45,0.2),
                (60,0.1),
                (90,0.2)]

    data_2a_int = [
                (15,0.8),
                (20,0.65),
                (25,0.5199999999999999),
                (30,0.41),
                (35,0.3277777777777778),
                (40,0.2577777777777778),
                (45,0.2),
                (50,0.15444444444444447),
                (55,0.12111111111111111),
                (60,0.1),
                (70,0.08888888888888889),
                (80,0.12222222222222222),
                (90,0.2)]
    
    data_2b = [
                (15,0.7),
                (30,0.61),
                (45,0.41),
                (60,0.3),
                (90,0.2)]

    data_2b_int = [
                (15,0.7),
                (20,0.6822222222222223),
                (25,0.6522222222222221),
                (30,0.61),
                (35,0.5333333333333333),
                (40,0.4666666666666666),
                (45,0.41),
                (50,0.363333333333333),
                (55,0.32666666666666666),
                (60,0.3),
                (70,0.24888888888888888),
                (80,0.21555555555555556),
                (90,0.2)]

    the_data = data_1a
    #the_data = data_1a_int
    #the_data = data_2a
    #the_data = data_2a_int
    #the_data = data_2b
    #the_data = data_2b_int

    # store x values (time) of the data into array t
    t = np.array([data[0] for data in the_data])
    # store y values (number of cells) of the data into array n
    n = np.array([data[1] for data in the_data])

    # normalization of the data
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
    x0 = np.array([-1, 55, 6, 1])
    x0 = np.reshape(x0, (4, 1))
    start_time = time.time()

    # calculate and solve the parameters using the gradient descent method
    while True:
        iteration += 1
        g = grad(x0, norm_t, n)

        def d_ls_fun(z):
            dx0 = g
            x1 = x0 - z * dx0
            dx1 = grad(x1, norm_t, n)
            return np.dot(dx0.T, dx1)

        step_size = bisection(d_ls_fun, -10, 10, 100, 1e-5)
        w = x0 - step_size * g
        
        print(f"iteration: {iteration}")
        print(f"partial a: {g[0]}, partial b:{g[1]}, partial c: {g[2]}, partial d: {g[3]}")

        #print("termination condition: ", np.linalg.norm(w - x0) / np.linalg.norm(x0), np.linalg.norm(w - x0), np.linalg.norm(x0))

        # termination condition for the gradient descent algorithm
        if np.linalg.norm(w - x0) / np.linalg.norm(x0) < 1e-10:
            print(f"After {iteration} iterations: ")
            print(f"Parameter a is: {w[0]} and partial A is {g[0]}")
            print(f"Parameter b is: {w[1]} and partial B is {g[1]}")
            print(f"Parameter c is: {w[2]} and partial C is {g[2]}")
            print(f"Parameter d is: {w[3]} and partial D is {g[3]}")
            print(f"Least squares calculation is: {gamma(w[0], w[1], w[2], w[3], norm_t, n)}")
            print(f"Runtime is: {time.time()-start_time} seconds")

            # Use the parameters found here for the function f(t). Get and store the output values for the graph
            x = np.linspace(0, 1, 100)
            f_t = []
            for i in range(len(x)):
                function_t = w[0] * np.exp(-w[1] * np.exp(-w[2] * x[i])) + w[3]
                f_t.append(function_t)
            graph_data(norm_t, n, x, f_t)  # calls the graphing function and graphs
            break

        '''
        elif iteration > 10000:
            print("Too many iterations")
            print(initial_a, initial_b, initial_c, step_size)
            print(a, b, c)
            print(f"partial a: {g[0]}, partial b:{g[1]}, partial c: {g[2]}")
            break
        '''

        x0 = w

main()