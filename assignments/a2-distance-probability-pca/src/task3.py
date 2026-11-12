"""Task 3: PCA simulation on correlated 2D data."""

import matplotlib.pyplot as plt
import numpy as np

from pca import fit_pca, project_pca, reconstruct_pca  # noqa: F401


def generate_data() -> np.ndarray:
    """3.1: 1,000 reproducible correlated 2D points."""
    rng = np.random.default_rng(581)
    mean = np.array([0.0, 0.0])
    cov = np.array([[2.0, 1.4], [1.4, 1.0]])
    return rng.multivariate_normal(mean, cov, size=1000)


def main() -> None:
    X = generate_data()

    # TODO 3.1: Figure 1, scatter of x1 vs x2 (equal axis scaling)
    # TODO 3.2: fit_pca, report both eigenvalues and PC1 explained variance ratio,
    #           project onto PC1, Figure 2 (PC1 scores vs zero)
    # TODO 3.3: reconstruct from PC1, Figure 3 (reconstructed points in 2D)
    _ = (X, plt)


if __name__ == "__main__":
    main()
