# smaller number example of secp256k1-type curve v2.0 | Jackson Jost

import matplotlib.pyplot as plt
from sympy.ntheory import isprime

private_keyint = 112

private_key = hex(private_keyint)

# Constants for the curve y^2 = x^3 + 7 mod p
a = 0
b = 7
p = 7789 #MAKE SURE THIS VALUE IS A SUITABLE PRIME - check plot to see point distribution and test this

# Ensure p is prime
if not isprime(p):
    raise ValueError("p must be prime")

# Function to find a generator point
def find_generator_point():
    for x in range(p):
        y2 = (x**3 + b) % p
        y = pow(y2, (p + 1) // 2, p)
        if (y * y) % p == y2:
            point = {'x': x, 'y': y}
            # Additional checks for point order and suitability coming in the future
            return point
    raise ValueError("No suitable generator point found")

# Find the generator point
g = find_generator_point()
#g = {
#    'x': 101,
#    'y': 3,
#}

# Modular Inverse
def modinv(a, m=p):
    a = a % m if a < 0 else a
    prevy, y = 0, 1
    while a > 1:
        q = m // a
        y, prevy = prevy - q * y, y
        a, m = m % a, a
    return y

# Double
def double(point):
    slope = ((3 * point['x'] ** 2) * modinv(2 * point['y'])) % p
    x = (slope ** 2 - (2 * point['x'])) % p
    y = (slope * (point['x'] - x) - point['y']) % p
    return {'x': x, 'y': y}

# Add
def add(point1, point2):
    if point1 == point2:
        return double(point1)
    slope = ((point1['y'] - point2['y']) * modinv(point1['x'] - point2['x'])) % p
    x = (slope ** 2 - point1['x'] - point2['x']) % p
    y = ((slope * (point1['x'] - x)) - point1['y']) % p
    return {'x': x, 'y': y}

# Multiply
def multiply(k, point=g):
    current = point
    binary = bin(k)[2:]
    for char in binary[1:]:
        current = double(current)
        if char == "1":
            current = add(current, point)
    return current

# Coord
def extract_coordinates(public_key):
    if public_key.startswith('04'):
        x_hex = public_key[2:66]
        y_hex = public_key[66:]
        x = int(x_hex, 16)
        y = int(y_hex, 16)
        return x, y
    else:
        raise ValueError("The provided public key does not appear to be uncompressed")

def plot_curve():
    x_values = []
    y_values = []
    for x in range(p):
        y2 = (x**3 + b) % p
        for y in range(p):
            if (y**2) % p == y2:
                x_values.append(x)
                y_values.append(y)
                break # We found one solution for y, no need to continue checking
    plt.scatter(x_values, y_values, s=5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Elliptic Curve')
    plt.show()


k = int(private_key, 16)
point = multiply(k, g)
x = format(point['x'], '064x')
y = format(point['y'], '064x')
public_key_uncompressed = "04" + x + y
prefix = "02" if (point['y'] % 2 == 0) else "03"
public_key_compressed = prefix + x

print(private_keyint)
#print(public_key_uncompressed)
x, y = extract_coordinates(public_key_uncompressed)
print(f"Generator point: {g}")
print(f"x: {x}\ny: {y}")

plot_curve()
