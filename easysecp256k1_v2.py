import matplotlib.pyplot as plt

# Constants for the curve y^2 = x^3 + 7 mod p
# points in the corners mean that your p is not sutible, or if you receive an error - see quadratic residue property in the finite field
a = 0
b = 7
p = 599 #MAKE SURE THIS VALUE IS A SUITABLE PRIME - check plot to see point distribution and test this

# Modular Inverse
def modinv(a, m=p):
    a = a % m if a < 0 else a
    prevy, y = 0, 1
    while a > 1:
        q = m // a
        y, prevy = prevy - q * y, y
        a, m = m % a, a
    return y

def plot_curve(curve):
    x_values = []
    y_values = []
    for x in range(curve.p):
        for y_sq in [(x**3 + curve.a * x + curve.b) % curve.p]:
            y = pow(y_sq, (curve.p + 1) // 4, curve.p)
            if (y * y - y_sq) % curve.p == 0:
                for y_val in {y, curve.p - y}:
                    x_values.append(x)
                    y_values.append(y_val)

    plt.scatter(x_values, y_values, s=1)
    plt.title('Elliptic Curve Field')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()

class EllipticCurve:
    def __init__(self, a, b, p):
        self.a = a
        self.b = b
        self.p = p
        self.G, self.M = self.find_generator()

    def find_generator(self):
        max_order = 0
        generator = None
        for x in range(self.p):
            for y_sq in [(x**3 + self.a * x + self.b) % self.p]:
                # Check if y_sq is a quadratic residue
                if pow(y_sq, (self.p - 1) // 2, self.p) != 1:
                    continue
                    
                y = pow(y_sq, (self.p+1)//4, self.p)
                # Debugging print statement
                #print(f"x: {x}, y_sq: {y_sq}, y: {y}")
                
                if (y*y - y_sq) % self.p == 0:
                    for y_val in {y, self.p-y}:
                        point = {'x': x, 'y': y_val}
                        order = 1
                        current_point = point
                        iteration = 0  # counter to avoid infinite loop
                        while self.add(current_point, point) is not None and iteration < 100:
                            current_point = self.add(current_point, point)
                            order += 1
                            iteration += 1
                            # Debugging print statement
                            #print(f"Current point: {current_point}, Point: {point}")
                        
                        if iteration == 100000:
                            print("Reached max iterations, potential infinite loop")
                            return None
                        
                        if order > max_order:
                            max_order = order
                            generator = point
        return generator, max_order

    def double(self, point):
        slope = ((3 * point['x'] ** 2 + a) * modinv(2 * point['y'])) % p
        x = (slope ** 2 - 2 * point['x']) % p
        y = (slope * (point['x'] - x) - point['y']) % p
        return {'x': x, 'y': y}

    def add(self, point1, point2):
        if point1 == point2:
            return self.double(point1)
        slope = ((point1['y'] - point2['y']) * modinv(point1['x'] - point2['x'])) % p
        x = (slope ** 2 - point1['x'] - point2['x']) % p
        y = ((slope * (point1['x'] - x)) - point1['y']) % p
        return {'x': x, 'y': y}

    def multiply(self, k, point):
        current = point
        binary = bin(k)[2:]
        for char in binary[1:]:
            current = self.double(current)
            if char == "1":
                current = self.add(current, point)
        return current

curve = EllipticCurve(a, b, p)
private_key = 97
G = curve.G # Set Generator Point
max_order = curve.M
public_key = curve.multiply(private_key, G)

# Ensure the private key modulo the order of the subgroup
if private_key <= max_order:
    print(f"Private key: {private_key}")
    print(f"Public key: {public_key}")
    print(f"The generator is {G} with order {max_order}.")
else:
    print(f"This private key is outside of group order {max_order}")

plot_curve(curve)
