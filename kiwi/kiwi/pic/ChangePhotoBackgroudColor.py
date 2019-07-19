# -*- coding: utf-8 -*-
"""
by xiaozhen
"""
import cv2
import os


def ConvertPhotoBgColor(path, source_color="red", target_color="white"):
    """convert id photo background color
    
    arguments:
        path {string} -- [input source photo file]
    
    keyword arguments:
        source_color {str} -- ["original background color"] (default: {"red"})
        target_color {str} -- ["desired background color"] (default: {"white"})
    
    raises:
        valueerror: [source_color not in ["red", "white", "blue"]]
        ValueError: [target_color not in ["red", "white", "blue"]]
    """
    img = cv2.imread(path)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    if source_color == "red":
        lower = np.array([120, 180, 100])
        upper = np.array([180, 255, 255])
    elif source_color == "blue":
        lower = np.array([100, 43, 46])
        upper = np.array([124, 255, 255])
    elif source_color == "white":
        lower = np.array([0, 0, 221])
        upper = np.array([180, 30, 255])
    else:
        raise ValueError("Unsupport color")
    mask = cv2.inRange(img_hsv, lower, upper)
    mask = cv2.bitwise_not(mask)
    step = 30
    for i in range(mask.shape[0]-step):
        for j in range(mask.shape[1]-step):
            region = mask[i:i + step, j:j + step]
            if region[0, :].sum() == 0 and region[-1, :].sum() == 0 and region[:, 0].sum() == 0 and region[:, -1].sum() == 0:
                mask[i:i + step, j:j + step] = 0

    if target_color == "blue":
        target = np.zeros_like(img, dtype=np.uint8)
        target[:, :] = np.uint8([255, 0, 0])
    elif target_color == "red":
        target = np.zeros_like(img, dtype=np.uint8)
        target[:, :] = np.uint8([0, 0, 255])
    elif target_color == "white":
        target = np.zeros_like(img, dtype=np.uint8)
        target[:, :] = np.uint8([255, 255, 255])
    else:
        raise ValueError("Unsupport target color")
    bg = cv2.bitwise_and(target, target, mask=cv2.bitwise_not(mask))
    fg = cv2.bitwise_and(img, img, mask=mask)
    dest = cv2.add(bg, fg)
    prefix, suffix = os.path.splitext(path)
    new_file = prefix + "_" + target_color+suffix
    cv2.imwrite(new_file, dest)
    print("File save to {0}".format(new_file))


if __name__ == "__main__":
    path = "./test/lixia.jpg"
    ConvertPhotoBgColor(path, source_color="red", target_color="white")
