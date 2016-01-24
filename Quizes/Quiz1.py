import math


def polynomial(x=0.0) -> float:
    """
    Returns the following polynomial given x.
    f(x) = -5 x**5 + 69 x**2 - 47

     :rtype: float
     :param x: float
    """

    return -5 * x ** 5 + 69 * x ** 2 - 47


def future_value(present_value, annual_rate, periods_per_year, years):
    """
    Returns the following polynomial given x.
    FV = PV (1+rate)^periods

     :rtype: float
     :param present_value:      float, the value today
     :param annual_rate:        float, the interest compounded yearly
     :param periods_per_year:   integer, e.g., 4, 12, 365
     :param years:              integer
    """
    rate_per_period = annual_rate / periods_per_year
    periods = periods_per_year * years

    # Put your code here.
    return present_value * (1 + rate_per_period) ** periods


def polygon(number_sides, length_side) -> float:
    """
    Returns the area of polynomial with n sides and length s.
    1/4 * n * s^2 / tan(π/n)

     :rtype: float
     :param number_sides:   int
     :param length_side:    float
    """
    return 0.25 * number_sides * length_side ** 2 / math.tan(math.pi / number_sides)


def max_of_2(a, b):
    if a > b:
        return a
    else:
        return b


def max_of_3(a, b, c):
    return max_of_2(a, max_of_2(b, c))


def project_to_distance(point_x, point_y, distance) -> None:
    """

    :rtype: None
    :param point_x:
    :param point_y:
    :param distance:
    """
    dist_to_origin = math.sqrt(point_x ** 2 + point_y ** 2)
    scale = distance / dist_to_origin
    print(point_x * scale, point_y * scale)
    return 


for i in [0, 1, 2, 3]:
    print(polynomial(i))

print(future_value(500, .04, 10, 10))
print("$1000 at 2% compounded daily for 3 years yields $", future_value(1000, .02, 365, 3))

print(polygon(5, 7))
print(polygon(7, 3))

project_to_distance(2, 7, 4)
