"""PCA from first principles (shared by Tasks 3 and 4)."""

import numpy as np  # noqa: F401


def fit_pca(X):
    # TODO: compute feature mean
    # TODO: center X
    # TODO: compute covariance matrix
    # TODO: compute eigenvalues/eigenvectors
    # TODO: sort from largest to smallest
    # return mean, eigenvalues, eigenvectors
    pass


def project_pca(X, mean, eigenvectors, p):
    # TODO: center X and project onto first p components
    pass


def reconstruct_pca(Z, mean, eigenvectors, p):
    # TODO: map scores back to feature space and add mean
    pass


def mse(X, X_hat):
    # TODO: return mean squared reconstruction error
    pass
