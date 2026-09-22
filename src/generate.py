import numpy as np
import pandas as pd
import torch

from src.preprocessing import load_data, preprocess_data
from src.vae import VAE


def generate_synthetic_data(
    n_samples=500,
    latent_dim=4
):
    df = load_data()
    processed, imputer, scaler = preprocess_data(df)

    feature_columns = [
        column
        for column in processed.columns
        if column != "Outcome"
    ]

    model = VAE(
        input_dim=len(feature_columns),
        latent_dim=latent_dim
    )

    model.load_state_dict(
        torch.load(
            "models/vae_model.pt",
            map_location="cpu"
        )
    )

    model.eval()

    with torch.no_grad():
        z = torch.randn(n_samples, latent_dim)
        synthetic_scaled = model.decode(z).numpy()

    synthetic_features = scaler.inverse_transform(
        synthetic_scaled
    )

    synthetic_df = pd.DataFrame(
        synthetic_features,
        columns=feature_columns
    )

    outcome_probability = df["Outcome"].mean()

    synthetic_df["Outcome"] = np.random.binomial(
        1,
        outcome_probability,
        size=n_samples
    )

    for column in ["Pregnancies", "Age"]:
        synthetic_df[column] = (
            synthetic_df[column]
            .round()
            .astype(int)
        )

    synthetic_df.to_csv(
        "output/synthetic_diabetes.csv",
        index=False
    )

    return synthetic_df


if __name__ == "__main__":
    synthetic_df = generate_synthetic_data()

    print("Synthetic shape:", synthetic_df.shape)

    print("\nPrime 5 righe:")
    print(synthetic_df.head())

    print("\nDistribuzione Outcome:")
    print(synthetic_df["Outcome"].value_counts())

    print(
        "\nDataset salvato in "
        "output/synthetic_diabetes.csv"
    )
