import torch
from torch.optim import Adam

from src.loss import vae_loss
from src.preprocessing import load_data, preprocess_data
from src.vae import VAE


def main():
    df = load_data()
    processed, _, _ = preprocess_data(df)

    x = processed.astype("float32")
    x_tensor = torch.tensor(x.values)

    input_dim = x_tensor.shape[1]

    model = VAE(
        input_dim=input_dim,
        latent_dim=4
    )

    optimizer = Adam(
        model.parameters(),
        lr=0.001
    )

    model.train()

    optimizer.zero_grad()

    reconstructed, mu, logvar = model(x_tensor)

    total_loss, reconstruction_loss, kl_loss = vae_loss(
        reconstructed,
        x_tensor,
        mu,
        logvar
    )

    total_loss.backward()
    optimizer.step()

    print("Dataset shape:", x_tensor.shape)
    print("Input dimension:", input_dim)
    print("Latent dimension:", mu.shape[1])

    print("\nLoss:")
    print("Total:", round(total_loss.item(), 4))
    print("Reconstruction:", round(reconstruction_loss.item(), 4))
    print("KL:", round(kl_loss.item(), 4))


if __name__ == "__main__":
    main()
