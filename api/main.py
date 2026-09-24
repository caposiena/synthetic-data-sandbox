from pathlib import Path

import pandas as pd
import torch
from fastapi import FastAPI, HTTPException

from src.generate import generate_synthetic_data
from src.preprocessing import load_data
from src.train import train_vae

app = FastAPI(
    title="Synthetic Data Sandbox API",
    version="1.0"
)

MODEL_PATH = Path("models/vae_model.pt")
SYNTHETIC_PATH = Path("output/synthetic_diabetes.csv")


@app.get("/")
def root():
    return {
        "message": "Synthetic Data Sandbox API"
    }


@app.get("/status")
def status():
    return {
        "status": "ready",
        "model_available": MODEL_PATH.exists(),
        "synthetic_data_available": SYNTHETIC_PATH.exists()
    }


@app.post("/train")
def train():
    model = train_vae()

    MODEL_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    torch.save(
        model.state_dict(),
        MODEL_PATH
    )

    return {
        "status": "trained"
    }


@app.post("/generate")
def generate(n_samples: int = 500):
    if n_samples < 1:
        raise HTTPException(
            status_code=400,
            detail="n_samples must be greater than zero"
        )

    if not MODEL_PATH.exists():
        raise HTTPException(
            status_code=400,
            detail="Train the model before generating data"
        )

    synthetic_df = generate_synthetic_data(
        n_samples=n_samples
    )

    return {
        "status": "generated",
        "samples": len(synthetic_df)
    }


@app.get("/statistics")
def statistics():
    if not SYNTHETIC_PATH.exists():
        raise HTTPException(
            status_code=400,
            detail="Generate synthetic data first"
        )

    real_df = load_data()
    synthetic_df = pd.read_csv(SYNTHETIC_PATH)

    numeric_columns = [
        column
        for column in real_df.columns
        if column != "Outcome"
    ]

    result = {}

    for column in numeric_columns:
        result[column] = {
            "real_mean": round(
                float(real_df[column].mean()),
                3
            ),
            "synthetic_mean": round(
                float(synthetic_df[column].mean()),
                3
            ),
            "real_std": round(
                float(real_df[column].std()),
                3
            ),
            "synthetic_std": round(
                float(synthetic_df[column].std()),
                3
            ),
        }

    return {
        "features": result,
        "real_outcome_rate": round(
            float(real_df["Outcome"].mean()),
            3
        ),
        "synthetic_outcome_rate": round(
            float(synthetic_df["Outcome"].mean()),
            3
        ),
    }
