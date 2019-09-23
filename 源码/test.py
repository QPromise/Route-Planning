import math
import numpy as np
def insec(p1, r1, p2, r2):
    x = p1[0]
    y = p1[1]
    R = r1
    a = p2[0]
    b = p2[1]
    S = r2
    d = math.sqrt((abs(a - x)) ** 2 + (abs(b - y)) ** 2)
    if d > (R + S) or d < (abs(R - S)):
        print("Two circles have no intersection")
        return
    elif d == 0 and R == S:
        print("Two circles have same center!")
        return
    else:
        A = (R ** 2 - S ** 2 + d ** 2) / (2 * d)
        h = math.sqrt(R ** 2 - A ** 2)
        x2 = x + A * (a - x) / d
        y2 = y + A * (b - y) / d
        x3 = round(x2 - h * (b - y) / d, 2)
        y3 = round(y2 + h * (a - x) / d, 2)
        x4 = round(x2 + h * (b - y) / d, 2)
        y4 = round(y2 - h * (a - x) / d, 2)
        # print(x3, y3)
        # print(x4, y4)
        c1 = [x3, y3]
        c2 = [x4, y4]
        return c1, c2


P1 = [12, 0]
R1 = 6
P2 = [5, 4]
R2 = 5
C = insec(P1, R1, P2, R2)
C1 = C[0]
C2 = C[1]
print(C1)
print(C2)