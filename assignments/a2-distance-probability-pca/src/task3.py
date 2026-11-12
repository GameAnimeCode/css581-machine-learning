"""Task 3: PCA simulation on correlated 2D data."""

import matplotlib.pyplot as plt
import numpy as np

from pca import figures_dir, fit_pca, project_pca, reconstruct_pca


def generate_data() -> np.ndarray:
    """3.1: 1,000 reproducible correlated 2D points."""
    rng = np.random.default_rng(581)
    mean = np.array([0.0, 0.0])
    cov = np.array([[2.0, 1.4], [1.4, 1.0]])
    return rng.multivariate_normal(mean, cov, size=1000)


def scatter_2d(points, name: str) -> None:
    """Scatter plot of 2D points with equal axis scaling, saved to figures/."""
    fig, ax = plt.subplots()
    ax.scatter(points[:, 0], points[:, 1], s=8, alpha=0.5)
    ax.axis("equal")
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    fig.savefig(figures_dir() / name, dpi=200, bbox_inches="tight")


def main() -> None:
    # Only write image files, so matplotlib never tries to open a window.
    plt.switch_backend("Agg")

    # 3.1: generate and visualize (first column is x, second is y).
    X = generate_data()
    scatter_2d(X, "task-3-figure-1.png")

    # 3.2: fit PCA (mean, center, covariance, eigendecomposition, sort), then
    # keep the eigenvector for the largest eigenvalue as PC1.
    mean, eigenvalues, eigenvectors, cov = fit_pca(X)
    pc1 = eigenvectors[:, 0]
    pc2 = eigenvectors[:, 1]
    explained_variance_ratio = eigenvalues[0] / eigenvalues.sum()
    pc1_angle = np.degrees(np.arctan2(pc1[1], pc1[0])) % 180

    print(f"Mean:                         {mean}")
    cov_label = "Covariance matrix C:".ljust(30)
    print(cov_label + np.array2string(cov, prefix=cov_label))
    print(f"Eigenvalues:                  {eigenvalues}")
    print(f"PC1 (v1):                     {pc1}")
    print(f"PC2 (v2):                     {pc2}")
    print(f"PC1 angle from x1 axis:       {pc1_angle:.1f} degrees")
    print(f"PC1 explained variance ratio: {explained_variance_ratio:.2%}")
    print(f"Variance discarded (PC2):     {1 - explained_variance_ratio:.2%}")

    # Project every centered point onto PC1: z1 = Xc v1 (one number per point).
    z1 = project_pca(X, mean, eigenvectors, 1).ravel()

    fig, ax = plt.subplots(figsize=(8, 2.5))
    ax.scatter(z1, np.zeros_like(z1), s=8, alpha=0.5)
    ax.set_xlabel("PC1 score $z_1$")
    ax.set_yticks([])
    fig.savefig(figures_dir() / "task-3-figure-2.png", dpi=200, bbox_inches="tight")

    # 3.3: reconstruct from PC1 only: X_hat = z1 v1^T + 1 mu^T. Every
    # reconstructed point lies on the PC1 line through the mean.
    X_hat = reconstruct_pca(z1.reshape(-1, 1), mean, eigenvectors, 1)
    scatter_2d(X_hat, "task-3-figure-3.png")
    print(f"Reconstruction MSE:           {np.mean((X - X_hat) ** 2):.4f}")

    # The dev container has no display, so figures are saved to figures/ above
    # rather than shown in a window.
    plt.close("all")


if __name__ == "__main__":
    main()
