def calculate_f(p):
    f = -0.083 * pow(p, 3) + 2.75 * pow(p, 2) - 30.667 * p + 118
    return f


factor = 0.77

for price in range(20):
    f = calculate_f(price) * factor
    print(price / 100, '€ | ', f, '%')
