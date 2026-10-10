"""
CSS 581 Assignment 1: Programming Warm-up.

Calculate from scratch, using the Python programming language,
the eigenvalues and eigenvectors associated with the covariance matrix below.
Show your source code and include a screenshot of the results.

Covariance matrix:
    [[0.61655556, 0.61544444],
     [0.61544444, 0.71655556]]

Run from the repository root with the virtual environment active:
    python assignments/<name>/src/main.py
"""


def calculate_determinate(matrix) -> float:
    """
    Calculate the determinant of a 2x2 matrix.
    [[a, b], [c, d]]
    det(A) = ad - bc
    """
    return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]


def calculate_trace(matrix) -> float:
    """
    Calculate the trace of a 2x2 matrix.
    [[a, b], [c, d]]
    trace(A) = a + d
    """
    return matrix[0][0] + matrix[1][1]


def calculate_eigenvalues(matrix) -> list:
    """
    Calculate the eigenvalues of a 2x2 matrix.
    [[a, b], [c, d]]
    Quadratic equation: aλ² + bλ + c = 0
    Quadratic formula:  λ = (-b ± sqrt(b² - 4ac)) / 2a

    For a 2x2 matrix, the characteristic polynomial is:
    det([[a - λ, b], [c, d - λ]]) = 0
    (a - λ)(d - λ) - bc = 0
    aλ² - (a + d)λ + (ad - bc) = 0

    Where:
    A = 1
    B = -(a + d) = -trace(A)
    C = (ad - bc) = det(A)

    ⇒ λ = (trace(A) ± sqrt(trace(A)² - 4 * det(A))) / 2
    """
    trace = calculate_trace(matrix)
    det = calculate_determinate(matrix)
    discriminant = trace**2 - 4 * det

    if discriminant < 0:
        raise ValueError("Matrix has complex eigenvalues.")

    sqrt_discriminant = discriminant**0.5
    eigenvalue1 = (trace + sqrt_discriminant) / 2
    eigenvalue2 = (trace - sqrt_discriminant) / 2

    return [eigenvalue1, eigenvalue2]


def calculate_eigenvectors(matrix, eigenvalues, normalize=False) -> list:
    """
    Calculate the eigenvectors of a 2x2 matrix.
    For each eigenvalue λ, solve (A - λI)v = 0 for v.

    [[a, b], [c, d]]
    The eigenvector corresponding to eigenvalue λ is found by solving:
    [[a - λ, b], [c, d - λ]] * [v1, v2] = [0, 0]

    This leads to a system of linear equations:
    (a - λ)v1 + bv2 = 0
    cv1 + (d - λ)v2 = 0
    """
    a, b = matrix[0]
    c, d = matrix[1]
    eps = 1e-12  # Using epsilon for floating point comparison

    eigenvectors = []
    for i, eigenvalue in enumerate(eigenvalues):
        a_minus_lambda = a - eigenvalue
        d_minus_lambda = d - eigenvalue

        if abs(b) > eps:
            v1 = 1
            v2 = -a_minus_lambda / b
        elif abs(c) > eps:
            v1 = -d_minus_lambda / c
            v2 = 1
        elif abs(a - d) < eps:
            # b = c = 0 & a = d ∴ any vector is an eigenvector
            v1, v2 = (1, 0) if i == 0 else (0, 1)
        elif abs(a_minus_lambda) < abs(d_minus_lambda):
            v1, v2 = 1, 0
        else:
            v1, v2 = 0, 1

        if normalize:
            length = (v1**2 + v2**2) ** 0.5
            v1 /= length
            v2 /= length

        eigenvectors.append([v1, v2])

    return eigenvectors


def main() -> None:
    covariance_matrix = [[0.61655556, 0.61544444], [0.61544444, 0.71655556]]

    try:
        eigenvalues = calculate_eigenvalues(covariance_matrix)
    except ValueError as error:
        print(f"Unable to calculate eigenvalues: {error}")
        return

    eigenvectors = calculate_eigenvectors(covariance_matrix, eigenvalues)
    eigenvectors_norm = calculate_eigenvectors(covariance_matrix, eigenvalues, True)

    print("Covariance Matrix:")
    for row in covariance_matrix:
        print(row)

    print("\nEigenvalues:")
    for i, eigenvalue in enumerate(eigenvalues):
        print(f"Eigenvalue {i + 1}: {eigenvalue}")

    print("\nEigenvectors:")
    for i, eigenvector in enumerate(eigenvectors):
        print(f"Eigenvector {i + 1}: {eigenvector}")

    print("\nEigenvectors (normalized):")
    for i, eigenvector in enumerate(eigenvectors_norm):
        print(f"Eigenvector {i + 1}: {eigenvector}")


if __name__ == "__main__":
    main()
