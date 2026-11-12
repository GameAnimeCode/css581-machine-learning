"""
Task 4: PCA on USPS handwritten digits.

Run with USPS.npz in the working directory, or fall back to the copy at
data/USPS.npz in the assignment folder.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pca import figures_dir, fit_pca, mse, project_pca, reconstruct_pca

P_VALUES = [10, 50, 100, 150, 200]
DATA_PATHS = [
    Path("USPS.npz"),
    Path(__file__).resolve().parent.parent / "data" / "USPS.npz",
]


def load_usps():
    """4.1: load images (3000 x 256) and labels (3000,)."""
    path = next((p for p in DATA_PATHS if p.exists()), None)
    if path is None:
        raise FileNotFoundError("USPS.npz not found in the working directory")

    data = np.load(path, allow_pickle=False)
    A = data["images"].astype(float)  # shape: (3000, 256)
    labels = data["labels"].ravel()  # shape: (3000,)

    return A, labels


def plot_comparison(A, labels, reconstructions) -> None:
    """4.3: original plus each reconstruction for the last two images,
    saved to figures/. One row per image, one column per version."""
    fig, axes = plt.subplots(nrows=2, ncols=len(P_VALUES) + 1, figsize=(15, 5))

    # Index -2 and -1 are the last two images in the dataset.
    for row, index in enumerate([-2, -1]):
        axes[row, 0].imshow(A[index].reshape(16, 16), cmap="gray")
        axes[row, 0].set_title(f"Original (digit {labels[index]})")

        for col, p in enumerate(P_VALUES, start=1):
            image = reconstructions[p][index].reshape(16, 16)
            axes[row, col].imshow(image, cmap="gray")
            axes[row, col].set_title(f"p = {p}")

    for ax in axes.ravel():
        ax.axis("off")

    fig.tight_layout()
    fig.savefig(figures_dir() / "task-4-figure-1.png", dpi=200, bbox_inches="tight")


def plot_mse(mse_values) -> None:
    """4.4: line plot of reconstruction error versus p, saved to figures/."""
    fig, ax = plt.subplots()
    ax.plot(P_VALUES, mse_values, marker="o")
    ax.set_xlabel("Number of principal components $p$")
    ax.set_ylabel("Mean squared reconstruction error")
    fig.savefig(figures_dir() / "task-4-figure-2.png", dpi=200, bbox_inches="tight")


def main() -> None:
    # Only write image files, so matplotlib never tries to open a window.
    plt.switch_backend("Agg")

    # 4.1: load, then fit PCA on the raw pixels. fit_pca subtracts the mean image
    # (feature-wise mean over all 3,000 samples) and does not standardize each pixel.
    A, labels = load_usps()
    std_low, std_high = A.std(axis=0).min(), A.std(axis=0).max()

    print(f"Images:                       {A.shape}")
    print(f"Labels:                       {labels.shape}")
    print(f"Pixel value range:            {A.min():.1f} to {A.max():.1f}")
    print(f"Mean image pixel value:       {A.mean():.4f}")
    print(f"Per-pixel std range:          {std_low:.4f} to {std_high:.4f}")
    print(f"Labels of last two images:    {labels[-2]} and {labels[-1]}")

    # 4.2: fit PCA, then project and reconstruct the whole dataset for each p.
    mean, eigenvalues, eigenvectors, cov = fit_pca(A)
    reconstructions = {}

    for p in P_VALUES:
        Z_p = project_pca(A, mean, eigenvectors, p)
        reconstructions[p] = reconstruct_pca(Z_p, mean, eigenvectors, p)

    # 4.3: compare the last two images with their reconstructions.
    plot_comparison(A, labels, reconstructions)

    # 4.4: mean squared error over the complete dataset, and how much of the total
    # variance the first p components keep.
    mse_values = [mse(A, reconstructions[p]) for p in P_VALUES]

    print(f"Total variance:               {eigenvalues.sum():.4f}")
    print(f"{'p':<5} | {'MSE':<8} | {'Check':<8} | {'Change':<9} | {'Variance kept'}")
    print("-" * 56)

    previous = None
    for p, mse_value in zip(P_VALUES, mse_values):
        variance_kept = eigenvalues[:p].sum() / eigenvalues.sum()
        # Check: the MSE equals the discarded eigenvalues, scaled by (m - 1) / m
        # (np.cov divides by m - 1) and averaged over the 256 pixels.
        check = eigenvalues[p:].sum() * (len(A) - 1) / len(A) / A.shape[1]
        change = "" if previous is None else f"{mse_value - previous:+.4f}"

        print(
            f"{p:<5} | {mse_value:<8.4f} | {check:<8.4f} | {change:<9} | "
            f"{variance_kept:.2%}"
        )

        previous = mse_value

    # 4.5: how many components keep a given share of the total variance.
    cumulative = np.cumsum(eigenvalues) / eigenvalues.sum()

    for share in [0.90, 0.95, 0.99]:
        needed = np.searchsorted(cumulative, share) + 1
        print(f"Components for {share:.0%} variance:    {needed}")

    plot_mse(mse_values)

    # The dev container has no display, so figures are saved to figures/ above
    # rather than shown in a window.
    plt.close("all")


if __name__ == "__main__":
    main()
