import numpy as np 
print(f"{20*"="} GRAM SCHMIDTH {20*"="}")


def gramm_shmidt(V):
    W = np.zeros((3, 3), dtype=float)
    n = V.shape[1]
    for i in range(n):
        vi = V[:,i]
        projection = np.zeros_like(vi)
        for j in range(i):
            wj = W[:,j]
            dot_product = np.dot(vi, wj)
            projection += dot_product * wj
        ui = vi - projection
        norm_ui = np.linalg.norm(ui)
        if norm_ui > 1e-10:
            W[:,i]= ui/norm_ui
        else:
            W[:,i]= ui
    return W

V_input = np.array([[1, 1, 1], 
                    [0, 1, 1], 
                    [0, 0, 1]], dtype=float).T
result = gramm_shmidt(V_input)
print(np.round(result, 10))