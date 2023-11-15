import matplotlib.pyplot as plt

#Curve Parameters
a = 0
b = 7

# Prime modulus 
p = 701 # MAKE SURE THIS VALUE IS A SUITABLE PRIME - see quadratic residue property in the finite field

private_key = "321"

# Check if a point is on the curve
def is_on_curve(x, y):
    return (y * y) % p == (x * x * x + a * x + b) % p

# Extended Euclidean Algorithm
def modinv(a, m=p):
    if a < 0:
        a = a % m
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    return x1 + m0 if x1 < 0 else x1

def double(point):
    slope = (3 * point['x']**2 * modinv(2 * point['y'])) % p
    x = (slope**2 - 2 * point['x']) % p
    y = (slope * (point['x'] - x) - point['y']) % p
    return {'x': x, 'y': y}

def add(point1, point2):
    if point1 == point2:
        return double(point1)
    slope = ((point1['y'] - point2['y']) * modinv(point1['x'] - point2['x'])) % p
    x = (slope**2 - point1['x'] - point2['x']) % p
    y = (slope * (point1['x'] - x) - point1['y']) % p
    return {'x': x, 'y': y}

def plot_curve():
    plt.figure(figsize=(10, 10))
    for x in range(p):
        for y in range(p):
            if is_on_curve(x, y):
                plt.scatter(x, y, c='black', marker='x', s=10)

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def get_curve_points():
    curve_points = []
    for x in range(p):
        for y in range(p):
            if is_on_curve(x, y):
                curve_points.append((x, y))
    return curve_points

def order_of_point(point, curve_points):
    if point == (None, None):
        return 1  # Order of the point at infinity is always 1

    n = 1
    current_point = {'x': point['x'], 'y': point['y']}
    while True:
        n += 1
        current_point = add(current_point, {'x': point['x'], 'y': point['y']})
        if (current_point['x'], current_point['y']) == (None, None):
            break
    return n

def calculate_generator():
    for x in reversed(range(p)):
        for y_sq in [(x**3 + a * x + b) % p]:
            y = pow(y_sq, (p + 1) // 4, p)
            if (y * y - y_sq) % p == 0:
                for y_val in reversed(sorted({y, p - y})):
                    point = {'x': x, 'y': y_val}
                    order = 1
                    current_point = point
                    while True:
                        current_point = add(current_point, point)
                        if current_point['x'] is None:
                            break
                        order += 1
                        if order == p:
                            return point, order


g, max_order = calculate_generator()

print(f"The generator is {g} with order {max_order}.")

def multiply(k, point=g):
    current = point
    binary = bin(k)[2:]
    for char in binary[1:]:
        current = double(current)
        if char == '1':
            current = add(current, point)
    return current

k = int(private_key)
print(f"Private Key is {k}")
print(f"The generated point is {point['x'], point['y']}")

point = multiply(k, g)

plot_curve()

plt.scatter(point['x'], point['y'], c='red', marker='x', s=10)
plt.title('All Possible Points and Point Generated')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(False)
plt.show()
