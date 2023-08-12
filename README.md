### Secp256k1-type Curve Example

![output](https://github.com/Stargl0w/easysecp256k1/assets/76890597/0e1d4dcd-fb7c-4bca-9e59-d62751174681)


Interactive Example: *Coming Soon*

This project implements an elliptic curve field that closely resembles the secp256k1 Koblitz curve, known for its use in Bitcoin. It includes essential functionalities to operate over elliptic curve groups, such as point addition and multiplication, and offers visualization of the curve/field using Matplotlib.

#### Class Definition: `EllipticCurve`
`EllipticCurve` encapsulates the curve parameters and provides methods for operations over the curve.

- `__init__(self, a, b, p)`: Constructs an elliptic curve given parameters `a`, `b`, and `p`. Validates the parameters, including the primality of `p`.
- `add(self, P, Q)`: Adds two points `P` and `Q` on the curve using standard elliptic curve addition rules.
- `multiply(self, P, k)`: Multiplies a point `P` by an integer/private key `k`.

#### Additional Functions
- `plot_curve(curve)`: Plots the given elliptic curve using Matplotlib, showing all possible points on the curve.
- `is_prime(n)`: Checks the primality of a given number `n`.

#### Generating a Generator
We iterate through all possible points on the curve to find a generator with the maximum order. The generator and the private key are used to compute the corresponding public key. The script ensures that the private key is within the bounds of the subgroup order.

#### Constants
- `p`: A suitable prime number defining the finite field.
- `a`: The coefficient of the x-term in the curve equation.
- `b`: The constant term in the curve equation.

### Usage
This code can be a helpful starting point for anyone interested in working with elliptic curve cryptography or learning about the mathematical principles underlying secp256k1-type curves.

**Note**: The selected prime `p` must be carefully chosen as suitable for the curve; the code provides comments to guide this selection. Furthermore, the curve parameters must not cause the curve's discriminant to be congruent to zero modulo `p`, as validated in the class constructor.

### Dependencies
- Matplotlib for plotting.
