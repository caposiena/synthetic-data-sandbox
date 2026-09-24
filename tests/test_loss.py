import torch

from src.loss import vae_loss
from src.vae import VAE


def test_vae_loss_is_positive():
    model = VAE(input_dim=8, latent_dim=4)

    x = torch.rand(8, 8)

    reconstructed, mu, logvar = model(x)

    total_loss, reconstruction_loss, kl_loss = vae_loss(
        reconstructed,
        x,
        mu,
        logvar
    )

    assert total_loss.item() > 0
    assert reconstruction_loss.item() >= 0
    assert kl_loss.item() >= 0


def test_vae_loss_has_gradient():
    model = VAE(input_dim=8, latent_dim=4)

    x = torch.rand(8, 8)

    reconstructed, mu, logvar = model(x)

    total_loss, _, _ = vae_loss(
        reconstructed,
        x,
        mu,
        logvar
    )

    total_loss.backward()

    gradients = [
        parameter.grad
        for parameter in model.parameters()
        if parameter.requires_grad
    ]

    assert any(
        gradient is not None
        for gradient in gradients
    )
