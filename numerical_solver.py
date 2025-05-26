from typing import Callable, List
from math import fabs, floor, ceil
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
    a = (info.x_end - info.x_start) / info.h

    if fabs(a - floor(a)) > 0.00000000000001:
        info.h = (info.x_end - info.x_start) / floor(a)

    k = floor((info.x_end - info.x_start) / info.h)

    for i in range(3):
        if i + 1 >= k:
            return info

        modified_euler(info, 0.0000000001)

    milne_method(info, k - 3)

    if floor(info.h / 0.001) > 1:
        interpolate(info, floor(info.h / 0.001))

    return info


def interpolate(info: MilneMethodInfo, multiply_by: int) -> None:
    new_h = info.h / multiply_by
    xs = [
        info.x_start + new_h * i
        for i in range(round((info.x_end - info.x_start) / new_h) + 1)
    ]

    new_ys = []
    old_xs = [info.x_start + info.h * i for i in range(info.ys.__len__())]

    print(new_h, info.h, len(xs), len(old_xs), multiply_by)
    i_prime = -1

    for i in range(len(xs)):
        if i % multiply_by == 0 or i == (len(xs) - 1):
            i_prime += 1
            new_ys.append(info.ys[i_prime])
            continue

        if fabs(old_xs[i_prime + 1] - old_xs[i_prime]) < 0.00000000000001:
            new_ys.append(new_ys[-1])
            continue

        new_y = (
            (xs[i] - old_xs[i_prime]) / (old_xs[i_prime + 1] - old_xs[i_prime])
        ) * (info.ys[i_prime + 1] - info.ys[i_prime]) + info.ys[i_prime]
        new_ys.append(new_y)

    info.ys = new_ys
    info.h = new_h
    info.n = new_ys.__len__()


def main():
    x_start = float(input("Input start of the interval: "))
    x_end = float(input("Input end of the interval: "))

    if x_end <= x_start:
        print("Invalid interval")
        return

    y_start = float(input("Input start value of y: "))
    h = float(input("Input h: "))

    if h <= 0:
        print("Invalid h")
        return

    info = MilneMethodInfo(lambda x, y: x + y / x, y_start, x_start, x_end, h)
    info = numerically_solve(info)

    xs = [x_start + info.h * i for i in range(info.ys.__len__())]
    ys_correct = [x * x + (y_start / x_start - x_start) * x for x in xs]
    diff = [fabs(y1 - y2) for (y1, y2) in zip(info.ys, ys_correct)]
    print("maxmimum difference = ", max(diff))
    print(len(xs), len(info.ys), info.h, xs[-1])

    # for i in range(info.ys.__len__()):
    #     print(
    #         f"x: {xs[i]:.3f}, y: {info.ys[i]:.8f}, correct: {ys_correct[i]:.8f}, diff: {diff[i]:.8f}"
    #     )

    plt.plot(xs, ys_correct, "r", label="correct")
    plt.plot(xs, info.ys, "b", label="computed")
    plt.plot(xs, diff, "y", label="difference")
    plt.legend(loc="upper left", fontsize=20)
    plt.show()


if __name__ == "__main__":
    main()
