#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import matplotlib.pyplot as plt
import random
import math
from scipy.interpolate import interp1d

def f(y, t, k_values, deg_values, her2):
    erk, akt, il1, ikk, ikb_nfkb, p_ikb, p_nfkb, ikb = y
    k_1, k_2, k_3, k_4, k_5, k_6, k_7, k_8, k_9, k_10 = k_values
    deg_1, deg_2, deg_3, deg_4, deg_5 = deg_values

    next_erk = k_1*her2 - k_2*akt*erk - deg_1*erk
    next_akt = k_3*her2 - deg_2*akt
    next_il1 = k_4 * erk + k_5 * p_nfkb - deg_3 * il1
    next_ikk = k_6 * akt + k_7 * il1 - deg_4 * ikk
    next_ikb_nfkb = -1 * k_8 * ikk * ikb_nfkb + k_9 * ikb * p_nfkb
    next_p_ikb = k_8 * ikk * ikb_nfkb - deg_5 * p_ikb
    next_p_nfkb = k_8 * ikk * ikb_nfkb - k_9 * ikb * p_nfkb
    next_ikb = k_10 * p_nfkb - k_9 * ikb * p_nfkb

    return np.array([next_erk, next_akt, next_il1, next_ikk, next_ikb_nfkb, next_p_ikb, next_p_nfkb, next_ikb])

def rk2(f, y0, h, k_values, deg_values, her2):  # step size
    t = t_0(h)
    y = np.zeros((len(t), len(y0) + 1))  # +1 for time
    y[0, 0] = t[0]  # set initial time
    y[0, 1:] = y0  # set initial conditions
    for i in range(len(t) - 1):
        k1 = h * f(y[i, 1:], t[i], k_values, deg_values, her2)
        k2 = h * f(y[i, 1:] + k1, t[i] + h, k_values, deg_values, her2)
        y[i+1, 0] = round(t[i+1],12)  # store time
        y[i+1, 1:] = y[i, 1:] + 0.5 * (k1 + k2)  # store solution
    return y

her2 = 1
erk_start = 1
akt_start = 1
il1_start = 1
ikk_start = 1
ikb_nfkb_start = 1
p_ikb_start = 1
p_nfkb_start = 1
ikb_start = 1

y0 = np.array([erk_start, akt_start, il1_start, ikk_start, ikb_nfkb_start, p_ikb_start, p_nfkb_start, ikb_start])
#                 0,         1            2           3          4        5               6                 7          8
k1 = .1
k2 = .2
k3 = .3
k4 = .4
k5 = .5
k6 = .6
k7 = .7
k8 = .8
k9 = .9
k10 = .95
k_values = [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10]

deg_1 = .5
deg_2 = .5
deg_3 = .5
deg_4 = .5
deg_5 = .5
deg_values = [deg_1, deg_2, deg_3, deg_4, deg_5]

# Time points
h = 0.01

def t_0(h):
    return np.arange(0,1+h, h)

# Solve the system
y = rk2(f, y0, h, k_values, deg_values, her2)

h_actual = 0.00000001
actual = rk2(f, y0, h_actual, k_values, deg_values, her2)
    
#div = int((len(t_actual)-1)/(len(t)-1))
#actual_2 = actual[::div,:]

#error = np.abs(y - actual_2)
#max_error = np.max(error)

#h = t[1] - t[0]
#order_of_accuracy = np.log(max_error) / np.log(h)
#print(f"Order of accuracy: {order_of_accuracy}")




##### Order Calculations from Last Year Code #####


def E2(f, y0, h, k_values, deg_values, her2):
    t = t_0(h)
    t_actual = t_0(h_actual)
    y = rk2(f, y0, h, k_values, deg_values, her2)
    iter = 0
    iter = 0
    actual_cut = []
    for i in range(len(y)):
        while y[i,0] != actual[iter,0]:
            iter += 1
            if iter >= len(actual):
                print("Exit due to error")
                sys.exit()
        actual_cut.append(actual[iter,:]) 
    error = np.abs(y - actual_cut)
    max_error = np.max(error)
    return max_error

def order(f,y0,h,k_values,deg_values,her2):
    h_new = h / 2
    e2 = E2(f,y0,h_new,k_values,deg_values,her2)
    e1 = E2(f,y0,h,k_values,deg_values,her2)
    ratio = float(e2/e1)
    print(f"ratio of the error is {ratio}")
    n = math.log2(abs(ratio))  #Calculates the order, n
    return -n


def convergence(f,y0,h,k_values,deg_values,her2):
    print("\nFor max error")
    print(f"Order with h = {h} and h/2 = {h / 2} is: {order(f,y0,h,k_values,deg_values,her2)}")
    h = h / 2
    print(f"Order with h = {h} and h/2 = {h / 2} is: {order(f,y0,h,k_values,deg_values,her2)}")
    h = h / 2
    print(f"Order with h = {h} and h/2 = {h / 2} is: {order(f,y0,h,k_values,deg_values,her2)}")
    h = h / 2
    print(f"Order with h = {h} and h/2 = {h / 2} is: {order(f,y0,h,k_values,deg_values,her2)}")
    h = h / 2
    print(f"Order with h = {h} and h/2 = {h / 2} is: {order(f,y0,h,k_values,deg_values,her2)}")





# In[8]:


convergence(f,y0,h,k_values,deg_values,her2)

