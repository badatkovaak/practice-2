from typing import Callable, List
from math import fabs
from matplotlib import pyplot as plt


class MilneMethodInfo:
    f: Callable[[float, float], float]
    ys: List[float]
    x_start: float
    x_end: float
    h: float
    n: int = 1

    def __init__(
        self,
        f: Callable[[float, float], float],
        y_start: float,
        x_start: float,
        x_end: float,
        h: float,
    ):
        self.f = f
        self.ys = [y_start]
        self.x_start = x_start
        self.x_end = x_end

        if x_end < x_start:
            raise Exception()

        self.h = h

        if h <= 0:
            raise Exception()

    def __repr__(self):
        return f"f: {self.f}, x_start: {self.x_start}, x_end: {self.x_end}, h: {self.h}, n: {self.n}\nys: {self.ys}\n"


def modified_euler(info: MilneMethodInfo, accuracy: float) -> None:
    y_0 = info.ys[info.n - 1]
    h = info.h
    f = info.f
    x_0 = info.x_start + (info.n - 1) * h
    y = y_0 + h * info.f(x_0, y_0)
    y_prev = y_0

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

    result = info.ys[n - 3] + 4 * info.h / 3 * (
        2 * y_primes[0] - y_primes[1] + 2 * y_primes[2]
    )

    return result


def corrector(info: MilneMethodInfo, y_n_plus_1: float) -> float:
    n = len(info.ys) - 1

    assert n + 1 == info.n

    y_primes = [
        info.f(info.x_start + (info.n - 3 + i) * info.h, info.ys[n - 2 + i])
        for i in range(3)
    ]

    y_n_plus_1_prime = info.f(info.x_start + info.n * info.h, y_n_plus_1)

    result = info.ys[n - 1] + info.h / 3 * (
        y_primes[1] + 4 * y_primes[2] + y_n_plus_1_prime
    )

    return result


def milne_method(info: MilneMethodInfo, k: int) -> MilneMethodInfo:
    for _ in range(k):
        y_n_plus_1 = corrector(info, predictor(info))
        info.ys.append(y_n_plus_1)
        info.n += 1

    return info


def numerically_solve(info: MilneMethodInfo) -> MilneMethodInfo:
    k = round((info.x_end - info.x_start) / info.h)

    for _ in range(3):
        modified_euler(info, 0.0000001)

    milne_method(info, k - 3)
    return info


def main():
    x_start = float(input("Input start of the interval:"))
    x_end = float(input("Input end of the interval:"))

    if x_end <= x_start:
        print("Invalid interval")
        return

    y_start = float(input("Input start value of y:"))
    h = float(input("Input h:"))

    if h <= 0:
        print("Invalid h")
        return

    info = MilneMethodInfo(lambda x, y: x + y / x, y_start, x_start, x_end, h)
    info = numerically_solve(info)

    xs = [x_start + h * i for i in range(info.ys.__len__())]
    ys_correct = [x * x + (y_start / x_start - x_start) * x for x in xs]
    diff = [fabs(y1 - y2) for (y1, y2) in zip(ys_correct, info.ys)]
    print("maxmimum difference = ", max(diff))

    plt.plot(xs, info.ys, "b")
    plt.plot(xs, ys_correct, "r")
    plt.plot(xs, diff, "y")
    plt.show()


if __name__ == "__main__":
    main()
