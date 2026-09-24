import os

import pandas as pd
from openai import OpenAI


def dataset_context(
    path="output/synthetic_diabetes.csv"
):
    df = pd.read_csv(path)

    summary = df.describe().round(2).to_string()

    outcome = (
        df["Outcome"]
        .value_counts(normalize=True)
        .sort_index()
        .round(3)
        .to_string()
    )

    return (
        "Synthetic dataset summary:\n"
        + summary
        + "\n\nOutcome distribution:\n"
        + outcome
    )


def ask_dataset(question):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "OPENAI_API_KEY is not configured. "
            "The rest of the application can still be used."
        )

    client = OpenAI(api_key=api_key)

    context = dataset_context()

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=(
            "Answer only using the following statistics "
            "from a synthetic diabetes dataset. "
            "If the answer cannot be derived from the "
            "available information, say so.\n\n"
            f"{context}\n\n"
            f"Question: {question}"
        )
    )

    return response.output_text
