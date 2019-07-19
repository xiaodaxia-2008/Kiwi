import numpy as np
from IPython import embed


def Intersection(p0, v0, p1, v1):
    # only for dimension 3
    if np.linalg.norm(np.cross(v0, v1)) == 0:
        print("parel lines")
        return
    direct_p01 = p1 - p0
    vec_s1 = np.cross(v0, v1)
    vec_s2 = np.cross(direct_p01, v1)
    if np.abs(np.dot(direct_p01, vec_s1)) > 1e-5:
        print("line2 not co-plannar")
        return
    #embed()
    ratio = vec_s2.dot(vec_s1) / np.linalg.norm(vec_s1, ord=2)
    intersection = p0 + ratio * v0
    return intersection

def Intersection2Lines(p0, t0, p1, t1):
    # possible for high dimensions
    T = np.c_[t0.reshape(-1, 1), t1.reshape(-1, 1)]
    c0, c1 = np.linalg.pinv(T).dot(p0 - p1)
    intersection = p1 + c1*t1
    return intersection

if __name__ == "__main__":
    p0 = np.array([2, 0, 0, 0])
    v0 = np.array([1, 1, 0, 0])
    p1 = np.array([0, 1, 0, 0])
    v1 = np.array([0, 1, 0, 0])
    #print(Intersection(p0, v0, p1, v1))
    print(Intersection2Lines(p0, v0, p1, v1))
