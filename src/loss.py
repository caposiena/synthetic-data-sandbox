import torch
import torch.nn.functional as F


def vae_loss(
    reconstructed,
    x,
    mu,
    logvar,
    beta=0.01
):
    reconstruction_loss = F.mse_loss(
        reconstructed,
        x,
        reduction="sum"
    )

    kl_loss = -0.5 * torch.sum(
        1 + logvar - mu.pow(2) - logvar.exp()
    )

    total_loss = reconstruction_loss + beta * kl_loss

    return total_loss, reconstruction_loss, kl_loss
