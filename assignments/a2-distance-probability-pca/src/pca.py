"""PCA from first principles (shared by Tasks 3 and 4)."""

import numpy as np


def fit_pca(X):
    """
    Fit PCA to X (m observations x n features).

    Returns the feature mean, the eigenvalues of the sample covariance matrix
    sorted largest to smallest, the matching eigenvectors as columns, and the
    covariance matrix itself.
    """
    # Feature-wise mean: axis=0 averages down each column.
    mean = np.mean(X, axis=0)

    # Center so the cloud sits on the origin without changing its shape.
    X_centered = X - mean

    # Sample covariance, C = Xc^T Xc / (m - 1).
    # rowvar=False treats columns as features.
    cov = np.cov(X_centered, rowvar=False)

    # eigh is for symmetric matrices and returns eigenvalues in ascending order.
    eigenvalues, eigenvectors = np.linalg.eigh(cov)

    # Reverse so the largest eigenvalue (direction of maximum stretch) is first.
    eigenvalues = eigenvalues[::-1]
    eigenvectors = eigenvectors[:, ::-1]

    return mean, eigenvalues, eigenvectors, cov


def project_pca(X, mean, eigenvectors, p):
    """Center X and project onto the first p principal components: Z = Xc V_p."""
    V_p = eigenvectors[:, :p]
    return np.dot(X - mean, V_p)


def reconstruct_pca(Z, mean, eigenvectors, p):
    """Map scores back to feature space and add the mean: Z V_p^T + 1 mu^T."""
    V_p = eigenvectors[:, :p]
    return np.dot(Z, V_p.T) + mean


def mse(X, X_hat):
    # TODO: return mean squared reconstruction error
    pass
