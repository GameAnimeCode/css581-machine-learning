"""Task 4: PCA on USPS handwritten digits.

The dataset lives at data/USPS_digits_python.npz.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from pca import fit_pca, mse, project_pca, reconstruct_pca  # noqa: F401

P_VALUES = [10, 50, 100, 150, 200]
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "USPS_digits_python.npz"


def load_usps(path: Path = DATA_PATH):
    """4.1: load images (3000 x 256) and labels (3000,)."""
    data = np.load(path, allow_pickle=False)
    A = data["images"].astype(float)  # shape: (3000, 256)
    labels = data["labels"].ravel()  # shape: (3000,)
    return A, labels


def main() -> None:
    A, labels = load_usps()
    print(A.shape, labels.shape)

    # Display one 16 x 16 image.
    image = A[1].reshape(16, 16)
    plt.imshow(image.T, cmap="gray")
    plt.axis("off")
    plt.show()

    # TODO 4.1: mean image and centered data (no per-pixel standardization)
    # TODO 4.2: fit_pca, then project/reconstruct for each p in P_VALUES
    # TODO 4.3: figure with A[-2] and A[-1]: Original plus p = 10, 50, 100, 150, 200
    #           (one row per image, six columns, digit label in the row title)
    # TODO 4.4: MSE over the full dataset for each p, table and optional line plot


if __name__ == "__main__":
    main()
