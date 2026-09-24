from pathlib import Path

import pandas as pd
import streamlit as st
import torch

from src.generate import generate_synthetic_data
from src.llm_engine import ask_dataset
from src.preprocessing import load_data
from src.train import train_vae


MODEL_PATH = Path("models/vae_model.pt")
SYNTHETIC_PATH = Path(
    "output/synthetic_diabetes.csv"
)


st.set_page_config(
    page_title="Synthetic Data Sandbox",
    layout="wide"
)

st.title("Synthetic Data Sandbox")
st.write(
    "Generate synthetic tabular data "
    "with a Variational Autoencoder."
)


st.header("1. Dataset")

real_df = load_data()

st.write(
    f"Rows: {len(real_df)} - "
    f"Columns: {len(real_df.columns)}"
)

st.dataframe(
    real_df.head(),
    use_container_width=True
)


st.header("2. Train VAE")

if st.button("Train model"):
    with st.spinner("Training VAE..."):
        model = train_vae()

        MODEL_PATH.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        torch.save(
            model.state_dict(),
            MODEL_PATH
        )

    st.success("Training completed.")


st.header("3. Generate synthetic data")

n_samples = st.number_input(
    "Number of synthetic rows",
    min_value=10,
    max_value=5000,
    value=500,
    step=10
)

if st.button("Generate data"):
    if not MODEL_PATH.exists():
        st.error(
            "Train the model first."
        )
    else:
        synthetic_df = generate_synthetic_data(
            n_samples=int(n_samples)
        )

        st.success(
            f"{len(synthetic_df)} rows generated."
        )


if SYNTHETIC_PATH.exists():
    synthetic_df = pd.read_csv(
        SYNTHETIC_PATH
    )

    st.subheader("Synthetic dataset")

    st.dataframe(
        synthetic_df.head(),
        use_container_width=True
    )

    st.download_button(
        "Download CSV",
        synthetic_df.to_csv(
            index=False
        ),
        file_name="synthetic_diabetes.csv",
        mime="text/csv"
    )

    st.header("4. Real vs synthetic")

    comparison = pd.DataFrame({
        "Real mean": real_df.mean(),
        "Synthetic mean": synthetic_df.mean(),
        "Real std": real_df.std(),
        "Synthetic std": synthetic_df.std(),
    })

    st.dataframe(
        comparison.round(3),
        use_container_width=True
    )

    selected_feature = st.selectbox(
        "Feature distribution",
        [
            column
            for column in real_df.columns
            if column != "Outcome"
        ]
    )

    chart_df = pd.DataFrame({
        "Real": real_df[selected_feature],
        "Synthetic": synthetic_df[
            selected_feature
        ]
    })

    st.line_chart(
        chart_df
    )

    st.header("5. Ask the synthetic data")

    question = st.text_input(
        "Ask a question about the dataset"
    )

    if st.button("Ask") and question:
        with st.spinner("Analysing..."):
            answer = ask_dataset(question)

        st.write(answer)

else:
    st.info(
        "Train the model and generate data "
        "to enable comparison and analysis."
    )
