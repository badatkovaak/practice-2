from typing import Callable, List
from math import fabs
from copy import deepcopy
from matplotlib import pyplot as plt


class MilneMethodInfo:
    f: Callable[[float, float], float]
    ys: List[float]
    x_start: float
    x_end: float
    h: float
    n: int = 1

    def __init__(self, f, ys, x_start, x_end, h, n=None):
        self.f = f
        self.ys = ys
        self.x_start = x_start
        self.x_end = x_end
        self.h = h

        if n is not None:
            self.n = n


def modified_euler(info: MilneMethodInfo, accuracy: float) -> None:
    y_0 = info.ys[info.n - 1]
    h = info.h
    f = info.f
    x_0 = info.x_start + (info.n - 1) * h
    y = y_0 + h * info.f(x_0, y_0)
    y_prev = y_0

    # print(y_0, y_prev, y, x_0)

    while True:
        y_prev = y
        y = y_0 + h / 2 * (f(x_0, y_0) + f(x_0 + h, y))

        if fabs(y - y_prev) < accuracy / 10:
            break

    info.ys.append(y)
    info.n += 1

    return


def predictor(info: MilneMethodInfo) -> float:
    n = len(info.ys) - 1

    assert n + 1 == info.n

    y_primes = [
        info.f(info.x_start + (info.n - 3 + i) * info.h, info.ys[n - 2 + i])
        for i in range(3)
    ]

    # print("predictor primes", y_primes)

    result = info.ys[n - 3] + 4 * info.h / 3 * (
        2 * y_primes[0] - y_primes[1] + 2 * y_primes[2]
    )

    # print("predictor result is ", result)

    return result


def corrector(info: MilneMethodInfo, y_n_plus_1: float) -> float:
    n = len(info.ys) - 1

    assert n + 1 == info.n

    y_primes = [
        info.f(info.x_start + (info.n - 3 + i) * info.h, info.ys[n - 2 + i])
        for i in range(3)
    ]

    y_n_plus_1_prime = info.f(info.x_start + info.n * info.h, y_n_plus_1)

    # print("corrector primes", y_primes)

    result = info.ys[n - 1] + info.h / 3 * (
        y_primes[1] + 4 * y_primes[2] + y_n_plus_1_prime
    )

    # print("corrector result is ", result)

    return result


def milne_method(info: MilneMethodInfo, k: int) -> MilneMethodInfo:
    for _ in range(k):
        y_n_plus_1 = corrector(info, predictor(info))
        info.ys.append(y_n_plus_1)
        info.n += 1

    # print(info.ys)

    return info


# def numerically_solve(
#     f: Callable[[float, float], float], x_start: float, y_start: float, h: float, n: int
# ) -> MilneMethodInfo:
def numerically_solve(info: MilneMethodInfo) -> MilneMethodInfo:
    # info = MilneMethodInfo(f, [y_start], x_start, h, 1)
    k = round((info.x_end - info.x_start) / info.h)

    for _ in range(3):
        modified_euler(info, 0.0000001)

    # print(info.ys)

    milne_method(info, k - 3)
    return info


def numerically_solve_raw(
    f: Callable[[float, float], float],
    x_start: float,
    x_end: float,
    y_start: float,
    h: float,
):
    return numerically_solve(MilneMethodInfo(f, [y_start], x_start, x_end, h, 1))


def main() -> None:
    # info1 = numerically_solve(lambda x,y: x*x*x + y, 0, 2, 0.2, 10)
    # info1 = MilneMethodInfo(f1, [2, 2.073, 2.452, 3.023], 0, 0.2)
    # milne_method(info1, 1)

    # info2 = numerically_solve(lambda x,y: (2 - y*y)/(5*x), 4, 1, 0.1, 10)
    # info2 = MilneMethodInfo(f2, [1, 1.0049, 1.0097, 1.0143], 4, 0.1)
    # milne_method(info2, 1)

    info3 = numerically_solve_raw(lambda x, y: x + y / x, 1, 1, 0.01, 100)
    # info3 = MilneMethodInfo(f3, [1, 1.0201, 1.0404, 1.0609], 1, 0.01)
    # milne_method(info3, 97)
    # info3 = numerically_solve(lambda x,y: x + y, 0, 1, 0.1, 5)

    # print(info1.ys)
    # print(info2.ys)
    # print(info3.ys)

    # xs = [info3.x_start + i * info3.h for i in range(101)]
    # ys1 = [f4(xs[i]) for i in range(101)]
    # diff = [fabs(info3.ys[i] - ys1[i]) for i in range(101)]

    # print("max diff is - ", max(diff))
    # print("max of ys is - ", max(info3.ys))

    # fig1 = plt.figure()
    # plot1 = plt.plot(xs, info3.ys, ".--b")
    # plot2 = plt.plot(deepcopy(xs), ys1, ".--r")
    # plt.figure
    # plt.savefig("figure.png")
    # plt.show()


if __name__ == "__main__":
    main()
