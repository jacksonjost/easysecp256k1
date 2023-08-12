# smaller number example of secp256k1-type curve | Jackson Jost
import matplotlib.pyplot as plt

def modular_sqrt(a, p):
    if pow(a, (p - 1) // 2, p) != 1:
        return None
    return pow(a, (p + 1) // 4, p)

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

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

class EllipticCurve:
    def __init__(self, a, b, p):
        if not is_prime(p):
            raise ValueError("p must be a prime number")
        if (4 * a**3 + 27 * b**2) % p == 0:
            raise ValueError("Invalid curve parameters: 4*a^3 + 27*b^2 must not be congruent to 0 mod p")
        self.a = a
        self.b = b
        self.p = p

    def add(self, P, Q):
        if P is None or Q is None:
            return P if Q is None else Q
        x_p, y_p = P
        x_q, y_q = Q
        if (x_p, y_p) == (x_q, -y_q % self.p):
            return None
        if P == Q:
            denom = (2 * y_p) % self.p
            if denom == 0:
                return None
            inverse_denom = pow(denom, -1, self.p)
            lamb = (3 * x_p**2 + self.a) * inverse_denom % self.p
        else:
            denom = (x_q - x_p) % self.p
            if denom == 0:
                return None
            inverse_denom = pow(denom, -1, self.p)
            lamb = (y_q - y_p) * inverse_denom % self.p

        x_r = (lamb**2 - x_p - x_q) % self.p
        y_r = (lamb * (x_p - x_r) - y_p) % self.p

        return x_r, y_r

    def multiply(self, P, k):
        R = None
        for i in range(k.bit_length()):
            if R is None:
                R = P
            if (k >> i) & 1:
                R = self.add(R, P)
            P = self.add(P, P)
        return R

# Iterate through all possible points
max_order = 0
generator = None
# Constants for the curve y^2 = x^3 + 7 mod p
# points in the corners mean that your p is not sutible - see quadratic residue property in the finite field
p = 419 #MAKE SURE THIS VALUE IS A SUITABLE PRIME - check plot to see point distribution and test this
a = 0
b = 7
curve = EllipticCurve(a, b, p)

for x in range(p):
    y_sq = (x**3 + b) % p
    y = modular_sqrt(y_sq, p)
    if y is not None:
        for y_val in {y, p-y}:
            point = (x, y_val)
            order = 1
            current_point = point
            while curve.add(current_point, point) is not None:
                current_point = curve.add(current_point, point)
                order += 1
            if order > max_order:
                max_order = order
                generator = point

G = generator  # Set the generator after finding it
print(f"The generator is {generator} with order {max_order}.")

private_key = 223

# Ensure the private key modulo the order of the subgroup
if private_key <= max_order:
    private_key = private_key
    public_key = curve.multiply(G, private_key)
    print(f"Private key: {private_key}")
    print(f"Public key: {public_key}")
else:
    print("This private key is outside of group order")

plot_curve(curve)
