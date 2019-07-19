import numpy as np
from scipy.spatial.transform import Rotation


def arrow(ax, Ts, length=4, display="xyzo", **kargs):
    """Draw an arrow in 3d space

    Arguments:
        ax {matplotlib axes} -- fig = plt.figure(), ax = fig.add_subplot(projection='3d')
        Ts {transform} -- a transform (4x4) or an array of transforms (Nx4x4)

    Keyword Arguments:
        length {int} -- the length of the arrow (default: {4})
        display {str} -- draw which part of the arrow (default: {"xyzo"})
        **kargs:
        origin_color: "red", etc, the color of the origin point
    """
    draw_code = ["ax.quiver(*T[:3, 3],*T[:3, 0], length=length, normalize=True, color=(1, 0, 0, 0.5))",
                 "ax.quiver(*T[:3, 3], *T[:3, 1], length=length, normalize=True, color=(0, 1, 0, 0.5))",
                 "ax.quiver(*T[:3, 3], *T[:3, 2], length=length, normalize=True, color=(0, 0, 1, 0.5))",
                 "ax.plot3D(*T[:3, 3].reshape(3, 1), 'o-', markersize=2*length, color=kargs.get('origin_color', 'red'))"]

    if len(Ts.shape) == 3:
        for T in Ts:
            if display == "xyzo":
                exec("\n".join(draw_code))
                continue
            if 'x' in display.lower():
                exec(draw_code[0])
            if 'y' in display.lower():
                exec(draw_code[1])
            if 'z' in display.lower():
                exec(draw_code[2])
            if 'o' in display.lower():
                exec(draw_code[3])

    elif len(Ts.shape) == 2:
        T = Ts
        exec("".join(draw_code))


def trans(axis, dis):
    AXIS = ('X', 'Y', 'Z')
    axis = str(axis).upper()
    if axis not in AXIS:
        print("%s is unknown axis, should be one of %s" % (axis, AXIS))
        return np.eye(4)
    trans_mat = np.eye(4)
    trans_mat[AXIS.index(axis), 3] = dis
    return trans_mat


if __name__ == "__main__":
    pass
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    T1 = trans("x", 3).dot(trans("y", 3)).dot(
        trans("z", 4))
    T2 = T1.dot(trans("x", -2))
    Ts = np.array([T1, T2])
    fig = plt.figure(figsize=(4, 3))

    ax = fig.gca(projection="3d")
    # ax.quiver(0, 0, 0, 1, 0, 0, length=2, normalize=True, color=(0, 0, 1, 1))
    # ax.quiver(0, 0, 0, 0, 1, 0, length=2, normalize=True)
    # ax.quiver(0, 0, 0, 0, 0, 1, length=2, normalize=True)
    arrow(ax, Ts, 2, origin_color="blue")
    ax.set_xlim(0, 5)
    ax.set_ylim(0, 5)
    ax.set_zlim(0, 5)
    plt.show()
