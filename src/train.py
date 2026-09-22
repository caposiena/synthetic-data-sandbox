import torch
from torch.utils.data import DataLoader, TensorDataset
from torch.optim import Adam

from src.loss import vae_loss
from src.preprocessing import load_data, preprocess_data
from src.vae import VAE


def prepare_data():
    df = load_data()
    processed, _, _ = preprocess_data(df)

    features = processed.drop(columns=["Outcome"]).astype("float32")
    x_tensor = torch.tensor(features.values)

    return x_tensor


def train_vae(
    epochs=50,
    batch_size=32,
    learning_rate=0.001,
    latent_dim=4
):
    x_tensor = prepare_data()

    dataset = TensorDataset(x_tensor)

    dataloader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=True
    )

    model = VAE(
        input_dim=x_tensor.shape[1],
        latent_dim=latent_dim
    )

    optimizer = Adam(
        model.parameters(),
        lr=learning_rate
    )

    model.train()

    for epoch in range(1, epochs + 1):
        epoch_loss = 0.0

        for batch in dataloader:
            x_batch = batch[0]

            optimizer.zero_grad()

            reconstructed, mu, logvar = model(x_batch)

            total_loss, _, _ = vae_loss(
                reconstructed,
                x_batch,
                mu,
                logvar
            )

            total_loss.backward()
            optimizer.step()

            epoch_loss += total_loss.item()

        average_loss = epoch_loss / len(dataset)

        if epoch == 1 or epoch % 10 == 0:
            print(
                f"Epoch {epoch:3d} "
                f"- loss: {average_loss:.4f}"
            )

    return model


if __name__ == "__main__":
    model = train_vae()

    torch.save(
        model.state_dict(),
        "models/vae_model.pt"
    )

    print("\nModello salvato in models/vae_model.pt")
