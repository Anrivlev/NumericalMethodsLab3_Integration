import numpy as np
import matplotlib.pyplot as plt


def func(x):
    return (x**5) * np.sin(x)


def integral_of_func(x):
    c1 = 5 * (x**4 - 12 * x**2 + 24)
    c2 = - x * (x**4 - 20 * x**2 + 120)
    return c1 * np.sin(x) + c2 * np.cos(x)


def rectangle(a, b, f):
    return (b - a) * f(a)


def trapezoid(a, b, f):
    return (b - a) * (f(a) + f(b)) / 2


def simpsons(a, b, f):
    return (b - a) * (f(a) + 4 * f((a + b) / 2) + f(b)) / 6


def three_eights(a, b, f):
    return (b - a) * (f(a) + 3 * f((2 * a + b) / 3) + 3 * f((a + 2 * b) / 3) + f(b)) / 8


def gaussian5(a, b, f):
    left = f(((a + b) / 2) - (b - a) / (2 * np.sqrt(3)))
    right = f(((a + b) / 2) + (b - a) / (2 * np.sqrt(3)))
    return (b - a) * (left + right) / 2


def main():
    a = -1
    b = 1
    hmin = 0.01
    hmax = 0.1
    hstep = 0.001
    hrange = np.arange(hmin, hmax, hstep)

    integral = dict()
    error = dict()
    error[rectangle] = np.zeros(len(hrange))
    error[trapezoid] = np.zeros(len(hrange))
    error[simpsons] = np.zeros(len(hrange))
    error[three_eights] = np.zeros(len(hrange))
    #error[gaussian5] = np.zeros(len(hrange))

    for k in range(len(hrange)):
        h = hrange[k]
        xrange = np.arange(a, b + h, h)

        integral[rectangle] = 0
        integral[trapezoid] = 0
        integral[simpsons] = 0
        integral[three_eights] = 0
        #integral[gaussian5] = 0

        for i in range(1, len(xrange)):
            for key in integral:
                truevalue_local = integral_of_func(xrange[i]) - integral_of_func(xrange[i - 1])
                integral_local = key(xrange[i - 1], xrange[i], func)
                integral[key] += integral_local
                error[key][k] = max(error[key][k], abs(truevalue_local - integral_local))

    hrange = np.log(hrange)
    for key in error:
        error[key] = np.log(error[key])

    i = 0
    for key in error:
        i += 1
        plt.subplot(1, len(error), i)
        plt.title(key.__name__)
        plt.xlabel("log(h)")
        plt.ylabel("log(max(|ΔFk|))")
        plt.grid()
        plt.plot(hrange, error[key], color='k', label='Абсолютная погрешность')
        plt.legend()

    gradient = dict()
    for key in error:
        gradient[key] = (error[key][-1] - error[key][0]) / (hrange[-1] - hrange[0])

    for key in gradient:
        print(key.__name__, ":", gradient[key])

    print()
    print("How much three-eights rule is better than Simpson's:")
    print(np.average(abs(np.exp(error[simpsons]) / np.exp(error[three_eights]))))

    plt.show()


main()
