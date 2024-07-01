# Evan Funderburg

# this code calculated the order of convergence of Euler's method implemented with our differential equations
# when run it should produce an order that approaches 1
# warning the way it is currently set up it will take over an hour to run, go to bottom and read comments
# if you wish to make it run faster
import sys
import random
import math


# uses the differential equations to determine the next value
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


def eulers_method(step_size, t_start, t_end, start_vals, k_vals, deg_vals):
    steps = int((t_end - t_start) / step_size)

    # adding start values to their respective lists
    stored_erk = [start_vals[1]]
    stored_akt = [start_vals[2]]
    stored_il1 = [start_vals[3]]
    stored_ikk = [start_vals[4]]
    stored_ikb_nfkb = [start_vals[5]]
    stored_p_ikb = [start_vals[6]]
    stored_p_nfkb = [start_vals[7]]
    stored_ikb = [start_vals[8]]

    stored_vals = [[t_start, stored_p_nfkb[0]]]
    # a 2d list where each row contains 2 values the first being the t value and the second being the value of p_nfkb at that t value
    curr = 0
    for i in range(steps):
        # incrementing each parameter for the next step
        stored_erk.append(next_erk(step_size, start_vals[0], stored_akt[i], stored_erk[i], k_vals[0], k_vals[1], deg_vals[0]))
        stored_akt.append(next_akt(step_size, start_vals[0], stored_akt[i], k_vals[2], deg_vals[1]))
        stored_il1.append(next_il1(step_size, stored_erk[i], stored_p_nfkb[i], stored_il1[i], k_vals[3], k_vals[4], deg_vals[2]))
        stored_ikk.append(next_ikk(step_size, stored_akt[i], stored_il1[i], stored_ikk[i], k_vals[5], k_vals[6], deg_vals[3]))
        stored_ikb_nfkb.append(next_ikb_nfkb(step_size, stored_ikk[i], stored_ikb_nfkb[i], stored_ikb[i], stored_p_nfkb[i], k_vals[7], k_vals[8]))
        stored_p_ikb.append(next_p_ikb(step_size, stored_ikk[i], stored_ikb_nfkb[i], stored_p_ikb[i], k_vals[7], deg_vals[4]))
        stored_p_nfkb.append(next_p_nfkb(step_size, stored_ikk[i], stored_ikb_nfkb[i], stored_ikb[i], stored_p_nfkb[i], k_vals[7], k_vals[8]))
        stored_ikb.append(next_ikb(step_size, stored_p_nfkb[i], stored_ikb[i], k_vals[8], k_vals[9]))

        curr = round(curr + step_size, 12)  # gets rid of the lack of precision on floats
        stored_vals.append([curr, stored_p_nfkb[i + 1]])  # add to the 2d list mentioned above
    return stored_vals  # returns 2d list


#calculates global error, E2, otherwise known as RSME or L2 error, over the bounds of the domain
def E2(step_size, t_start, t_end, start_vals, k_vals, deg_vals):
    x_eulers = eulers_method(step_size, t_start, t_end, start_vals, k_vals, deg_vals)  #List of approximated values for x(t_i)
    # print("E2: " + str(step_size))
    max_error = 0
    iter = 0
    # for loop runs through every element in the eulers list
    for i in range(len(x_eulers)):
        while x_eulers[i][0] != actual_list[iter][0]:  # finds where eulers and actual have the same t value
            iter += 1
            if iter >= len(actual_list):
                print("Exit due to error")
                sys.exit()
        # print(x_eulers[i])
        # print(actual_list[iter])
        max_error = max(max_error, abs(x_eulers[i][1] - actual_list[iter][1]))  # calculates max error for the equal t values
    # print(max_error)
    return max_error


def order(step_size, t_start, t_end, start_vals, k_vals, deg_vals):  #Calculates the order, n. Should be approximately 4
    #print(f"h is {h}")
    step_new = float(step_size / 2)  #h_new is the new step-size, which is 1/2 of the original
    e2 = E2(step_new, t_start, t_end, start_vals, k_vals,
            deg_vals)  #Calculates the new error based on the new step-size
    print(f"The max error, e2, with {step_new} is {e2}")
    e1 = E2(step_size, t_start, t_end, start_vals, k_vals,
            deg_vals)  #Calculates the old error based on the orignal step-size
    print(f"The max error, e1, with {step_size} is {e1}")
    ratio = float(e2 / e1)
    print(f"ratio of the error is {ratio}")
    n = math.log2(abs(ratio))  #Calculates the order, n
    return -n


# printing our results for the order of convergence code
def convergence_case_1(step_size, t_start, t_end, start_vals, k_vals, deg_vals):
    print("\nFor max error")
    print(f"Order with h = {step_size} and h/2 = {step_size / 2} is: {order(step_size, t_start, t_end, start_vals, k_vals, deg_vals)}")
    step_size = step_size / 2
    print(f"Order with h = {step_size} and h/2 = {step_size / 2} is: {order(step_size, t_start, t_end, start_vals, k_vals, deg_vals)}")
    step_size = step_size / 2
    print(f"Order with h = {step_size} and h/2 = {step_size / 2} is: {order(step_size, t_start, t_end, start_vals, k_vals, deg_vals)}")
    step_size = step_size / 2
    print(f"Order with h = {step_size} and h/2 = {step_size / 2} is: {order(step_size, t_start, t_end, start_vals, k_vals, deg_vals)}")
    step_size = step_size / 2
    print(f"Order with h = {step_size} and h/2 = {step_size / 2} is: {order(step_size, t_start, t_end, start_vals, k_vals, deg_vals)}")


# randomize these starting parameters
her2_start = 0.02
erk_start = 9.37
akt_start = 0.02
il1_start = 0.01
ikk_start = 0.01
ikb_nfkb_start = 11.58
p_ikb_start = 0.06
p_nfkb_start = .99
ikb_start = 2.17

start_values = [her2_start, erk_start, akt_start, il1_start, ikk_start, ikb_nfkb_start, p_ikb_start, p_nfkb_start, ikb_start]
#                 0,         1            2           3          4        5               6                 7          8
k1 = 0.01
k2 = 1.11
k3 = 0.02
k4 = 3.54
k5 = 0.01
k6 = 11.78
k7 = 6.0
k8 = 0.27
k9 = 0.37
k10 = 26.47
k_values = [k1, k2, k3, k4, k5, k6, k7, k8, k9, k10]

deg_1 = 6.84
deg_2 = 71.59
deg_3 = 6.9
deg_4 = 6.86
deg_5 = 5.48
deg_values = [deg_1, deg_2, deg_3, deg_4, deg_5]

# this code will take over an hour to run with this current step size
# remove two zeros it will run much fast but be less precise
actual_list = eulers_method(.00000001, 0, 1, start_values, k_values, deg_values)
# print("Actual List")
# print(actual_list)
convergence_case_1(.01, 0, 1, start_values, k_values, deg_values)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
