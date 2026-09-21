import torch
from torch import nn


class VAE(nn.Module):
    def __init__(self, input_dim, latent_dim=4):
        super().__init__()

        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 16),
            nn.ReLU(),
            nn.Linear(16, 8),
            nn.ReLU(),
        )

        self.fc_mu = nn.Linear(8, latent_dim)
        self.fc_logvar = nn.Linear(8, latent_dim)

        self.decoder = nn.Sequential(
            nn.Linear(latent_dim, 8),
            nn.ReLU(),
            nn.Linear(8, 16),
            nn.ReLU(),
            nn.Linear(16, input_dim),
            nn.Sigmoid(),
        )

    def encode(self, x):
        hidden = self.encoder(x)
        mu = self.fc_mu(hidden)
        logvar = self.fc_logvar(hidden)
        return mu, logvar

    def reparameterize(self, mu, logvar):
        std = torch.exp(0.5 * logvar)
        epsilon = torch.randn_like(std)
        return mu + epsilon * std

    def decode(self, z):
        return self.decoder(z)

    def forward(self, x):
        mu, logvar = self.encode(x)
        z = self.reparameterize(mu, logvar)
        reconstructed = self.decode(z)
        return reconstructed, mu, logvar


if __name__ == "__main__":
    input_dim = 9
    batch_size = 5

    model = VAE(input_dim=input_dim, latent_dim=4)

    sample = torch.rand(batch_size, input_dim)

    reconstructed, mu, logvar = model(sample)

    print("Input shape:", sample.shape)
    print("Reconstructed shape:", reconstructed.shape)
    print("Mu shape:", mu.shape)
    print("Logvar shape:", logvar.shape)
