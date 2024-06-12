#!/usr/bin/env python
# coding: utf-8

# In[109]:


import numpy as np
import math
import matplotlib.pyplot as plt


# In[169]:


t = np.array([0, 180, 360, 540, 720])


# In[170]:


n = np.array([0.8, 0.81, 0.82, 0.41, 0.22])


# In[171]:


def graph_data(x,y,x_2,y_2):
    plt.figure()
    plt.scatter(x,y, color='red')
    plt.plot(x_2,y_2, color='blue')
    plt.xlabel('Number of Minutes')
    plt.ylabel('Concentration of Her2')
    plt.title("Her2 Concentration Over Time")
    return plt.show()


# In[205]:


def main2():
    
    #normalization of the data
    min_n = float(min(n))
    max_n = float(max(n))
    norm_n =[] #this is the new list where the normalized data goes
    for i in range(len(n)):
        value = float((n[i] - min_n) / (max_n - min_n))
        norm_n.append(value)

    min_t = float(min(t))
    max_t = float(max(t))
    norm_t = []
    for i in range(len(t)):
        value = float((t[i] - min_t) / (max_t - min_t))
        norm_t.append(value)
    
    #user makes the initial guesses for the parameters and step size
    a = float(input("Initial value for a: "))
    initial_a = a
    b = float(input("Initial value for b: "))
    initial_b = b
    c = float(input("Initial value for c: "))
    initial_c = c
    d = float(input("Initial value for d:"))
    initial_d = d
    step_size = float(input("Determine the step size: "))
    #initialize variables
    prev_a = a
    prev_b = b
    prev_c = c
    prev_d = d
    iteration = 0

    #calculate and solve the parameters using the gradient descent method
    while True:
        iteration += 1
        partial_a = 0
        partial_b = 0
        partial_c = 0
        partial_d = 0
        for i in range(len(t)):
            partial_a += (a * np.exp(-2*b * np.exp(-c * norm_t[i])) - (norm_n[i] * np.exp(-b * np.exp(-c * norm_t[i]))) + (d * np.exp(-b * np.exp(-c * norm_t[i]))))
        for i in range(len(t)):
            partial_b += (-(a**2) * np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i])) + (norm_n[i] * a * np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))) - (a*d* np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))))
        for i in range(len(t)):
            partial_c += ((a**2) *b*norm_t[i]*np.exp(-c*norm_t[i]-2*b*np.exp(-c*norm_t[i])) - (norm_n[i]*a*b*norm_t[i]*np.exp(-c*norm_t[i] - b*np.exp(-c*norm_t[i]))) + (norm_t[i]*a*b*d* np.exp(-c*norm_t[i] - b * np.exp(-c*norm_t[i]))))
        for i in range(len(t)):
            partial_d += (a*np.exp(-b*np.exp(-c*norm_t[i])) + d - norm_n[i])
        a = prev_a  - (step_size * partial_a) #next iteration of a gets updated i.e. a^(k+1)
        b = prev_b  - (step_size * partial_b)
        c = prev_c  - (step_size * partial_c)
        d = prev_d  - (step_size * partial_d)
        #print(f"iteration: {iteration}")
        #print(f"partial a: {partial_a}, partial b:{partial_b}, partial c: {partial_c}")
        #print(f"Iteration: {iteration}")#checks for infinite loop
        if abs(partial_a)<0.0001 and abs(partial_b)<0.0001 and abs(partial_c)<0.0001 and abs(partial_d)<0.0001: #termination condition for the gradient descent algorithm
            print (f"After {iteration}th iteration: ")
            print (f"Parameter a is: {a} and partial A is {partial_a}")
            print (f"Parameter b is: {b} and partial B is {partial_b}")
            print (f"Parameter c is: {c} and partial C is {partial_c}")
            print (f"Parameter d is: {d} and partial D is {partial_d}")
            #Use the parameters found here for the function f(t). Get and store the output values for the graph
            x = np.linspace(0,1,100)
            f_t = []
            for i in range(len(x)):
                function_t = (a * np.exp(-b * np.exp(-c * x[i]))) + d
                f_t.append(function_t)
            graph_data(norm_t,norm_n,x,f_t)#calls the graphing function and graphs
            break
        elif iteration>2000000:
            print("Too many iterations")
            print(initial_a, initial_b, initial_c, initial_d, step_size)
            print(a,b,c,d)
            print(f"partial a: {partial_a}, partial b:{partial_b}, partial c: {partial_c}, partial d: {partial_d}")
            break
        prev_a = a
        prev_b = b
        prev_c = c
        prev_d = d


# In[207]:


main2()


# In[ ]:




