import torch

from src.vae import VAE


def test_vae_output_shapes():
    input_dim = 9
    latent_dim = 4
    batch_size = 8

    model = VAE(
        input_dim=input_dim,
        latent_dim=latent_dim
    )

    x = torch.rand(batch_size, input_dim)

    reconstructed, mu, logvar = model(x)

    assert reconstructed.shape == x.shape
    assert mu.shape == (batch_size, latent_dim)
    assert logvar.shape == (batch_size, latent_dim)


def test_decoder_output_range():
    model = VAE(input_dim=9, latent_dim=4)

    z = torch.randn(8, 4)
    decoded = model.decode(z)

    assert decoded.min().item() >= 0.0
    assert decoded.max().item() <= 1.0
