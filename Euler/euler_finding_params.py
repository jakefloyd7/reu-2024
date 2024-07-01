# This is a sample Python script.

# Press Ctrl+F5 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import numpy as np
import matplotlib.pyplot as plt
import random

def next_erk(step_size, her2, akt, erk, k_1, k_2, deg_1):
    return float(erk + step_size * (k_1 * her2 - k_2 * akt * erk - deg_1 * erk))


def next_akt(step_size, her2, akt, k_3, deg_2):
    return float(akt + step_size * (k_3 * her2 - deg_2 * akt))


def next_il1(step_size, erk, p_nfkb, il1, k_4, k_5, deg_3):
    return float(il1 + step_size * (k_4 * erk + k_5 * p_nfkb - deg_3 * il1))


def next_ikk(step_size, akt, il1, ikk, k_6, k_7, deg_4):
    return float(ikk + step_size * (k_6 * akt + k_7 * il1 - deg_4 * ikk))


def next_ikb_nfkb(step_size, ikk, ikb_nfkb, ikb, p_nfkb, k_8, k_9):
    return float(ikb_nfkb + step_size * (-1 * k_8 * ikk * ikb_nfkb + k_9 * ikb * p_nfkb))


def next_p_ikb(step_size, ikk, ikb_nfkb, p_ikb, k_8, deg_5):
    return float(p_ikb + step_size * (k_8 * ikk * ikb_nfkb - deg_5 * p_ikb))


def next_p_nfkb(step_size, ikk, ikb_nfkb, ikb, p_nfkb, k_8, k_9):
    return float(p_nfkb + step_size * (k_8 * ikk * ikb_nfkb - k_9 * ikb * p_nfkb))


def next_ikb(step_size, p_nfkb, ikb, k_9, k_10):
    return float(ikb + step_size * (k_10 * p_nfkb - k_9 * ikb * p_nfkb))


def eulers_method(step_size, t_start, t_end, start_values, k_values, deg_values):
    steps = int((t_end - t_start) / step_size)

    stored_erk = [start_values[1]]
    stored_akt = [start_values[2]]
    stored_il1 = [start_values[3]]
    stored_ikk = [start_values[4]]
    stored_ikb_nfkb = [start_values[5]]
    stored_p_ikb = [start_values[6]]
    stored_p_nfkb = [start_values[7]]
    stored_ikb = [start_values[8]]

    for i in range(steps):
        stored_erk.append(next_erk(step_size, start_values[0], stored_akt[i], stored_erk[i], k_values[0], k_values[1], deg_values[0]))
        stored_akt.append(next_akt(step_size, start_values[0], stored_akt[i], k_values[2], deg_values[1]))
        stored_il1.append(next_il1(step_size, stored_erk[i], stored_p_nfkb[i], stored_il1[i], k_values[3], k_values[4], deg_values[2]))
        stored_ikk.append(next_ikk(step_size, stored_akt[i], stored_il1[i], stored_ikk[i], k_values[5], k_values[6], deg_values[3]))
        stored_ikb_nfkb.append(next_ikb_nfkb(step_size, stored_ikk[i], stored_ikb_nfkb[i], stored_ikb[i], stored_p_nfkb[i], k_values[7], k_values[8]))
        stored_p_ikb.append(next_p_ikb(step_size, stored_ikk[i], stored_ikb_nfkb[i], stored_p_ikb[i], k_values[7], deg_values[4]))
        stored_p_nfkb.append(next_p_nfkb(step_size, stored_ikk[i], stored_ikb_nfkb[i], stored_ikb[i], stored_p_nfkb[i], k_values[7], k_values[8]))
        stored_ikb.append(next_ikb(step_size, stored_p_nfkb[i], stored_ikb[i], k_values[8], k_values[9]))
    return stored_p_nfkb


def graphData(t_values, actual_values, approx_values, t_data, x_data):
    plt.figure()
    plt.scatter(t_data, x_data, color= 'blue')
    plt.plot(t_values,approx_values, color = 'purple')
    plt.plot(t_values,actual_values, color = 'green')
    plt.xlabel('Time in minutes - normalized')
    plt.ylabel('p_NFKB -noramlized')
    plt.title('Over expression of HER2. Reach equilibrium. Block HER2 (in vivo) 1a')
    return plt.show()

# write a method that represents the actual function using the data fitting equation
def actual(data):
    a = data[0]
    b = data[1]
    c = data[2]
    d = data[3]
    t = 0
    p_actual = [a*np.exp(-b*np.exp(-c*t))+d]
    while t < 1:
        t += h
        p_actual.append(a*np.exp(-b*np.exp(-c*t))+d)
    return p_actual



