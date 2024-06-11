import numpy as np
import math
import matplotlib.pyplot as plt

def graphData(x,y,x_2,y_2):
    plt.figure()
    plt.scatter(x,y, color = 'purple')
    plt.plot(x_2,y_2, color = 'green')
    plt.xlabel('Time in minutes - normalized')
    plt.ylabel('p_NFKB -noramlized')
    plt.title('Over expression of HER2. Reach equilibrium. Block HER2 (in vivo) 1a')
    return plt.show()

def main():
    #estimated data points according to the graph (slide #14)
    #5 data points in 1a
    data_1a = [
                (0,0.8),
                (180,0.81),
                (360,0.82),
                (540,0.41),
                (720,0.22)]

    #store x values (time in minutes) into array t
    t = np.array([data[0] for data in data_1a])
    #store y values into array y
    y = np.array([data[1] for data in data_1a])

    #normalize the x's
    norm_t = []
    for i  in range(len(t)):
        new_t = (t[i]/720)
        norm_t.append(new_t)
        #print(norm_t[i])

    #print("now the y's")

    #normalize the y's
    norm_y = []
    min_y = float(min(y))
    max_y = float(max(y))
    for i in range(len(y)):
        new_y = (y[i]-min_y)/(max_y-min_y)
        norm_y.append(new_y)
        #print(norm_y[i])


    
    #ask user for initial parameter guesses and step size
    a = float(input("Initial value for a: "))
    b = float(input("Initial value for b: "))
    c = float(input("Initial value for c: "))
    step_size = float(input("Step size: "))
    #store user initial guess for running the program again
    initial_a = a
    initial_b = b
    initial_c = c
    #previous parameter values for the gradient descent algorithm
    prev_a = a
    prev_b = b
    prev_c = c
    #initialize iteration number
    iteration = 0

    #calculate using gradient descent
    while True:
        iteration +=1
        #initialize/reset partial_a,b,c values
        partial_a = 0
        partial_b = 0
        partial_c = 0
        
        #summation for each partial derivatives
        for i in range(len(norm_t)):
            partial_a += a*np.exp(-2*b*np.exp(-c*norm_t[i]))-norm_y[i]*np.exp(-b*np.exp(-c*norm_t[i]))
        for i in range(len(norm_t)):
            partial_b += -a*a*np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i]))+norm_y[i]*a*np.exp(-c*norm_t[i]-b*np.exp(-c*norm_t[i]))
        for i in range(len(norm_t)):
            partial_c += a*a*b*norm_t[i]*np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i]))-norm_y[i]*a*b*norm_t[i]*np.exp(-c*norm_t[i]-b*np.exp(-c*norm_t[i]))
        #gradient descent algorithm:
        #update the parameters a,b, and c
        a = prev_a - step_size*partial_a
        b = prev_b - step_size*partial_b
        c = prev_c - step_size*partial_c

        if abs(partial_a)<0.00001 and abs(partial_b)<0.00001 and abs(partial_c)<0.00001:
            print (f"After {iteration}th interations: ")
            print (f"Parameter a is: {a} and partial A is {partial_a}")
            print (f"Parameter b is: {b} and partial B is {partial_b}")
            print (f"Parameter c is: {c} and partial C is {partial_c}")
            #Use the parameters found here for the function f(norm_t). Get and store the output values for the graph
            x = np.linspace(0,1,100)
            f_t = []
            for i in range(len(x)):
                function_t = a * np.exp(-b * np.exp(-c * x[i]))
                f_t.append(function_t)
            graphData(norm_t,norm_y,x,f_t)#calls the graphing function and graphs
            break
        
        elif iteration >500000:
            print("Too many iterations")
            print(initial_a,initial_b,initial_c)
            print("initial a, b, and c above.")
            print(step_size)
            print("step size above.")
            x = np.linspace(0,1,50)
            f_t = []
            for i in range(len(x)):
                function_t = a * np.exp(-b * np.exp(c * x[i]))
                f_t.append(function_t)
            graphData(norm_t,norm_y,x,f_t)
            break

        prev_a = a
        prev_b = b
        prev_c = c

main()
