### Secp256k1-type Curve Example

![output](https://raw.githubusercontent.com/jacksonjost/easysecp256k1/main/output2.PNG)

Interactive Application: [Download Available](https://github.com/jacksonjost/easysecp256k1/releases/tag/Windows)

This project implements an elliptic curve field that closely resembles the secp256k1 Koblitz curve, known for its use in Bitcoin. It includes essential functionalities to operate over elliptic curve groups, such as point addition and multiplication, and offers visualization of the curve/field using Matplotlib.

## Core Functions
- `is_on_curve(x, y)`: Checks if a given point `(x, y)` lies on the curve.
- `modinv(a, m)`: Computes the modular multiplicative inverse of `a` modulo `m`.
- `double(point)`: Applies the point doubling operation.
- `add(point1, point2)`: Adds two points on the elliptic curve using the chord-and-tangent rule.
- `plot_curve()`: Visualizes the elliptic curve, marking all valid points.
- `is_prime(n)`: Ensures the validity of the finite field by verifying the primality of `n`.
- `multiply(k, point=g)`: Performs scalar multiplication of a point `k` times.

#### Generating a Generator
We iterate through all possible points on the curve to find a generator with the maximum order. The generator and the private key are used to compute the corresponding public key.
- `get_curve_points()`: Retrieves all points on the curve.
- `order_of_point(point, curve_points)`: Determines the order of a given point on the curve.
- `calculate_generator()`: Finds a generator point with maximal order for the curve.

## Curve Parameters
- `a`, `b`: Define the shape of the curve.
- `p`: A prime number that defines the finite field.
- `private_key`: Represents the private key in ECC.

#### Constants
- `p`: A suitable prime number defining the finite field.
- `a`: The coefficient of the x-term in the curve equation.
- `b`: The constant term in the curve equation.

### Usage
This code can be a helpful starting point for anyone interested in working with elliptic curve cryptography or learning about the mathematical principles underlying secp256k1-type curves.

**Note**: The selected prime `p` must be carefully chosen as suitable for the curve; the code provides comments to guide this selection. Furthermore, the curve parameters must not cause the curve's discriminant to be congruent to zero modulo `p`, as validated.

### Dependencies
- Matplotlib for plotting.

**WARNING**: This project is not suitable for, or designed for, cryptographic use.

**Comment**: The project opted against using Schoof's algorithm for calculating the order of an elliptic curve. Instead, we opted for a straightforward iterative method that, while more accessible and clear for our purposes, lacks the computational efficiency and scalability essential for large prime fields. The method presented should be suitable for visualization and understanding but is not appropriate for cryptographic/production use.