def main():

    # code borrowed from gradient descent code to find normalized points
    data_1a = [
                (0,0.8),
                (180,0.81),
                (360,0.82),
                (540,0.41),
                (720,0.22)]

    #store x values (time in minutes) into array t
    t = np.array([data[0] for data in data_1a])
    #t = t/72
    #store y values into array y
    y = np.array([data[1] for data in data_1a])

    #normalize the x's
    min_t = float(min(t))
    max_t = float(max(t))
    norm_t = []
    for i in range(len(t)):
        value = float((t[i] - min_t) / (max_t - min_t))
        norm_t.append(value)

    #normalize the y's
    norm_y = []
    min_y = float(min(y))
    max_y = float(max(y))
    for i in range(len(y)):
        new_y = (y[i]-min_y)/(max_y-min_y)
        norm_y.append(new_y)
        #print(norm_y[i])


    iter = 0
    runs =  0
    while True:
        iter +=1
        her2_start = random.uniform(0,.2)
        erk_start = random.uniform(7,12)
        akt_start = random.uniform(0,1)
        il1_start = random.uniform(0,3)
        ikk_start = random.uniform(0,2)
        ikb_nfkb_start = random.uniform(8,12)
        p_ikb_start = random.uniform(0,.1)
        p_nfkb_start = 1
        ikb_start = random.uniform(3,5)

        start_values = [her2_start, erk_start, akt_start, il1_start, ikk_start, ikb_nfkb_start, p_ikb_start, p_nfkb_start, ikb_start]
        #                 0,         1            2           3              4        5         6                 7            8
        k_1 = random.uniform(0,5)
        k_2 = random.uniform(5,10)
        k_3 = random.uniform(0,5)
        k_4 = random.uniform(0,5)
        k_5 = random.uniform(0,2)
        k_6 = random.uniform(30,100)
        k_7 = random.uniform(0,10)
        k_8 = random.uniform(0,2)
        k_9 = random.uniform(0,2)
        k_10 = random.uniform(10,20)
        k_values = [k_1, k_2, k_3, k_4, k_5, k_6, k_7, k_8, k_9, k_10]

        deg_1 = random.uniform(5,10)
        deg_2 = random.uniform(5,10)
        deg_3 = random.uniform(5,10)
        deg_4 = random.uniform(5,10)
        deg_5 = random.uniform(5,10)
        deg_values = [deg_1, deg_2, deg_3, deg_4, deg_5]


        da_list = eulers_method(h, 0, 1, start_values, k_values, deg_values)
        p_nfkb_actual = actual(data = params)
        t_vals = np.linspace(0,1,101)
        # print(start_values)
        # print(k_values)
        # print(deg_values)
        # print(len(da_list))
        print(iter)
        if (abs(da_list[100] - norm_y[4]) < tol and abs(da_list[75] - norm_y[3]) < tol
                and abs(da_list[50] - norm_y[2]) < tol and abs(da_list[25] - norm_y[1]) < tol):
            graphData(t_vals, p_nfkb_actual, da_list, norm_t, norm_y)
            file1 = open("start_values.txt", "a")
            file1.write(str(start_values) + "\n")
            file1.close()
            print(start_values)
            file1 = open("k_values.txt", "a")
            file1.write(str(k_values) + "\n")
            file1.close()
            print(k_values)
            file1 = open("deg_values.txt", "a")
            file1.write(str(deg_values) + "\n")
            file1.close()
            print(deg_values)
            iter = 0
            runs+=1
            break
        #if runs == 10 :
        #    break


# parameters found using data fitting
a_1 = -1.1693673371945799
b_1 = 51.41919388017123
c_1 = 5.954712391658841
d_1 = 1.0045788520232413
params = [a_1, b_1, c_1, d_1]
h = .01
tol = .15
main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/




"""
Current Best Params found

    her2_start = 0.02
    erk_start = 9.37
    akt_start = 0.02
    il1_start = 0.01
    ikk_start = 0.01
    ikb_nfkb_start = 11.58
    p_ikb_start = 0.06
    p_nfkb_start = .99
    ikb_start = 2.17
    
     k_1 = 0.01
    k_2 = 1.11
    k_3 = 0.02
    k_4 = 3.54
    k_5 = 0.01
    k_6 = 11.78
    k_7 = 6.0
    k_8 = 0.27
    k_9 = 0.37
    k_10 = 26.47
    
    deg_1 = 6.84
    deg_2 = 71.59
    deg_3 = 6.9
    deg_4 = 6.86
    deg_5 = 5.48
    

"""
