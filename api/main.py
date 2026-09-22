from fastapi import FastAPI

from src.generate import generate_synthetic_data
from src.train import train_vae

app = FastAPI(
    title="Synthetic Data Sandbox API",
    version="1.0"
)


@app.get("/")
def root():
    return {
        "message": "Synthetic Data Sandbox API"
    }


@app.get("/status")
def status():
    return {
        "status": "ready"
    }


@app.post("/train")
def train():
    model = train_vae()

    import torch

    torch.save(
        model.state_dict(),
        "models/vae_model.pt"
    )

    return {
        "status": "trained"
    }


@app.post("/generate")
def generate(n_samples: int = 500):
    synthetic_df = generate_synthetic_data(
        n_samples=n_samples
    )

    return {
        "status": "generated",
        "samples": len(synthetic_df)
    }
