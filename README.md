# Synthetic Data Sandbox

Final project for Module 6.

The project uses a Variational Autoencoder implemented in PyTorch to generate synthetic tabular data.

The example dataset is the Pima Indians Diabetes dataset.

## Project structure

- data preprocessing with pandas and scikit-learn
- VAE model implemented in PyTorch
- training with DataLoader and Adam
- synthetic data generation
- comparison between real and synthetic statistics
- FastAPI backend
- Streamlit interface
- optional natural language analysis

## Preprocessing

Invalid zero values in selected medical variables are treated as missing values.

Missing values are replaced with the median and numerical features are scaled with MinMaxScaler.

## VAE

The encoder produces the mean and log variance of the latent distribution.

Sampling uses the reparameterization trick.

The decoder reconstructs the numerical features.

The loss combines reconstruction error and KL divergence. A small beta value is used to reduce excessive concentration of generated samples.

Outcome is generated separately according to its observed proportion in the training dataset.

## Installation

Create a virtual environment and install the dependencies:

    pip install -r requirements.txt

## Training

Run:

    python -m src.train

The trained model is saved in:

    models/vae_model.pt

## Generate synthetic data

Run:

    python -m src.generate

The generated dataset is saved in:

    output/synthetic_diabetes.csv

## Evaluation

Run:

    python -m src.evaluation

The script compares mean, standard deviation and Outcome distribution between the real and synthetic datasets.

## API

Start FastAPI with:

    uvicorn api.main:app --reload

The main endpoints are:

    GET /status
    POST /train
    POST /generate
    GET /statistics

## Streamlit

Start the interface with:

    streamlit run app.py

## Natural language analysis

The natural language section is optional.

Set the OPENAI_API_KEY environment variable before starting Streamlit to enable it.

No API key is stored in the repository.

## Tests

Run:

    pytest -v

## Limitations

The VAE reproduces average values reasonably well but the synthetic distributions remain less variable than the original data.

This is expected from the small model and dataset and is visible in the statistical comparison.

Synthetic data generation alone should not be considered a formal guarantee of anonymization.
