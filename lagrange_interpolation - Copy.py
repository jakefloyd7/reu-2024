import numpy as np


def lagrange_interpolation(x, y, x_new):
    """
    Perform Lagrange interpolation for given data points.

    Parameters:
    x (list or array): x-coordinates of the given data points
    y (list or array): y-coordinates of the given data points
    x_new (float or array): x-coordinates where interpolation is to be evaluated

    Returns:
    y_new (float or array): interpolated y-coordinates at x_new
    """
    assert len(x) == len(y) == 3, "This function only supports interpolation for three points."

    def basis_polynomial(x, i, x_points):
        b = [(x - x_points[j]) / (x_points[i] - x_points[j]) for j in range(len(x_points)) if j != i]
        return np.prod(b, axis=0)

    y_new = sum(y[i] * basis_polynomial(x_new, i, x) for i in range(len(x)))
    return y_new


# import our data
t = np.array([0, 180, 360, 540, 720])
n = np.array([0.8, 0.81, 0.82, 0.41, 0.22])

''' #normalization of the data - not using yet
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
    norm_t.append(value) '''

new_n = []
new_t = []
for i in range(len(t)-2):
    e
new_



print(f'The interpolated y value at x = {x_new} is {y_new}')