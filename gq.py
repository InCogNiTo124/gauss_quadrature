import math
from functools import partial
from weights import ORDER_WEIGHTS


def _gauss_quad_n(f, boundary_list, order_list):
    a, b = boundary_list[0]
    a = a()
    b = b()
    h = (b - a) / 2
    m = (b + a) / 2
    order = order_list[0]
    weights = ORDER_WEIGHTS[order]
    if len(boundary_list) == 1:
        return h * math.fsum(weights[x] * f(h * x + m) for x in weights)
    else:
        results = []
        for x, w in weights.items():
            x = h * x + m
            new_boundary_list = [
                (partial(a, x), partial(b, x)) for (a, b) in boundary_list[1:]
            ]
            results.append(
                w * _gauss_quad_n(partial(f, x), new_boundary_list, order_list[1:])
            )
        return h * math.fsum(results)


def _boundary(x):
    if callable(x):
        return x
    if isinstance(x, (int, float)):
        # little trick
        # this now accepts any number of arguments
        # and returns a constant
        return lambda *args: x
    else:
        raise TypeError("boundary must be callable or number: {}".format(repr(x)))


def gauss_quad(f, boundary_list, order=21):
    new_boundary_list = [(_boundary(a), _boundary(b)) for (a, b) in boundary_list]
    if isinstance(order, int):
        if order <= 1:
            raise ValueError(
                "order must be positive integer >= 2: {}".format(repr(order))
            )
        order_list = [order] * len(boundary_list)
    elif isinstance(order, (list, tuple)):
        assert len(order) == len(
            boundary_list
        ), "Order list must have same length as boundary list"
        order_list = list(order)
    else:
        raise TypeError("order must be int or list or tuple: {}".format(repr(order)))

    return _gauss_quad_n(f, new_boundary_list, order_list)


if __name__ == "__main__":

    def ff(*args):
        # calculates entropy of a probability distribution
        args += (1 - math.fsum(args),)
        return math.fsum(0 if x <= 0 else -x * math.log(x) for x in args)

    print(gauss_quad(ff, [(0, 1)]))
    print(gauss_quad(ff, [(0, 1), (0, lambda x: 1 - x)]))
    print(gauss_quad(ff, [(0, 1), (0, lambda x: 1 - x), (0, lambda x, y: 1 - x - y)]))
