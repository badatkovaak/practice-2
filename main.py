from typing import Callable, List
from attrs import define
from math import fabs
from copy import deepcopy

from matplotlib import pyplot as plt


@define(slots=True)
class MilneMethodInfo:
    f: Callable[[float, float], float]
    ys: List[float]
    x_start: float
    h: float
    n: int = 4


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


def milne_method(info: MilneMethodInfo, k: int):
    for i in range(k):
        y_n_plus_1 = corrector(info, predictor(info))
        info.ys.append(y_n_plus_1)
        info.n += 1

    print(info.ys)

    return info


def f1(x: float, y: float) -> float:
    return x * x * x + y


def f2(x: float, y: float) -> float:
    return (2 - y * y) / (5 * x)


def f3(x: float, y: float) -> float:
    return x + y / x


def f4(x: float) -> float:
    return x * x + 0.001 * x


def main() -> None:
    info1 = MilneMethodInfo(f1, [2, 2.073, 2.452, 3.023], 0, 0.2)
    milne_method(info1, 1)

    info2 = MilneMethodInfo(f2, [1, 1.0049, 1.0097, 1.0143], 4, 0.1)
    milne_method(info2, 1)

    info3 = MilneMethodInfo(f3, [1, 1.0201, 1.0404, 1.0609], 1, 0.01)
    milne_method(info3, 97)

    xs = [info3.x_start + i * info3.h for i in range(101)]
    ys1 = [f4(xs[i]) for i in range(101)]
    diff = [fabs(info3.ys[i] - ys1[i]) for i in range(101)]

    print(max(diff))

    plot1 = plt.plot(xs, info3.ys, ".--b")
    plot2 = plt.plot(deepcopy(xs), ys1, ".--r")
    plt.show()


if __name__ == "__main__":
    main()
